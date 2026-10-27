/*
 * qgpu_accel.cpp
 * QGAOPS-QGPU Simple HLS Accelerator — Implementation
 *
 * Project  : QGAOPS_SIMPLE_HW
 * Board    : Xilinx ZedBoard (xc7z020clg484-1)
 * PL Clock : 100 MHz  (T = 10 ns)
 * HLS Tool : Vitis HLS 2025.2
 *
 * DESIGN RULES (non-negotiable):
 *   - No PIPELINE, DATAFLOW, UNROLL, or ARRAY_PARTITION pragmas
 *   - No manual scheduling directives
 *   - Plain C++ loops for all arithmetic
 *   - AXI interface directives ONLY (required to define interfaces)
 *   - Functionally correct before any performance optimisation
 *
 * OPERATIONS IMPLEMENTED (Phase 1):
 *   OPCODE_ADDVEC  (0x01) — array add/subtract:  C=A+B, D=A-B
 *   OPCODE_GP      (0x02) — G3 geometric product: C = A*B
 *   OPCODE_WEDGE   (0x03) — G3 outer (wedge) product: C = A^B
 *   OPCODE_INNER   (0x04) — G3 left inner product: C = A.B
 *
 * DATA FLOW (using AXI DMA Scatter-Gather or Simple DMA):
 *
 *   ARM DDR ──► AXI DMA MM2S ──► in_stream ──► qgpu_accel ──► out_stream ──► AXI DMA S2MM ──► ARM DDR
 *
 * STREAM PROTOCOL:
 *   Word 0 (32-bit): opcode  (lower 8 bits)
 *   Word 1 (32-bit): N       (element count for ADDVEC; must be 8 for GP/WEDGE/INNER)
 *   Words 2+:        N × int16 A values (packed 2 per 32-bit word, little-endian)
 *                    N × int16 B values
 *
 *   Result:
 *   ADDVEC: N × int16 C = A+B, then N × int16 D = A-B
 *   GP/WEDGE/INNER: 8 × int16 result multivector
 */

#include "qgpu_accel.h"
#include <string.h>

/* =========================================================================
 * FIX16 Q1.14 ARITHMETIC PRIMITIVES
 *
 * These are simple C functions — no HLS pragmas.
 * HLS will infer appropriate datapaths automatically.
 * ========================================================================= */

/**
 * fix16_add() — Saturating signed 16-bit addition.
 *
 * Overflow behaviour:
 *   If a + b > FIX16_MAX  → clamp to FIX16_MAX  (+32767)
 *   If a + b < FIX16_MIN  → clamp to FIX16_MIN  (-32768)
 *   Else exact result.
 */
fix16_t fix16_add(fix16_t a, fix16_t b)
{
    fix32_t result = (fix32_t)a + (fix32_t)b;
    if (result > FIX16_MAX)  return (fix16_t)FIX16_MAX;
    if (result < FIX16_MIN)  return (fix16_t)FIX16_MIN;
    return (fix16_t)result;
}

/**
 * fix16_sub() — Saturating signed 16-bit subtraction.
 */
fix16_t fix16_sub(fix16_t a, fix16_t b)
{
    fix32_t result = (fix32_t)a - (fix32_t)b;
    if (result > FIX16_MAX)  return (fix16_t)FIX16_MAX;
    if (result < FIX16_MIN)  return (fix16_t)FIX16_MIN;
    return (fix16_t)result;
}

/**
 * fix16_mul() — Q1.14 × Q1.14 → Q1.14
 *
 * Steps:
 *   1. 16×16 signed multiply → 32-bit product  (Q2.28)
 *   2. Arithmetic right-shift by 14 → Q2.14   (truncate, no round)
 *   3. Saturate to [-32768, 32767]
 *
 * The intermediate 32-bit value prevents intermediate overflow.
 */
fix16_t fix16_mul(fix16_t a, fix16_t b)
{
    fix32_t product = (fix32_t)a * (fix32_t)b;   /* Q2.28 */
    fix32_t shifted = product >> 14;              /* Q2.14, truncated */
    if (shifted > FIX16_MAX)  return (fix16_t)FIX16_MAX;
    if (shifted < FIX16_MIN)  return (fix16_t)FIX16_MIN;
    return (fix16_t)shifted;
}

/**
 * fix16_mac() — Multiply-accumulate into 32-bit accumulator.
 *
 * Used in the geometric product inner loop.
 * Accumulator holds the raw Q2.28 sum before final saturation.
 * *acc += a * b
 */
void fix16_mac(fix32_t* acc, fix16_t a, fix16_t b)
{
    *acc += (fix32_t)a * (fix32_t)b;
}

/**
 * fix16_saturate() — Saturate 32-bit accumulator to FIX16 range.
 *
 * Call after the inner MAC loop.
 * The accumulator is in Q2.28 if all MACs are raw products,
 * or in Q2.14 if pre-shifted. We pre-shift here.
 */
fix16_t fix16_saturate(fix32_t v)
{
    if (v > FIX16_MAX)  return (fix16_t)FIX16_MAX;
    if (v < FIX16_MIN)  return (fix16_t)FIX16_MIN;
    return (fix16_t)v;
}

/* =========================================================================
 * ARRAY ADD / SUBTRACT
 *
 * Implements:  C[i] = A[i] + B[i]
 *              D[i] = A[i] - B[i]
 *
 * This is the first proof-of-function operation.
 * Input arrays are in FIX16 (Q1.14 signed 16-bit).
 * Overflow is saturating.
 * ========================================================================= */

static void op_addvec(
    const fix16_t* A,
    const fix16_t* B,
    fix16_t*       C,   /* C = A + B */
    fix16_t*       D,   /* D = A - B */
    uint32_t       N
)
{
    uint32_t i;
    for (i = 0; i < N; i++) {
        C[i] = fix16_add(A[i], B[i]);
        D[i] = fix16_sub(A[i], B[i]);
    }
}

/* =========================================================================
 * G3 GEOMETRIC PRODUCT
 *
 * Algorithm (matches ga/geometric_product.py::geometric_product):
 *
 *   For each pair (ia, ib):
 *     ic = ia XOR ib          (result blade index = XOR of input masks)
 *     sign = G3_SIGN[ia][ib]  (permutation sign from sign_product())
 *     metric = G3_METRIC(ia, ib)  (for G(3,0,0): always +1 when shared
 *                                  bits exist, product = sign × 1 = sign)
 *     C[ic] += A[ia] × B[ib] × sign
 *
 * Coefficient width:
 *   A[ia] and B[ib] are Q1.14 (16-bit).
 *   The product is Q2.28 (32-bit), accumulated in fix32_t.
 *   After accumulation, right-shift 14 to return to Q1.14 and saturate.
 *
 * G3 METRIC NOTE:
 *   For G(3,0,0): e0²=+1, e1²=+1, e2²=+1.
 *   metric_coefficient(mask_a, mask_b) = product of signature[i]
 *   for shared bits = always +1 in G3.
 *   Therefore: coeff = sign_product(mask_a, mask_b) × 1 = sign only.
 *
 * The sign table G3_SIGN is precomputed from ga/basis.py::sign_product()
 * and verified in the C testbench against Python-generated vectors.
 * ========================================================================= */

void g3_geometric_product(const G3_mv A, const G3_mv B, G3_mv C)
{
    /* Accumulate in 32-bit to hold full Q2.28 sums before shift */
    fix32_t acc[G3_DIM];
    int ic;

    /* Zero the accumulator */
    for (ic = 0; ic < G3_DIM; ic++) {
        acc[ic] = 0;
    }

    /* Double loop: O(64) multiply-accumulates */
    int ia, ib;
    for (ia = 0; ia < G3_DIM; ia++) {
        if (A[ia] == 0) continue;   /* sparse optimisation (no pragma needed) */
        for (ib = 0; ib < G3_DIM; ib++) {
#pragma HLS PIPELINE off
            if (B[ib] == 0) continue;
            ic = ia ^ ib;                        /* result blade by XOR */
            int8_t sgn = G3_SIGN[ia][ib];        /* permutation sign    */
            fix32_t term = (fix32_t)A[ia] * (fix32_t)B[ib];
            if (sgn > 0)
                acc[ic] += term;
            else
                acc[ic] -= term;
        }
    }

    /* Convert accumulated Q2.28 products to Q1.14, then saturate */
    for (ic = 0; ic < G3_DIM; ic++) {
        C[ic] = fix16_saturate(acc[ic] >> 14);
    }
}

/* =========================================================================
 * G3 OUTER (WEDGE) PRODUCT
 *
 * Algorithm (matches ga/geometric_product.py::outer_product):
 *
 *   For each pair (ia, ib):
 *     Include term ONLY if mask_a AND mask_b == 0
 *     (i.e., the two blades share no basis vectors)
 *     ic = ia XOR ib  (= ia OR ib when no overlap)
 *     C[ic] += A[ia] × B[ib] × sign_product(mask_a, mask_b)
 *
 * No metric correction needed (metric only appears on shared indices).
 * ========================================================================= */

void g3_outer_product(const G3_mv A, const G3_mv B, G3_mv C)
{
    fix32_t acc[G3_DIM];
    int ic;

    for (ic = 0; ic < G3_DIM; ic++) {
        acc[ic] = 0;
    }

    int ia, ib;
    for (ia = 0; ia < G3_DIM; ia++) {
        if (A[ia] == 0) continue;
        for (ib = 0; ib < G3_DIM; ib++) {
#pragma HLS PIPELINE off
            if (B[ib] == 0) continue;
            /* Wedge condition: masks must not share any bit */
            if (ia & ib) continue;
            ic = ia ^ ib;
            int8_t sgn = G3_SIGN[ia][ib];
            fix32_t term = (fix32_t)A[ia] * (fix32_t)B[ib];
            if (sgn > 0)
                acc[ic] += term;
            else
                acc[ic] -= term;
        }
    }

    for (ic = 0; ic < G3_DIM; ic++) {
        C[ic] = fix16_saturate(acc[ic] >> 14);
    }
}

/* =========================================================================
 * G3 LEFT INNER (DOT) PRODUCT
 *
 * Algorithm (matches ga/geometric_product.py::inner_product):
 *
 *   Hestenes convention: zero if either operand grade == 0.
 *   For grade_a > 0 and grade_b > 0:
 *     mask_c = mask_a XOR mask_b
 *     Include term only if grade(mask_c) == |grade_a - grade_b|
 *     C[ic] += A[ia] × B[ib] × sign × metric
 *
 * For G(3,0,0) metric applies when mask_a AND mask_b != 0.
 * Here metric = +1 for all shared basis vectors (all positive signature).
 * ========================================================================= */

/* Helper: popcount = number of set bits (= grade of mask) */
static int popcount3(int mask)
{
    return ((mask >> 0) & 1) + ((mask >> 1) & 1) + ((mask >> 2) & 1);
}

void g3_inner_product(const G3_mv A, const G3_mv B, G3_mv C)
{
    fix32_t acc[G3_DIM];
    int ic;

    for (ic = 0; ic < G3_DIM; ic++) {
        acc[ic] = 0;
    }

    int ia, ib;
    for (ia = 0; ia < G3_DIM; ia++) {
        if (A[ia] == 0) continue;
        int grade_a = popcount3(ia);
        if (grade_a == 0) continue;     /* Hestenes: skip scalar grade */
        for (ib = 0; ib < G3_DIM; ib++) {
#pragma HLS PIPELINE off
            if (B[ib] == 0) continue;
            int grade_b = popcount3(ib);
            if (grade_b == 0) continue;
            ic = ia ^ ib;
            int grade_c = popcount3(ic);
            int expected_grade = grade_a - grade_b;
            if (expected_grade < 0) expected_grade = -expected_grade;
            if (grade_c != expected_grade) continue;
            int8_t sgn = G3_SIGN[ia][ib];
            fix32_t term = (fix32_t)A[ia] * (fix32_t)B[ib];
            if (sgn > 0)
                acc[ic] += term;
            else
                acc[ic] -= term;
        }
    }

    for (ic = 0; ic < G3_DIM; ic++) {
        C[ic] = fix16_saturate(acc[ic] >> 14);
    }
}

/* =========================================================================
 * STREAM PACK / UNPACK HELPERS
 *
 * The AXI DMA transfers 32-bit words.
 * Two int16 samples are packed into one 32-bit stream word:
 *   bits[15: 0] = sample[2k]   (first)
 *   bits[31:16] = sample[2k+1] (second)
 *
 * For odd N: the last 32-bit word has bits[31:16] = 0 (padding).
 * ========================================================================= */

static void stream_read_words(axis_t& stream, fix16_t* buf, uint32_t n)
{
    uint32_t words = (n + 1) / 2;  /* ceil(n/2) 32-bit words */
    uint32_t i;
    for (i = 0; i < words; i++) {
        stream_word_t w = stream.read();
        buf[2*i]   = (fix16_t)(int16_t)(w.data & 0xFFFF);
        if (2*i + 1 < n)
            buf[2*i+1] = (fix16_t)(int16_t)((w.data >> 16) & 0xFFFF);
    }
}

static void stream_write_words(axis_t& stream, const fix16_t* buf, uint32_t n, bool is_last)
{
    uint32_t words = (n + 1) / 2;
    uint32_t i;
    for (i = 0; i < words; i++) {
        stream_word_t w;
        ap_uint<32> d = 0;
        d |= ((ap_uint<32>)(uint16_t)buf[2*i]);
        if (2*i + 1 < n)
            d |= ((ap_uint<32>)(uint16_t)buf[2*i+1]) << 16;
        w.data = d;
        w.keep = 0xF;
        w.strb = 0xF;
        w.last = (is_last && (i == words - 1)) ? 1 : 0;
        stream.write(w);
    }
}

/* =========================================================================
 * TOP-LEVEL HLS FUNCTION: qgpu_accel()
 *
 * AXI4-Stream interfaces (connect to AXI DMA in block design):
 *   in_stream  — carries input data from PS/DDR via DMA MM2S
 *   out_stream — carries result data back to PS/DDR via DMA S2MM
 *
 * AXI4-Lite control interface (s_axilite bundle=ctrl):
 *   status     — current state (idle/busy/done/error)
 *   op_count   — number of completed operations (for diagnostics)
 *
 * STREAM PROTOCOL (simple framing, no handshake overhead):
 *   Word 0: opcode (uint32)
 *   Word 1: N      (uint32, element count)
 *   Words 2..(1+ceil(N/2)): A array (N int16 packed as 32-bit pairs)
 *   Next ceil(N/2) words:   B array
 *
 * RESULT:
 *   For OPCODE_ADDVEC: ceil(N/2) words C, then ceil(N/2) words D (last word sets TLAST)
 *   For OPCODE_GP/WEDGE/INNER: ceil(8/2)=4 words (8 int16 result MV, 4th word sets TLAST)
 * ========================================================================= */


//top function
void qgpu_accel(
    axis_t            &in_stream,
    axis_t            &out_stream,
    volatile uint32_t *status,
    volatile uint32_t *op_count
)
{
/* ------- AXI4-Stream interface directives (required, not algorithm) ------- */
#pragma HLS INTERFACE axis port=in_stream  name=s_axis
#pragma HLS INTERFACE axis port=out_stream name=m_axis

/* ------- AXI4-Lite control registers --------------------------------- */
#pragma HLS INTERFACE s_axilite port=status   bundle=ctrl
#pragma HLS INTERFACE s_axilite port=op_count bundle=ctrl
#pragma HLS INTERFACE s_axilite port=return   bundle=ctrl

    /* Persistent operation counter (static retains value between calls) */
    static uint32_t s_op_count = 0;

    /* Signal we are now executing */
    *status = STATUS_BUSY;

    /* ------------------------------------------------------------------ */
    /* Step 1: Read header from stream                                     */
    /* ------------------------------------------------------------------ */
    stream_word_t hdr0  = in_stream.read();  /* opcode word */
    stream_word_t hdr1  = in_stream.read();  /* N word      */

    uint32_t opcode = (uint32_t)(hdr0.data & 0xFF);
    uint32_t N      = (uint32_t)hdr1.data;

    /* Clamp N to maximum supported length */
    if (N > ACCEL_MAX_N) {
        *status    = STATUS_ERR_LEN;
        *op_count  = s_op_count;
        return;
    }

    /* ------------------------------------------------------------------ */
    /* Step 2: Read input arrays from stream into local buffers            */
    /* ------------------------------------------------------------------ */
    fix16_t A[ACCEL_MAX_N];
    fix16_t B[ACCEL_MAX_N];
    fix16_t C[ACCEL_MAX_N];
    fix16_t D[ACCEL_MAX_N];

    stream_read_words(in_stream, A, N);
    stream_read_words(in_stream, B, N);

    /* ------------------------------------------------------------------ */
    /* Step 3: Execute selected operation                                  */
    /* ------------------------------------------------------------------ */
    if (opcode == OPCODE_ADDVEC) {
        /* Array addition and subtraction */
        op_addvec(A, B, C, D, N);

        /* Write results: C first, then D with TLAST on the final word */
        stream_write_words(out_stream, C, N, false);
        stream_write_words(out_stream, D, N, true);

        s_op_count++;
        *status    = STATUS_DONE;
        *op_count  = s_op_count;

    } else if (opcode == OPCODE_GP) {
        /* G3 Geometric Product — requires N=8 */
        G3_mv R;
        g3_geometric_product(
            (const fix16_t*)A,
            (const fix16_t*)B,
            R
        );
        stream_write_words(out_stream, R, G3_DIM, true);

        s_op_count++;
        *status    = STATUS_DONE;
        *op_count  = s_op_count;

    } else if (opcode == OPCODE_WEDGE) {
        /* G3 Outer (Wedge) Product */
        G3_mv R;
        g3_outer_product(
            (const fix16_t*)A,
            (const fix16_t*)B,
            R
        );
        stream_write_words(out_stream, R, G3_DIM, true);

        s_op_count++;
        *status    = STATUS_DONE;
        *op_count  = s_op_count;

    } else if (opcode == OPCODE_INNER) {
        /* G3 Left Inner Product */
        G3_mv R;
        g3_inner_product(
            (const fix16_t*)A,
            (const fix16_t*)B,
            R
        );
        stream_write_words(out_stream, R, G3_DIM, true);

        s_op_count++;
        *status    = STATUS_DONE;
        *op_count  = s_op_count;

    } else {
        /* Unknown opcode */
        *status    = STATUS_ERR_OP;
        *op_count  = s_op_count;
    }
}
