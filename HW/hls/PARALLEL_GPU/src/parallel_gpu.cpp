/**
 * parallel_gpu.cpp
 * Parallel Pipelined Geometric Algebra Accelerator Kernel
 *
 * Microarchitecture:
 * - Fully unrolled 8-blade parallel computation with balanced tree reduction.
 * - Array partitioning (#pragma HLS ARRAY_PARTITION complete) on all operand
 *   and accumulator registers, eliminating memory port bottlenecks.
 * - Loop pipelining (#pragma HLS PIPELINE II=1) across arithmetic stages.
 * - Explicit trade-off: Trades higher DSP48 and LUT logic for drastically
 *   reduced cycle latency (~8-12 cycles for GP vs ~70 cycles in SEQ_GPU).
 */

#include "../include/parallel_gpu.h"

/* Helper: Parallel Clifford Product Core (Used by GP, WEDGE, INNER) */
static void parallel_product_core(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    uint32_t opcode,
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1

    // Parallel Blade Trees: Computes all 8 output blades concurrently
    PARALLEL_BLADE_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        uint8_t out_mask = BASIS_MASKS[k];
        accum_t blade_acc = 0;

        // Summation Tree: 8 pairwise product terms per blade
        PARALLEL_SUM_TREE:
        for (int left = 0; left < GA_BLADES; left++) {
            #pragma HLS UNROLL
            uint8_t left_mask = BASIS_MASKS[left];
            uint8_t left_grade = BASIS_GRADES[left];
            uint8_t right_mask = out_mask ^ left_mask;
            int right = mask_to_index(right_mask);
            uint8_t right_grade = BASIS_GRADES[right];

            bool include_term = true;
            if (opcode == OPCODE_WEDGE) {
                if ((left_mask & right_mask) != 0) {
                    include_term = false;
                }
            } else if (opcode == OPCODE_INNER) {
                int out_grade = BASIS_GRADES[k];
                if (left_grade > right_grade || out_grade != (right_grade - left_grade)) {
                    include_term = false;
                }
            }

            if (include_term) {
                int sign = blade_product_sign(left_mask, right_mask);
                prod_t p = (prod_t)a[left] * (prod_t)b[right];
                if (sign < 0) {
                    blade_acc -= (accum_t)p;
                } else {
                    blade_acc += (accum_t)p;
                }
            }
        }

        c[k] = rescale_and_saturate(blade_acc, overflow);
    }
}

/* Submodule: Parallel Multivector Addition */
static void parallel_op_add(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_ADD_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = sat_add(a[k], b[k], overflow);
    }
}

/* Submodule: Parallel Multivector Subtraction */
static void parallel_op_sub(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_SUB_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = sat_sub(a[k], b[k], overflow);
    }
}

/* Submodule: Parallel Scalar Multiplication (C = B[0] * A) */
static void parallel_op_scalar_mul(
    const int32_t a[GA_BLADES],
    int32_t scalar_val,
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_SCALAR_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        prod_t p = (prod_t)a[k] * (prod_t)scalar_val;
        c[k] = rescale_and_saturate((accum_t)p, overflow);
    }
}

/* Submodule: Parallel Grade Projection (C = <A>_k, k in B[0]) */
static void parallel_op_grade_proj(
    const int32_t a[GA_BLADES],
    int32_t grade_target,
    int32_t c[GA_BLADES]
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_GRADE_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] == grade_target) {
            c[k] = a[k];
        } else {
            c[k] = 0;
        }
    }
}

/* Submodule: Parallel Reversion (C = ~A, grades 2, 3 negated) */
static void parallel_op_reverse(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_REVERSE_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] == 2 || BASIS_GRADES[k] == 3) {
            c[k] = sat_sub(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

/* Submodule: Parallel Grade Involution (C = ^A, grades 1, 3 negated) */
static void parallel_op_grade_involution(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_INVOLUTION_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] % 2 != 0) {
            c[k] = sat_sub(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

/* Submodule: Parallel Clifford Conjugation (C = ~^A, grades 1, 2 negated) */
static void parallel_op_clifford_conj(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    PARALLEL_CONJ_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        if (BASIS_GRADES[k] == 1 || BASIS_GRADES[k] == 2) {
            c[k] = sat_sub(0, a[k], overflow);
        } else {
            c[k] = a[k];
        }
    }
}

/* Submodule: Parallel Rotor Norm Squared (C[0] = sum(a_k^2)) */
static void parallel_op_rotor_norm(
    const int32_t a[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS PIPELINE II=1
    accum_t sum_sq = 0;
    PARALLEL_NORM_LOOP:
    for (int k = 0; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        prod_t p = (prod_t)a[k] * (prod_t)a[k];
        sum_sq += (accum_t)p;
    }
    c[0] = rescale_and_saturate(sum_sq, overflow);
    PARALLEL_CLEAR_NORM:
    for (int k = 1; k < GA_BLADES; k++) {
        #pragma HLS UNROLL
        c[k] = 0;
    }
}

/* Submodule: Parallel Rotor Sandwich Product (C = A * B * ~A) */
static void parallel_op_sandwich(
    const int32_t a[GA_BLADES],
    const int32_t b[GA_BLADES],
    int32_t c[GA_BLADES],
    bool *overflow
) {
    #pragma HLS INLINE off
    #pragma HLS DATAFLOW
    int32_t temp[GA_BLADES];
    int32_t a_rev[GA_BLADES];
    #pragma HLS ARRAY_PARTITION variable=temp complete dim=1
    #pragma HLS ARRAY_PARTITION variable=a_rev complete dim=1

    // Stage 1: T = A * B and A_rev = ~A executed concurrently
    parallel_product_core(a, b, temp, OPCODE_GP, overflow);
    parallel_op_reverse(a, a_rev, overflow);

    // Stage 2: C = T * A_rev
    parallel_product_core(temp, a_rev, c, OPCODE_GP, overflow);
}

/* =========================================================================
 * TOP-LEVEL SYNTHESIZABLE ENTRY POINT: parallel_gpu
 * ========================================================================= */
void parallel_gpu(
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

    #pragma HLS ARRAY_PARTITION variable=a complete dim=1
    #pragma HLS ARRAY_PARTITION variable=b complete dim=1
    #pragma HLS ARRAY_PARTITION variable=c complete dim=1

    bool overflow_flag = false;
    uint32_t local_status = STATUS_OK;

    switch (opcode) {
        case OPCODE_GP:
        case OPCODE_WEDGE:
        case OPCODE_INNER:
            parallel_product_core(a, b, c, opcode, &overflow_flag);
            break;

        case OPCODE_ADD:
            parallel_op_add(a, b, c, &overflow_flag);
            break;

        case OPCODE_SUB:
            parallel_op_sub(a, b, c, &overflow_flag);
            break;

        case OPCODE_SCALAR_MUL:
            parallel_op_scalar_mul(a, b[0], c, &overflow_flag);
            break;

        case OPCODE_GRADE_PROJ:
            parallel_op_grade_proj(a, b[0], c);
            break;

        case OPCODE_REVERSE:
            parallel_op_reverse(a, c, &overflow_flag);
            break;

        case OPCODE_GRADE_INVOLUTION:
            parallel_op_grade_involution(a, c, &overflow_flag);
            break;

        case OPCODE_CLIFFORD_CONJ:
            parallel_op_clifford_conj(a, c, &overflow_flag);
            break;

        case OPCODE_SANDWICH:
            parallel_op_sandwich(a, b, c, &overflow_flag);
            break;

        case OPCODE_ROTOR_NORM:
            parallel_op_rotor_norm(a, c, &overflow_flag);
            break;

        default:
            local_status = STATUS_ERR_OP;
            PARALLEL_CLEAR_ERR:
            for (int k = 0; k < GA_BLADES; k++) {
                #pragma HLS UNROLL
                c[k] = 0;
            }
            break;
    }

    if (overflow_flag) {
        local_status |= STATUS_OVERFLOW;
    }

    *status = local_status;
}
