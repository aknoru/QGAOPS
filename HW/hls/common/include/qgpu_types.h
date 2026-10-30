#ifndef QGPU_TYPES_H
#define QGPU_TYPES_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* =========================================================================
 * CLIFFORD GEOMETRIC ALGEBRA Cl(3,0) CONSTANTS
 * ========================================================================= */
#define GA_BLADES 8

/* Canonical Euclidean Cl(3,0) Basis Blade Bitmasks:
 * Index 0: 1     (mask 0b000 = 0) - Grade 0
 * Index 1: e1    (mask 0b001 = 1) - Grade 1
 * Index 2: e2    (mask 0b010 = 2) - Grade 1
 * Index 3: e3    (mask 0b100 = 4) - Grade 1
 * Index 4: e12   (mask 0b011 = 3) - Grade 2
 * Index 5: e13   (mask 0b101 = 5) - Grade 2
 * Index 6: e23   (mask 0b110 = 6) - Grade 2
 * Index 7: e123  (mask 0b111 = 7) - Grade 3
 */
static const uint8_t BASIS_MASKS[GA_BLADES]  = {0, 1, 2, 4, 3, 5, 6, 7};
static const uint8_t BASIS_GRADES[GA_BLADES] = {0, 1, 1, 1, 2, 2, 2, 3};

/* Map 3-bit blade mask to canonical index 0..7 */
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

/* Euclidean Cl(3,0) blade product sign derivation:
 * Counts transpositions of anti-commuting orthogonal vector basis elements */
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

/* =========================================================================
 * SIGNED Q16.16 BOUNDS AND METRIC CONSTANTS
 * ========================================================================= */
#define Q16_SCALE  65536LL
#define Q16_MAX    2147483647LL
#define Q16_MIN    (-2147483648LL)

#ifdef __cplusplus
}
#endif

#endif /* QGPU_TYPES_H */
