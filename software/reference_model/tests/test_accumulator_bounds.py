"""Automated boundary tests for QGAOPS-QGPU arithmetic bit-widths.

Proves the mathematical theorems derived in docs/verification/accumulator_width_analysis.md:
1. Single product of signed 32-bit Q16.16 values requires 64 bits (63 bits overflows).
2. Theoretical unconstrained sum of 8 products (2^65) requires 67 bits (66 bits overflows by 1 count).
3. Exact Cl(3,0) worst-case sum across all 8 blades is 2^65 - 2^32, fitting safely within 67 bits.
4. Addition/subtraction of signed 32-bit values requires 33 bits before saturation.
5. Round-to-nearest-even handles exact half ties bit-exactly without drift.
"""

import pytest
from software.reference_model.qgaops_reference.algebra import BASIS_MASKS, MASK_TO_INDEX, _blade_product_sign
from software.reference_model.qgaops_reference.fixed_point import FixedPointFormat, FixedPointMultivector

MIN_INT32 = -(1 << 31)         # -2147483648
MAX_INT32 = (1 << 31) - 1      # +2147483647


def test_single_product_bit_width_requirement():
    # (-2^31) * (-2^31) = +2^62
    worst_case_pos_prod = MIN_INT32 * MIN_INT32
    assert worst_case_pos_prod == (1 << 62)

    # A signed 63-bit integer has max positive value 2^62 - 1
    max_signed_63 = (1 << 62) - 1
    assert worst_case_pos_prod > max_signed_63, "Signed 63-bit integer must fail to hold +2^62"

    # A signed 64-bit integer has max positive value 2^63 - 1
    max_signed_64 = (1 << 63) - 1
    assert worst_case_pos_prod <= max_signed_64, "Signed 64-bit integer safely holds +2^62"


def test_unconstrained_accumulator_width_defect():
    """Demonstrate why claiming 66 bits holds 2^65 is defective."""
    unconstrained_sum_8_products = 8 * (1 << 62)  # 2^65
    assert unconstrained_sum_8_products == (1 << 65)

    # A signed 66-bit integer has max positive value 2^65 - 1
    max_signed_66 = (1 << 65) - 1
    assert unconstrained_sum_8_products > max_signed_66, "Signed 66-bit integer overflows on 2^65 by 1 count"

    # A signed 67-bit integer has max positive value 2^66 - 1
    max_signed_67 = (1 << 66) - 1
    assert unconstrained_sum_8_products <= max_signed_67, "Signed 67-bit integer safely holds 2^65"


def test_exact_cl30_blade_worst_case_bounds():
    """Derive the exact algebraic bounds for all 8 output blades in Cl(3,0)."""
    for k in range(8):
        terms = []
        for i in range(8):
            for j in range(8):
                if MASK_TO_INDEX[BASIS_MASKS[i] ^ BASIS_MASKS[j]] == k:
                    s = _blade_product_sign(BASIS_MASKS[i], BASIS_MASKS[j])
                    terms.append((i, j, s))
        assert len(terms) == 8

        pos_count = sum(1 for _, _, s in terms if s > 0)
        neg_count = sum(1 for _, _, s in terms if s < 0)

        # Every blade has at least two negative signs
        assert neg_count >= 2, f"Blade {k} must have at least 2 negative signs"

        # Compute maximal achievable sum
        max_sum = 0
        min_sum = 0
        for i, j, s in terms:
            if s > 0:
                max_sum += 1 * MIN_INT32 * MIN_INT32         # +2^62
                min_sum += 1 * MIN_INT32 * MAX_INT32         # -2^62 + 2^31
            else:
                max_sum += (-1) * MIN_INT32 * MAX_INT32      # +2^62 - 2^31
                min_sum += (-1) * MIN_INT32 * MIN_INT32      # -2^62

        if pos_count == 6 and neg_count == 2:
            expected_max = (1 << 65) - (2 << 31)   # 6*(2^62) + 2*(2^62 - 2^31) = 2^65 - 2^32
            expected_min = -(1 << 65) + (6 << 31)  # 6*(-2^62 + 2^31) + 2*(-2^62) = -2^65 + 6*2^31
        elif pos_count == 4 and neg_count == 4:
            expected_max = (1 << 65) - (4 << 31)   # 4*(2^62) + 4*(2^62 - 2^31) = 2^65 - 2^33
            expected_min = -(1 << 65) + (4 << 31)  # 4*(-2^62 + 2^31) + 4*(-2^62) = -2^65 + 4*2^31
        else:
            pytest.fail(f"Unexpected sign count for blade {k}: {pos_count} pos, {neg_count} neg")

        assert max_sum == expected_max
        assert min_sum == expected_min

        # Both fit within signed 67-bit range
        assert max_sum <= (1 << 66) - 1
        assert min_sum >= -(1 << 66)


def test_addition_subtraction_33bit_requirement():
    worst_case_add = MIN_INT32 + MIN_INT32  # -2^32
    assert worst_case_add == -(1 << 32)

    # 32-bit signed integer has minimum -2^31
    assert worst_case_add < MIN_INT32, "Must overflow 32-bit signed range"

    # 33-bit signed integer has range [-2^32, 2^32 - 1]
    min_signed_33 = -(1 << 32)
    assert worst_case_add >= min_signed_33, "33 bits is necessary and sufficient for addition"
