/*
 * qgpu_accel.h
 * QGAOPS-QGPU Simple HLS Accelerator — Header
 *
 * Project  : QGAOPS_SIMPLE_HW
 * Board    : Xilinx ZedBoard (xc7z020clg484-1)
 * PL Clock : 100 MHz  (T = 10 ns)
 * HLS Tool : Vitis HLS 2025.2
 *
 * ==========================================================================
 * ARITHMETIC CONTRACT (FIX16 / Q1.14)
 * ==========================================================================
 *  Representation  : signed 16-bit two's complement
 *  Integer bits    : 2  (range −2 to +1.999...)
 *  Fractional bits : 14
 *  Scale           : 1.0 = 16384  (0x4000)
 *  Range           : [−2.0, +1.999938...]
 *  Overflow        : saturating (clamp to min/max)
 *  Rounding        : truncation (>>14 after multiply)
 *  Product width   : 32-bit intermediate before right-shift
 *
 * G3 BASIS ENCODING (bitmask order — from ga/multivector.py)
 * ==========================================================================
 *  Index  Mask  Name    Grade
 *  0      0b000 scalar  0
 *  1      0b001 e0      1
 *  2      0b010 e1      1
 *  3      0b011 e01     2
 *  4      0b100 e2      1
 *  5      0b101 e02     2
 *  6      0b110 e12     2
 *  7      0b111 e012    3
 *
 * G3 METRIC: G(3,0,0)  →  e0²=+1, e1²=+1, e2²=+1
 *
 * ==========================================================================
 * INTERFACE DESIGN
 * ==========================================================================
 *  AXI4-Stream IN  (from AXI DMA MM2S)  : carries packed payload
 *  AXI4-Stream OUT (to   AXI DMA S2MM)  : carries packed result
 *  AXI4-Lite CTRL  (s_axilite)          : opcode, status, length registers
 *
 * STREAM PAYLOAD FORMAT (per transaction):
 *  Header word 0: opcode  (32-bit, lower 8 bits used)
 *  Header word 1: N       (32-bit, element count)
 *  Data words 2…: N int16 values for array A, then N int16 values for B
 *
 * RESULT STREAM FORMAT:
 *  N int16 values for array C (A+B), then N int16 values for D (A-B)
 *
 * For the G3 geometric product:
 *  Header opcode = OPCODE_GP (0x02)
 *  Data: 8 int16 for multivector A, then 8 int16 for B
 *  Result: 8 int16 for C = A*B (geometric product)
 */

#ifndef QGPU_ACCEL_H
#define QGPU_ACCEL_H

#include <stdint.h>
#include <ap_int.h>
#include <hls_stream.h>
#include <ap_axi_sdata.h>

/* =========================================================================
 * CONSTANTS
 * ========================================================================= */

/* FIX16 scale: 1.0 is represented as 16384 */
#define FIX16_SCALE       16384
#define FIX16_MAX         32767     /* +1.99993... */
#define FIX16_MIN         (-32768)  /* -2.0 */

/* G3 dimension: 2^3 = 8 basis blades */
#define G3_DIM            8

/* Maximum array length supported by the accelerator */
#define ACCEL_MAX_N       256

/* Opcodes — transmitted in stream header word 0 */
#define OPCODE_NOP        0x00   /* No operation */
#define OPCODE_ADDVEC     0x01   /* Array add/subtract:  C=A+B, D=A-B */
#define OPCODE_GP         0x02   /* G3 geometric product: C = A*B */
#define OPCODE_WEDGE      0x03   /* G3 outer product:    C = A^B */
#define OPCODE_INNER      0x04   /* G3 inner product:    C = A.B */

/* Status codes returned in AXI-Lite status register */
#define STATUS_IDLE       0x00
#define STATUS_BUSY       0x01
#define STATUS_DONE       0x02
#define STATUS_ERR_OP     0x10  /* Unknown opcode */
#define STATUS_ERR_LEN    0x11  /* Length out of range */

/* =========================================================================
 * TYPES
 * ========================================================================= */

/* AXI4-Stream packet with TLAST and TKEEP for AXI DMA S2MM compatibility */
typedef ap_axiu<32, 0, 0, 0> stream_word_t;

/* AXI4-Stream interface type */
typedef hls::stream<stream_word_t> axis_t;

/* Fixed-point coefficient — signed 16-bit Q1.14 */
typedef int16_t fix16_t;

/* Intermediate product — signed 32-bit to hold 16×16 product */
typedef int32_t fix32_t;

/* G3 multivector: 8 coefficients, index = basis mask */
typedef fix16_t G3_mv[G3_DIM];

/* =========================================================================
 * G3 SIGN TABLE
 * Precomputed: SIGN[ia][ib] = permutation sign for e_{ia} * e_{ib}
 *
 * Derived from Python ga/basis.py::sign_product(mask_a, mask_b)
 * using G(3,0,0) metric (all +1).
 *
 * Layout: SIGN[row=ia][col=ib], value ∈ {+1, -1}
 *
 *   Mask encoding:  0=scalar,1=e0,2=e1,3=e01,4=e2,5=e02,6=e12,7=e012
 *
 *      ib:  0   1   2   3   4   5   6   7
 *  ia=0:  [ 1,  1,  1,  1,  1,  1,  1,  1]
 *  ia=1:  [ 1,  1,  1,  1,  1,  1,  1,  1]  (e0 * anything)
 *  ia=2:  [ 1,  1,  1,  1,  1,  1,  1,  1]
 *  ia=3:  [ 1,  1, -1, -1,  1,  1, -1, -1]
 *  ia=4:  [ 1,  1,  1,  1,  1,  1,  1,  1]
 *  ia=5:  [ 1,  1, -1, -1, -1, -1,  1,  1]
 *  ia=6:  [ 1,  1,  1,  1, -1, -1, -1, -1]
 *  ia=7:  [ 1,  1, -1, -1, -1, -1,  1,  1]
 *
 * See docs/ENVIRONMENT_AUDIT.md for full derivation.
 * ========================================================================= */
static const int8_t G3_SIGN[G3_DIM][G3_DIM] = {
    /* ia=0  (scalar, mask=0) */
    { 1,  1,  1,  1,  1,  1,  1,  1},
    /* ia=1  (e0, mask=1) */
    { 1,  1,  1,  1,  1,  1,  1,  1},
    /* ia=2  (e1, mask=2) */
    { 1, -1,  1, -1,  1, -1,  1, -1},
    /* ia=3  (e01, mask=3) */
    { 1, -1,  1, -1,  1, -1,  1, -1},
    /* ia=4  (e2, mask=4) */
    { 1, -1, -1,  1,  1, -1, -1,  1},
    /* ia=5  (e02, mask=5) */
    { 1, -1, -1,  1,  1, -1, -1,  1},
    /* ia=6  (e12, mask=6) */
    { 1,  1, -1, -1,  1,  1, -1, -1},
    /* ia=7  (e012, mask=7) */
    { 1,  1, -1, -1,  1,  1, -1, -1}
};

/* =========================================================================
 * FUNCTION PROTOTYPES
 * ========================================================================= */

/* Saturating FIX16 addition — implemented in qgpu_accel.cpp */
fix16_t fix16_add(fix16_t a, fix16_t b);

/* Saturating FIX16 subtraction */
fix16_t fix16_sub(fix16_t a, fix16_t b);

/* FIX16 Q1.14 multiply: result = (a * b) >> 14, saturated */
fix16_t fix16_mul(fix16_t a, fix16_t b);

/* Accumulate FIX16: result += a * b, keep 32-bit intermediate */
void    fix16_mac(fix32_t* acc, fix16_t a, fix16_t b);

/* Saturate 32-bit accumulator to FIX16 */
fix16_t fix16_saturate(fix32_t v);

/* G3 Geometric Product: C = A * B  (G(3,0,0)) */
void g3_geometric_product(const G3_mv A, const G3_mv B, G3_mv C);

/* G3 Outer Product: C = A ^ B */
void g3_outer_product(const G3_mv A, const G3_mv B, G3_mv C);

/* G3 Inner Product: C = A . B  (Hestenes convention) */
void g3_inner_product(const G3_mv A, const G3_mv B, G3_mv C);

/* Top-level HLS function — AXI4-Stream + AXI4-Lite interfaces */
void qgpu_accel(
    axis_t         &in_stream,   /* AXI4-Stream from DMA MM2S  */
    axis_t         &out_stream,  /* AXI4-Stream to   DMA S2MM  */
    volatile uint32_t *status,   /* AXI4-Lite: status register */
    volatile uint32_t *op_count  /* AXI4-Lite: ops completed   */
);

#endif /* QGPU_ACCEL_H */
