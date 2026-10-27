"""Readable floating-point Cl(3,0) reference implementation."""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, isfinite, sin, sqrt
from numbers import Real
from typing import Iterable, Sequence

BASIS_NAMES = ("1", "e1", "e2", "e3", "e12", "e13", "e23", "e123")
BASIS_MASKS = (0, 1, 2, 4, 3, 5, 6, 7)
MASK_TO_INDEX = {mask: index for index, mask in enumerate(BASIS_MASKS)}
BASIS_GRADES = tuple(mask.bit_count() for mask in BASIS_MASKS)


def _validate_grade(grade: int) -> None:
    if not isinstance(grade, int) or isinstance(grade, bool) or not 0 <= grade <= 3:
        raise ValueError("grade must be an integer in the range 0..3")


def _blade_product_sign(left_mask: int, right_mask: int) -> int:
    """Return the Euclidean sign for the ordered basis-vector convention."""
    swaps = 0
    for left_index in range(3):
        if left_mask & (1 << left_index):
            for right_index in range(3):
                if right_mask & (1 << right_index) and left_index > right_index:
                    swaps += 1
    return -1 if swaps % 2 else 1


def _coerce_coefficients(coefficients: Iterable[Real]) -> tuple[float, ...]:
    values = tuple(coefficients)
    if len(values) != 8:
        raise ValueError("a multivector requires exactly 8 coefficients")
    result = tuple(float(value) for value in values)
    if not all(isfinite(value) for value in result):
        raise ValueError("multivector coefficients must be finite")
    return result


@dataclass(frozen=True)
class Multivector:
    """Eight-coefficient floating-point multivector in the fixed basis order."""

    coefficients: tuple[float, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "coefficients", _coerce_coefficients(self.coefficients))

    @classmethod
    def zero(cls) -> "Multivector":
        return cls((0.0,) * 8)

    @classmethod
    def from_coefficients(cls, coefficients: Iterable[Real]) -> "Multivector":
        return cls(tuple(coefficients))

    def __getitem__(self, index: int) -> float:
        return self.coefficients[index]

    def __add__(self, other: "Multivector") -> "Multivector":
        _require_multivector(other)
        return Multivector(tuple(a + b for a, b in zip(self.coefficients, other.coefficients)))

    def __sub__(self, other: "Multivector") -> "Multivector":
        _require_multivector(other)
        return Multivector(tuple(a - b for a, b in zip(self.coefficients, other.coefficients)))

    def __neg__(self) -> "Multivector":
        return Multivector(tuple(-value for value in self.coefficients))

    def scale(self, value: Real) -> "Multivector":
        if not isinstance(value, Real) or isinstance(value, bool) or not isfinite(float(value)):
            raise TypeError("scale must be a finite real number")
        return Multivector(tuple(value * coefficient for coefficient in self.coefficients))

    def geometric_product(self, other: "Multivector") -> "Multivector":
        _require_multivector(other)
        result = [0.0] * 8
        for left_index, left_mask in enumerate(BASIS_MASKS):
            for right_index, right_mask in enumerate(BASIS_MASKS):
                output_index = MASK_TO_INDEX[left_mask ^ right_mask]
                sign = _blade_product_sign(left_mask, right_mask)
                result[output_index] += sign * self[left_index] * other[right_index]
        return Multivector(tuple(result))

    def wedge(self, other: "Multivector") -> "Multivector":
        _require_multivector(other)
        result = [0.0] * 8
        for left_index, left_mask in enumerate(BASIS_MASKS):
            for right_index, right_mask in enumerate(BASIS_MASKS):
                if left_mask & right_mask:
                    continue
                output_index = MASK_TO_INDEX[left_mask ^ right_mask]
                sign = _blade_product_sign(left_mask, right_mask)
                result[output_index] += sign * self[left_index] * other[right_index]
        return Multivector(tuple(result))

    def hestenes_inner(self, other: "Multivector") -> "Multivector":
        _require_multivector(other)
        result = [0.0] * 8
        for left_index, left_mask in enumerate(BASIS_MASKS):
            left_grade = BASIS_GRADES[left_index]
            for right_index, right_mask in enumerate(BASIS_MASKS):
                right_grade = BASIS_GRADES[right_index]
                if left_grade > right_grade:
                    continue
                output_mask = left_mask ^ right_mask
                if output_mask.bit_count() != right_grade - left_grade:
                    continue
                output_index = MASK_TO_INDEX[output_mask]
                sign = _blade_product_sign(left_mask, right_mask)
                result[output_index] += sign * self[left_index] * other[right_index]
        return Multivector(tuple(result))

    def grade_projection(self, grade: int) -> "Multivector":
        _validate_grade(grade)
        return Multivector(tuple(value if BASIS_GRADES[index] == grade else 0.0
                                 for index, value in enumerate(self.coefficients)))

    def reverse(self) -> "Multivector":
        return Multivector(tuple(
            value * (-1 if grade in (2, 3) else 1)
            for value, grade in zip(self.coefficients, BASIS_GRADES)
        ))

    def grade_involution(self) -> "Multivector":
        return Multivector(tuple(
            value * (-1 if grade % 2 else 1)
            for value, grade in zip(self.coefficients, BASIS_GRADES)
        ))

    def clifford_conjugation(self) -> "Multivector":
        return self.reverse().grade_involution()

    def norm_squared(self) -> float:
        """Return scalar component of A * ~A."""
        return self.geometric_product(self.reverse())[0]

    def norm(self) -> float:
        val = self.norm_squared()
        return sqrt(max(0.0, val)) if val >= 0 else 0.0

    def sandwich(self, target: "Multivector") -> "Multivector":
        """Compute rotor sandwich transformation: R * target * ~R."""
        _require_multivector(target)
        return self.geometric_product(target).geometric_product(self.reverse())


def _require_multivector(value: object) -> None:
    if not isinstance(value, Multivector):
        raise TypeError("operation requires a Multivector")


def scalar(value: Real) -> Multivector:
    if not isinstance(value, Real) or isinstance(value, bool) or not isfinite(float(value)):
        raise TypeError("scalar must be a finite real number")
    return Multivector((float(value),) + (0.0,) * 7)


def blade(name_or_index: str | int, coefficient: Real = 1.0) -> Multivector:
    if isinstance(name_or_index, int) and not isinstance(name_or_index, bool):
        index = name_or_index
    elif isinstance(name_or_index, str):
        try:
            index = BASIS_NAMES.index(name_or_index)
        except ValueError as exc:
            raise ValueError(f"unknown basis blade: {name_or_index}") from exc
    else:
        raise TypeError("blade must be selected by basis name or index")
    if not 0 <= index < 8:
        raise ValueError("basis index must be in the range 0..7")
    return Multivector((float(coefficient) if i == index else 0.0 for i in range(8)))


def rotor(bivector_coeffs: Sequence[Real], theta: Real) -> Multivector:
    """Construct a unit rotor R = cos(theta/2) - sin(theta/2) * B_hat in Cl(3,0).
    
    bivector_coeffs: components for [e12, e13, e23] (blades 4, 5, 6).
    """
    b12, b13, b23 = float(bivector_coeffs[0]), float(bivector_coeffs[1]), float(bivector_coeffs[2])
    norm_b = sqrt(b12 * b12 + b13 * b13 + b23 * b23)
    half_theta = float(theta) / 2.0
    c = cos(half_theta)
    s = sin(half_theta)
    
    coeffs = [0.0] * 8
    coeffs[0] = c
    if norm_b > 1e-12:
        coeffs[4] = -s * (b12 / norm_b)  # e12
        coeffs[5] = -s * (b13 / norm_b)  # e13
        coeffs[6] = -s * (b23 / norm_b)  # e23
    return Multivector(tuple(coeffs))
