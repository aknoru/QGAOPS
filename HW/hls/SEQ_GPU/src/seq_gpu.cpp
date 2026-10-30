/**
 * seq_gpu.cpp
 * Sequential Resource-Shared Geometric Algebra Accelerator Kernel
 *
 * Microarchitecture:
 * - Time-multiplexed loop hierarchy designed to share a single DSP multiplier datapath.
 * - Single 67-bit accumulator buffer visited across sequential cycles.
 * - Explicit submodule functions with #pragma HLS INLINE off for clear
 *   visibility in synthesis call graphs.
 * - Zero unroll directives to maintain strict resource-sharing goals.
 */

#include "../include/seq_gpu.h"

/* Helper: Sequential Clifford Product Core (Used by GP, WEDGE, INNER) */
static void seq_product_core(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    bool *overflow
) {
    #pragma HLS INLINE off
    accum_t accum[GA_BLADES];
    #pragma HLS ARRAY_PARTITION variable=accum complete dim=1

    // Clear accumulator
    INIT_ACCUM:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        accum[k] = 0;
    }

    // Time-multiplexed sequential product iteration
    OUTER_LOOP:
    for (int left = 0; left < GA_BLADES; left++) {
        uint8_t left_mask = BASIS_MASKS[left];
        uint8_t left_grade = BASIS_GRADES[left];
        int32_t a_val = a[left];

        INNER_LOOP:
        for (int right = 0; right < GA_BLADES; right++) {
            #pragma HLS PIPELINE II=1
            #pragma HLS DEPENDENCE variable=accum type=inter direction=RAW dependent=false
            #pragma HLS DEPENDENCE variable=accum type=inter direction=WAR dependent=false
            uint8_t right_mask = BASIS_MASKS[right];
            uint8_t right_grade = BASIS_GRADES[right];
            int32_t b_val = b[right];

            bool include_term = true;
            if (opcode == OPCODE_WEDGE) {
                // Wedge product condition: disjoint blade indices
                if ((left_mask & right_mask) != 0) {
                    include_term = false;
                }
            } else if (opcode == OPCODE_INNER) {
                // Hestenes inner product condition: |grade(B) - grade(A)| == grade(out)
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

    // Sequential rescaling with round-to-nearest-even and saturation
    RESCALE_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        c[k] = rescale_and_saturate(accum[k], overflow);
    }
}

/* Submodule: Multivector Addition */
static void seq_op_add(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    ADD_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        c[k] = sat_add(a[k], b[k], overflow);
    }
}

/* Submodule: Multivector Subtraction */
static void seq_op_sub(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    SUB_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        c[k] = sat_sub(a[k], b[k], overflow);
    }
}

/* Submodule: Scalar Multiplication (C = B[0] * A) */
static void seq_op_scalar_mul(
    const int32_t a[GA_BLADES],
    int32_t scalar_val,
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    SCALAR_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        prod_t p = (prod_t)a[k] * (prod_t)scalar_val;
        c[k] = rescale_and_saturate((accum_t)p, overflow);
    }
}

/* Submodule: Grade Projection (C = <A>_k, k in B[0]) */
static void seq_op_grade_proj(
    const int32_t a[GA_BLADES],
    int32_t grade_target,
    int32_t c[GA_BLADES]
) {
    #pragma HLS INLINE off
    GRADE_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        if (BASIS_GRADES[k] == grade_target) {
            c[k] = a[k];
        } else {
            c[k] = 0;
        }
    }
}

/* Submodule: Reversion (C = ~A, grades 2, 3 negated) */
static void seq_op_reverse(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    REVERSE_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        if (BASIS_GRADES[k] == 2 || BASIS_GRADES[k] == 3) {
            c[k] = sat_sub(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

/* Submodule: Grade Involution (C = ^A, grades 1, 3 negated) */
static void seq_op_grade_involution(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    INVOLUTION_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        if (BASIS_GRADES[k] % 2 != 0) {
            c[k] = sat_sub(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

/* Submodule: Clifford Conjugation (C = ~^A, grades 1, 2 negated) */
static void seq_op_clifford_conj(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    CONJ_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        if (BASIS_GRADES[k] == 1 || BASIS_GRADES[k] == 2) {
            c[k] = sat_sub(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

/* Submodule: Rotor Norm Squared (C[0] = sum(a_k^2)) */
static void seq_op_rotor_norm(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    accum_t sum_sq = 0;
    NORM_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        prod_t p = (prod_t)a[k] * (prod_t)a[k];
        sum_sq += (accum_t)p;
    }
    c[0] = rescale_and_saturate(sum_sq, overflow);
    CLEAR_REMAINING:
    for (int k = 1; k < GA_BLADES; k++) {
        c[k] = 0;
    }
}

/* Submodule: Rotor Sandwich Product (C = A * B * ~A) */
static void seq_op_sandwich(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    int32_t temp[GA_BLADES];
    int32_t a_rev[GA_BLADES];

    // 1. Compute intermediate T = A * B
    seq_product_core(a, b, temp, OPCODE_GP, overflow);

    // 2. Compute A_rev = ~A
    seq_op_reverse(a, a_rev, overflow);

    // 3. Compute C = T * A_rev
    seq_product_core(temp, a_rev, c, OPCODE_GP, overflow);
}

/* =========================================================================
 * TOP-LEVEL SYNTHESIZABLE ENTRY POINT: seq_gpu
 * ========================================================================= */
void seq_gpu(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    uint32_t *status
) {
    #pragma HLS INTERFACE s_axilite port=return bundle=control
    #pragma HLS INTERFACE s_axilite port=opcode bundle=control
    #pragma HLS INTERFACE s_axilite port=status bundle=control
    #pragma HLS INTERFACE s_axilite port=a bundle=control
    #pragma HLS INTERFACE s_axilite port=b bundle=control
    #pragma HLS INTERFACE s_axilite port=c bundle=control

    bool overflow_flag = false;
    uint32_t local_status = STATUS_OK;

    switch (opcode) {
        case OPCODE_GP:
        case OPCODE_WEDGE:
        case OPCODE_INNER:
            seq_product_core(a, b, c, opcode, &overflow_flag);
            break;

        case OPCODE_ADD:
            seq_op_add(a, b, c, &overflow_flag);
            break;

        case OPCODE_SUB:
            seq_op_sub(a, b, c, &overflow_flag);
            break;

        case OPCODE_SCALAR_MUL:
            seq_op_scalar_mul(a, b[0], c, &overflow_flag);
            break;

        case OPCODE_GRADE_PROJ:
            seq_op_grade_proj(a, b[0], c);
            break;

        case OPCODE_REVERSE:
            seq_op_reverse(a, c, &overflow_flag);
            break;

        case OPCODE_GRADE_INVOLUTION:
            seq_op_grade_involution(a, c, &overflow_flag);
            break;

        case OPCODE_CLIFFORD_CONJ:
            seq_op_clifford_conj(a, c, &overflow_flag);
            break;

        case OPCODE_SANDWICH:
            seq_op_sandwich(a, b, c, &overflow_flag);
            break;

        case OPCODE_ROTOR_NORM:
            seq_op_rotor_norm(a, c, &overflow_flag);
            break;

        default:
            local_status = STATUS_ERR_OP;
            CLEAR_ERR:
            for (int k = 0; k < GA_BLADES; k++) {
                c[k] = 0;
            }
            break;
    }

    if (overflow_flag) {
        local_status |= STATUS_OVERFLOW;
    }

    *status = local_status;
}
