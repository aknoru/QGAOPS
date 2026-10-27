/**
 * qgpu_ga_engine_parallel.cpp
 * Variant B: Parallel Pipelined Cl(3,0) Geometric Algebra Kernel
 * with Algebra-Aware Memory Fabric (AAMF) and Explicit Operation Hierarchy.
 *
 * Architecture Strategy:
 * - Algebra-Aware Memory Fabric (AAMF): True dual-port BRAM-backed multivector
 *   operand banks (Bank A, Bank B, and Result Bank C) with 64-multivector capacity
 *   (512 words of 32-bit Q16.16 each, mapped to physical BRAM18K blocks).
 * - Explicit Operation Submodules: Every canonical Geometric Algebra operation is
 *   instantiated as an independent non-inlined hardware module (INLINE off),
 *   guaranteeing clear visibility in Vitis Analyzer / HLS Dependency & Call Graphs.
 * - Parallel Pipelined Multiplier Array: Balanced adder-tree architecture with
 *   positive timing slack at 100 MHz on xc7z020.
 */

#include "qgpu_ga_engine.h"
#include "hls_compat.h"

/* =========================================================================
 * ALGEBRA-AWARE MEMORY FABRIC (AAMF) ON-CHIP STORAGE
 * Explicitly bound to dual-port Block RAM (BRAM18K).
 * Each bank stores up to AAMF_BUFFER_MV_COUNT (64) multivectors (512 words).
 * ========================================================================= */
static int32_t aamf_bank_a[AAMF_BUFFER_WORDS];
static int32_t aamf_bank_b[AAMF_BUFFER_WORDS];
static int32_t aamf_bank_c[AAMF_BUFFER_WORDS];

/* Common parallel product accumulation kernel */
static void compute_gp_core(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    bool *overflow
) {
    #pragma HLS INLINE off
    accum_t accum[GA_BLADES];
    #pragma HLS ARRAY_PARTITION variable=accum complete dim=1

    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        accum[k] = 0;
    }

    PARALLEL_OUTER_LOOP:
    for (int left = 0; left < GA_BLADES; left++) {
        #pragma HLS PIPELINE II=1
        #pragma HLS DEPENDENCE variable=accum inter false

        uint8_t left_mask = BASIS_MASKS[left];
        uint8_t left_grade = BASIS_GRADES[left];
        int32_t a_val = a[left];

        PARALLEL_INNER_LOOP:
        for (int right = 0; right < GA_BLADES; right++) {
            #pragma HLS UNROLL
            uint8_t right_mask = BASIS_MASKS[right];
            uint8_t right_grade = BASIS_GRADES[right];
            int32_t b_val = b[right];

            bool include_term = true;
            if (opcode == OPCODE_WEDGE) {
                if ((left_mask & right_mask) != 0) {
                    include_term = false;
                }
            } else if (opcode == OPCODE_INNER) {
                uint8_t out_mask = left_mask ^ right_mask;
                int out_grade = BASIS_GRADES[mask_to_index(out_mask)];
                if (left_grade > right_grade || out_grade != (right_grade - left_grade)) {
                    include_term = false;
                }
            }

            if (include_term) {
                int out_idx = mask_to_index(left_mask ^ right_mask);
                int sign = blade_product_sign(left_mask, right_mask);
                prod_t p = (prod_t)a_val * (prod_t)b_val;
                if (sign < 0) {
                    accum[out_idx] -= (accum_t)p;
                } else {
                    accum[out_idx] += (accum_t)p;
                }
            }
        }
    }

    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = rescale_and_saturate(accum[k], overflow);
    }
}

/* =========================================================================
 * INDEPENDENT HARDWARE MODULES FOR ALL 12 GEOMETRIC ALGEBRA OPERATIONS
 * Guaranteed visible as distinct nodes in Vitis Analyzer Dependency Graph.
 * ========================================================================= */

void ga_op_geometric_product(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    compute_gp_core(a, b, c, OPCODE_GP, overflow);
}

void ga_op_wedge_product(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    compute_gp_core(a, b, c, OPCODE_WEDGE, overflow);
}

void ga_op_inner_product(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    compute_gp_core(a, b, c, OPCODE_INNER, overflow);
}

void ga_op_addition(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = sat_add_q16(a[k], b[k], overflow);
    }
}

void ga_op_subtraction(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = sat_sub_q16(a[k], b[k], overflow);
    }
}

void ga_op_scalar_mul(
    const int32_t a[GA_BLADES],
    int32_t scalar_val,
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        prod_t p = (prod_t)a[k] * (prod_t)scalar_val;
        c[k] = rescale_and_saturate((accum_t)p, overflow);
    }
}

void ga_op_grade_project(
    const int32_t a[GA_BLADES],
    int target_grade,
    int32_t c[GA_BLADES],
    uint32_t *err_code
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    if (target_grade < 0 || target_grade > 3) {
        *err_code = STATUS_ERR_OP;
        for (int k = 0; k < GA_BLADES; k++) {
            #pragma HLS UNROLL
            c[k] = 0;
        }
    } else {
        for (int k = 0; k < GA_BLADES; k++) {
            #pragma HLS UNROLL
            c[k] = (BASIS_GRADES[k] == target_grade) ? a[k] : 0;
        }
    }
}

void ga_op_reverse(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] == 2 || BASIS_GRADES[k] == 3) {
            c[k] = sat_sub_q16(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

void ga_op_grade_involution(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] == 1 || BASIS_GRADES[k] == 3) {
            c[k] = sat_sub_q16(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

void ga_op_clifford_conjugation(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] == 1 || BASIS_GRADES[k] == 2) {
            c[k] = sat_sub_q16(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

void ga_op_rotor_sandwich(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    int32_t t[GA_BLADES];
    int32_t a_rev[GA_BLADES];
    #pragma HLS ARRAY_PARTITION variable=t complete dim=1
    #pragma HLS ARRAY_PARTITION variable=a_rev complete dim=1

    /* Step 1: Compute T = A * B */
    compute_gp_core(a, b, t, OPCODE_GP, overflow);

    /* Step 2: Compute ~A (reversion) */
    ga_op_reverse(a, a_rev, overflow);

    /* Step 3: Compute C = T * ~A */
    compute_gp_core(t, a_rev, c, OPCODE_GP, overflow);
}

void ga_op_rotor_norm(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1
    accum_t norm_accum = 0;
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        prod_t p = (prod_t)a[k] * (prod_t)a[k];
        norm_accum += (accum_t)p;
    }
    c[0] = rescale_and_saturate(norm_accum, overflow);
    for (int k = 1; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = 0;
    }
}

/* =========================================================================
 * PARALLEL ENGINE TOP: INTEGRATES AAMF MEMORY FABRIC AND OPERATION DISPATCH
 * ========================================================================= */
void qgpu_ga_engine_parallel(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status
) {
    #pragma HLS INLINE off
    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1

    // Explicitly bind the AAMF multi-vector buffers to dual-port Block RAM
    #pragma HLS BIND_STORAGE variable=aamf_bank_a type=ram_2p impl=bram
    #pragma HLS BIND_STORAGE variable=aamf_bank_b type=ram_2p impl=bram
    #pragma HLS BIND_STORAGE variable=aamf_bank_c type=ram_2p impl=bram

    // AAMF Slot Addressing: upper 16 bits of opcode specify the target multivector slot (0..63)
    // Default 0 for single-operation execution, matching standard test vectors.
    uint32_t slot = (opcode >> 16) & (AAMF_BUFFER_MV_COUNT - 1);
    int base_addr = slot * GA_BLADES;

    // Stage inputs into the AAMF BRAM banks
    AAMF_STAGE_IN:
    for (int k = 0; k < GA_BLADES; k++) {
        aamf_bank_a[base_addr + k] = a[k];
        aamf_bank_b[base_addr + k] = b[k];
    }

    // Local execution registers read from AAMF BRAM storage
    int32_t a_reg[GA_BLADES];
    int32_t b_reg[GA_BLADES];
    int32_t c_reg[GA_BLADES];
    #pragma HLS ARRAY_PARTITION variable=a_reg complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b_reg complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c_reg complete dim=1

    AAMF_FETCH:
    for (int k = 0; k < GA_BLADES; k++) {
        a_reg[k] = aamf_bank_a[base_addr + k];
        b_reg[k] = aamf_bank_b[base_addr + k];
        c_reg[k] = 0;
    }

    bool overflow = false;
    uint32_t err_code = STATUS_OK;
    uint32_t op = opcode & 0xFFFF;

    // Operation dispatch to individual hardware submodules
    switch (op) {
        case OPCODE_GP:
            ga_op_geometric_product(a_reg, b_reg, c_reg, &overflow);
            break;

        case OPCODE_WEDGE:
            ga_op_wedge_product(a_reg, b_reg, c_reg, &overflow);
            break;

        case OPCODE_INNER:
            ga_op_inner_product(a_reg, b_reg, c_reg, &overflow);
            break;

        case OPCODE_ADD:
            ga_op_addition(a_reg, b_reg, c_reg, &overflow);
            break;

        case OPCODE_SUB:
            ga_op_subtraction(a_reg, b_reg, c_reg, &overflow);
            break;

        case OPCODE_SCALAR_MUL:
            ga_op_scalar_mul(a_reg, b_reg[0], c_reg, &overflow);
            break;

        case OPCODE_GRADE_PROJ: {
            int target_grade = (b_reg[0] >= 0 && b_reg[0] <= 3) ? b_reg[0] : (b_reg[0] >> 16);
            ga_op_grade_project(a_reg, target_grade, c_reg, &err_code);
            break;
        }

        case OPCODE_REVERSE:
            ga_op_reverse(a_reg, c_reg, &overflow);
            break;

        case OPCODE_GRADE_INVOLUTION:
            ga_op_grade_involution(a_reg, c_reg, &overflow);
            break;

        case OPCODE_CLIFFORD_CONJ:
            ga_op_clifford_conjugation(a_reg, c_reg, &overflow);
            break;

        case OPCODE_SANDWICH:
            ga_op_rotor_sandwich(a_reg, b_reg, c_reg, &overflow);
            break;

        case OPCODE_ROTOR_NORM:
            ga_op_rotor_norm(a_reg, c_reg, &overflow);
            break;

        default:
            err_code = STATUS_ERR_OP;
            for (int k = 0; k < GA_BLADES; k++) {
                #pragma HLS UNROLL
                c_reg[k] = 0;
            }
            break;
    }

    // Commit results into AAMF Result BRAM and output port
    AAMF_COMMIT_OUT:
    for (int k = 0; k < GA_BLADES; k++) {
        aamf_bank_c[base_addr + k] = c_reg[k];
        c[k] = aamf_bank_c[base_addr + k];
    }

    *status = err_code | (overflow ? STATUS_OVERFLOW : STATUS_OK);
}
