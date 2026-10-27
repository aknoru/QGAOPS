#ifndef HLS_COMPAT_H
#define HLS_COMPAT_H

#include <stdint.h>
#include <stdbool.h>

#if defined(__SYNTHESIS__) || defined(USE_XILINX_HLS)
    #include <ap_int.h>
    /* Signed 67-bit accumulator: Mathematically guarantees zero overflow for 8 products
     * of signed 32-bit Q16.16 values: 8 * (+2^62) = 2^65 <= 2^66 - 1 */
    typedef ap_int<67> accum_t;
    typedef ap_int<64> prod_t;
    typedef ap_int<33> add_accum_t;
#else
    /* Portable 67-bit accumulator emulation for host C++ simulation (MinGW/GCC/Clang) */
    typedef __int128_t accum_t;
    typedef int64_t prod_t;
    typedef int64_t add_accum_t;
#endif

/* Canonical Cl(3,0) Basis Blade bitmasks:
 * 0: 1     (mask 0b000)
 * 1: e1    (mask 0b001)
 * 2: e2    (mask 0b010)
 * 3: e3    (mask 0b100)
 * 4: e12   (mask 0b011)
 * 5: e13   (mask 0b101)
 * 6: e23   (mask 0b110)
 * 7: e123  (mask 0b111)
 */
static const uint8_t BASIS_MASKS[8] = {0, 1, 2, 4, 3, 5, 6, 7};
static const uint8_t BASIS_GRADES[8] = {0, 1, 1, 1, 2, 2, 2, 3};

/* Map 3-bit mask to canonical index 0..7 */
static inline int mask_to_index(uint8_t mask) {
    switch (mask) {
        case 0: return 0;
        case 1: return 1;
        case 2: return 2;
        case 4: return 3;
        case 3: return 4;
        case 5: return 5;
        case 6: return 6;
        case 7: return 7;
        default: return 0;
    }
}

/* Euclidean Cl(3,0) blade product sign derivation */
static inline int blade_product_sign(uint8_t left_mask, uint8_t right_mask) {
    int swaps = 0;
    for (int left_idx = 0; left_idx < 3; left_idx++) {
        if (left_mask & (1 << left_idx)) {
            for (int right_idx = 0; right_idx < 3; right_idx++) {
                if ((right_mask & (1 << right_idx)) && (left_idx > right_idx)) {
                    swaps++;
                }
            }
        }
    }
    return (swaps % 2 == 1) ? -1 : 1;
}

/**
 * Rescale 67-bit accumulated product sum back to Q16.16 using exact Round-to-Nearest-Even,
 * with saturating clamp to [Q16_MIN, Q16_MAX] and sticky overflow tracking.
 */
static inline int32_t rescale_and_saturate(accum_t sum_val, bool *overflow_flag) {
    /* Compute floor quotient Q and remainder R: sum_val = Q * 65536 + R */
    accum_t q = sum_val >> 16;
    accum_t r = sum_val & 0xFFFF;
    accum_t rounded;

    if (r < 0x8000) {
        rounded = q;
    } else if (r > 0x8000) {
        rounded = q + 1;
    } else {
        /* Write this without ?: because ap_int operands of q and q+1 have
         * different inferred widths in Vitis HLS. */
        rounded = q;
        if ((q & 1) != 0) {
            rounded = q + 1;
        }
    }

    const accum_t MAX_VAL = 2147483647LL;
    const accum_t MIN_VAL = -2147483648LL;

    if (rounded > MAX_VAL) {
        *overflow_flag = true;
        return (int32_t)MAX_VAL;
    } else if (rounded < MIN_VAL) {
        *overflow_flag = true;
        return (int32_t)MIN_VAL;
    } else {
        return (int32_t)rounded;
    }
}

/**
 * Saturating addition for two Q16.16 integers with sticky overflow tracking.
 */
static inline int32_t sat_add_q16(int32_t a, int32_t b, bool *overflow_flag) {
    add_accum_t sum = (add_accum_t)a + (add_accum_t)b;
    const add_accum_t MAX_VAL = 2147483647LL;
    const add_accum_t MIN_VAL = -2147483648LL;

    if (sum > MAX_VAL) {
        *overflow_flag = true;
        return (int32_t)MAX_VAL;
    } else if (sum < MIN_VAL) {
        *overflow_flag = true;
        return (int32_t)MIN_VAL;
    } else {
        return (int32_t)sum;
    }
}

/**
 * Saturating subtraction for two Q16.16 integers with sticky overflow tracking.
 */
static inline int32_t sat_sub_q16(int32_t a, int32_t b, bool *overflow_flag) {
    add_accum_t diff = (add_accum_t)a - (add_accum_t)b;
    const add_accum_t MAX_VAL = 2147483647LL;
    const add_accum_t MIN_VAL = -2147483648LL;

    if (diff > MAX_VAL) {
        *overflow_flag = true;
        return (int32_t)MAX_VAL;
    } else if (diff < MIN_VAL) {
        *overflow_flag = true;
        return (int32_t)MIN_VAL;
    } else {
        return (int32_t)diff;
    }
}

#endif /* HLS_COMPAT_H */
