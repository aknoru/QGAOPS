#ifndef QGPU_FIXED_POINT_H
#define QGPU_FIXED_POINT_H

#include <stdint.h>
#include <stdbool.h>
#include "qgpu_types.h"

#if defined(__SYNTHESIS__) || defined(USE_XILINX_HLS)
    #include <ap_int.h>
    /* Signed 67-bit accumulator: Mathematically guarantees zero intermediate overflow
     * for sum of 8 products of signed 32-bit Q16.16 values:
     * Worst case: 8 * (+2^62) = +2^65 <= 2^66 - 1. */
    typedef ap_int<67> accum_t;
    typedef ap_int<64> prod_t;
    typedef ap_int<33> add_accum_t;
#else
    /* Host C++ simulation emulation types */
    typedef __int128_t accum_t;
    typedef int64_t prod_t;
    typedef int64_t add_accum_t;
#endif

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Rescale 67-bit accumulated product sum back to signed Q16.16 using exact Round-to-Nearest-Even,
 * with saturating clamp to [Q16_MIN, Q16_MAX] and sticky overflow tracking.
 *
 * @param sum_val        67-bit accumulated product sum (Q32.32 scaling)
 * @param overflow_flag  Pointer to sticky overflow boolean flag
 * @return               Saturated and rounded 32-bit signed Q16.16 result
 */
static inline int32_t rescale_and_saturate(accum_t sum_val, bool *overflow_flag) {
    /* Floor quotient q and remainder r in [0, 65535]:
     * sum_val = q * 65536 + r */
    accum_t q = sum_val >> 16;
    accum_t r = sum_val & 0xFFFF;
    accum_t rounded;

    if (r < 0x8000) {
        rounded = q;
    } else if (r > 0x8000) {
        rounded = q + 1;
    } else {
        /* Exact tie (0.500000...): round towards nearest even integer */
        rounded = q;
        if ((q & 1) != 0) {
            rounded = q + 1;
        }
    }

    const accum_t MAX_VAL = (accum_t)Q16_MAX;
    const accum_t MIN_VAL = (accum_t)Q16_MIN;

    if (rounded > MAX_VAL) {
        *overflow_flag = true;
        return (int32_t)Q16_MAX;
    } else if (rounded < MIN_VAL) {
        *overflow_flag = true;
        return (int32_t)Q16_MIN;
    } else {
        return (int32_t)rounded;
    }
}

/**
 * Saturated addition of two signed 32-bit Q16.16 integers.
 */
static inline int32_t sat_add(int32_t a, int32_t b, bool *overflow_flag) {
    add_accum_t sum = (add_accum_t)a + (add_accum_t)b;
    if (sum > (add_accum_t)Q16_MAX) {
        *overflow_flag = true;
        return (int32_t)Q16_MAX;
    } else if (sum < (add_accum_t)Q16_MIN) {
        *overflow_flag = true;
        return (int32_t)Q16_MIN;
    }
    return (int32_t)sum;
}

/**
 * Saturated subtraction of two signed 32-bit Q16.16 integers.
 */
static inline int32_t sat_sub(int32_t a, int32_t b, bool *overflow_flag) {
    add_accum_t diff = (add_accum_t)a - (add_accum_t)b;
    if (diff > (add_accum_t)Q16_MAX) {
        *overflow_flag = true;
        return (int32_t)Q16_MAX;
    } else if (diff < (add_accum_t)Q16_MIN) {
        *overflow_flag = true;
        return (int32_t)Q16_MIN;
    }
    return (int32_t)diff;
}

#ifdef __cplusplus
}
#endif

#endif /* QGPU_FIXED_POINT_H */
