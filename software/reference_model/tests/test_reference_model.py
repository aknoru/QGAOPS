import math
import random

import pytest

from software.reference_model.qgaops_reference.algebra import (
    BASIS_GRADES,
    BASIS_MASKS,
    Multivector,
    blade,
    rotor,
    scalar,
)
from software.reference_model.qgaops_reference.fixed_point import (
    FixedPointFormat,
    FixedPointMultivector,
)


def independent_sign(left: int, right: int) -> int:
    ordered_left = [index for index in range(3) if left & (1 << index)]
    ordered_right = [index for index in range(3) if right & (1 << index)]
    inversions = sum(a > b for a in ordered_left for b in ordered_right)
    return -1 if inversions % 2 else 1


def basis_expected(left_index, right_index, operation):
    left, right = BASIS_MASKS[left_index], BASIS_MASKS[right_index]
    if operation == "wedge" and left & right:
        return None
    output = left ^ right
    if operation == "inner" and (
        BASIS_GRADES[left_index] > BASIS_GRADES[right_index]
        or output.bit_count() != BASIS_GRADES[right_index] - BASIS_GRADES[left_index]
    ):
        return None
    return output, independent_sign(left, right)


@pytest.mark.parametrize("operation", ["geometric_product", "wedge", "hestenes_inner"])
def test_all_64_basis_pairs(operation):
    for left_index in range(8):
        for right_index in range(8):
            result = getattr(blade(left_index), operation)(blade(right_index))
            expected = basis_expected(
                left_index, right_index,
                {"geometric_product": "geometric", "wedge": "wedge", "hestenes_inner": "inner"}[operation],
            )
            expected_coefficients = [0.0] * 8
            if expected is not None:
                output_mask, sign = expected
                expected_coefficients[BASIS_MASKS.index(output_mask)] = float(sign)
            assert result.coefficients == tuple(expected_coefficients)


def test_basis_identities_and_involutions():
    assert blade("e1").geometric_product(blade("e1")) == scalar(1)
    assert blade("e1").geometric_product(blade("e2")) == blade("e12")
    assert blade("e2").geometric_product(blade("e1")) == blade("e12", -1)
    assert blade("e123").geometric_product(blade("e123")) == scalar(-1)
    for index in range(8):
        value = blade(index)
        assert value.reverse().reverse() == value
        assert value.grade_involution().grade_involution() == value
        assert value.clifford_conjugation().clifford_conjugation() == value


def test_bilinearity_associativity_and_grade_reconstruction():
    rng = random.Random(20261026)
    a = Multivector.from_coefficients(rng.randint(-3, 3) for _ in range(8))
    b = Multivector.from_coefficients(rng.randint(-3, 3) for _ in range(8))
    c = Multivector.from_coefficients(rng.randint(-3, 3) for _ in range(8))
    assert a.geometric_product(b + c) == a.geometric_product(b) + a.geometric_product(c)
    assert a.geometric_product(b).geometric_product(c) == a.geometric_product(b.geometric_product(c))
    reconstruction = Multivector.zero()
    for grade in range(4):
        reconstruction = reconstruction + a.grade_projection(grade)
    assert reconstruction == a


def test_input_validation():
    with pytest.raises(ValueError):
        Multivector.from_coefficients([0] * 7)
    with pytest.raises(ValueError):
        Multivector.from_coefficients([0] * 7 + [float("inf")])
    with pytest.raises(ValueError):
        blade("not-a-blade")
    with pytest.raises(ValueError):
        scalar(1).grade_projection(4)


def test_fixed_point_conversion_rounding_limits_and_overflow():
    fmt = FixedPointFormat()
    assert fmt.encode(0.5 / fmt.scale) == (0, False)
    assert fmt.encode(1.5 / fmt.scale) == (2, False)
    assert fmt.encode(-1.5 / fmt.scale) == (-2, False)
    assert fmt.encode(40000.0)[1]
    assert fmt.decode(fmt.minimum) == -32768.0
    assert fmt.decode(fmt.maximum) == pytest.approx(32767.99998474121)
    saturated = FixedPointMultivector.from_reals([40000.0] + [0.0] * 7)
    assert saturated.overflowed
    assert saturated.coefficients[0] == fmt.maximum


def test_fixed_point_all_basis_products_and_differential_checks():
    fmt = FixedPointFormat()
    for operation in ("geometric_product", "wedge", "hestenes_inner"):
        for left_index in range(8):
            for right_index in range(8):
                left = FixedPointMultivector.from_reals(
                    [1.0 if i == left_index else 0.0 for i in range(8)], fmt
                )
                right = FixedPointMultivector.from_reals(
                    [1.0 if i == right_index else 0.0 for i in range(8)], fmt
                )
                result = getattr(left, operation)(right)
                expected = basis_expected(
                    left_index, right_index,
                    {"geometric_product": "geometric", "wedge": "wedge", "hestenes_inner": "inner"}[operation],
                )
                expected_coefficients = [0] * 8
                if expected is not None:
                    output_mask, sign = expected
                    expected_coefficients[BASIS_MASKS.index(output_mask)] = sign * fmt.scale
                assert result.coefficients == tuple(expected_coefficients)


def test_fixed_point_intermediate_arithmetic_and_error_metrics():
    fmt = FixedPointFormat()
    a = FixedPointMultivector.from_reals([1.25] + [0.0] * 7, fmt)
    b = FixedPointMultivector.from_reals([2.5] + [0.0] * 7, fmt)
    result = a.geometric_product(b)
    assert result.to_reals()[0] == pytest.approx(3.125)
    assert not result.overflowed
    assert a.negated().to_reals()[0] == pytest.approx(-1.25)
    large = FixedPointMultivector([fmt.maximum] * 8, fmt)
    assert large.geometric_product(large).overflowed
    reference = 1.0 / 3.0
    quantized = fmt.decode(fmt.encode(reference)[0])
    assert abs(reference - quantized) <= 0.5 / fmt.scale


def test_multivector_norm_and_norm_squared():
    # Test blade norm
    mv = blade("e1", 3.0)
    assert mv.norm_squared() == pytest.approx(9.0)
    assert mv.norm() == pytest.approx(3.0)

    # Test 3D Euclidean vector norm (e1 + 2*e2 + 2*e3 -> len = 3)
    vec = blade("e1", 1.0) + blade("e2", 2.0) + blade("e3", 2.0)
    assert vec.norm_squared() == pytest.approx(9.0)
    assert vec.norm() == pytest.approx(3.0)

    # Test rotor norm (normalized rotor has norm 1.0)
    r = rotor([1.0, 0.0, 0.0], 0.785398)
    assert r.norm() == pytest.approx(1.0, abs=1e-5)


