"""Separate integer-arithmetic Q16.16 Cl(3,0) reference implementation."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN, localcontext
from math import isfinite
from numbers import Real
from typing import Iterable

from .algebra import BASIS_GRADES, BASIS_MASKS, MASK_TO_INDEX, _blade_product_sign


@dataclass(frozen=True)
class FixedPointFormat:
    width: int = 32
    fractional_bits: int = 16

    @property
    def scale(self) -> int:
        return 1 << self.fractional_bits

    @property
    def minimum(self) -> int:
        return -(1 << (self.width - 1))

    @property
    def maximum(self) -> int:
        return (1 << (self.width - 1)) - 1

    def encode(self, value: Real) -> tuple[int, bool]:
        if not isinstance(value, Real) or isinstance(value, bool) or not isfinite(float(value)):
            raise TypeError("fixed-point input must be a finite real number")
        with localcontext() as context:
            context.prec = 80
            scaled = Decimal(str(value)) * Decimal(self.scale)
            raw = int(scaled.to_integral_value(rounding=ROUND_HALF_EVEN))
        return self._saturate(raw)

    def _saturate(self, raw: int) -> tuple[int, bool]:
        if raw < self.minimum:
            return self.minimum, True
        if raw > self.maximum:
            return self.maximum, True
        return raw, False

    def decode(self, raw: int) -> float:
        if not isinstance(raw, int) or isinstance(raw, bool):
            raise TypeError("encoded coefficient must be an integer")
        return raw / self.scale

    def rescale_product_sum(self, raw_sum: int) -> tuple[int, bool]:
        """Round an accumulated raw-product sum back to coefficient units."""
        with localcontext() as context:
            context.prec = 100
            scaled = (Decimal(raw_sum) / Decimal(self.scale)).to_integral_value(
                rounding=ROUND_HALF_EVEN
            )
        return self._saturate(int(scaled))


class FixedPointMultivector:
    """Q16.16 multivector with explicit saturation reporting."""

    def __init__(
        self,
        coefficients: Iterable[int],
        fmt: FixedPointFormat | None = None,
        overflowed: bool = False,
    ) -> None:
        values = tuple(coefficients)
        if len(values) != 8:
            raise ValueError("a fixed-point multivector requires exactly 8 coefficients")
        if any(not isinstance(value, int) or isinstance(value, bool) for value in values):
            raise TypeError("fixed-point coefficients must be integers")
        self.format = fmt or FixedPointFormat()
        if any(value < self.format.minimum or value > self.format.maximum for value in values):
            raise ValueError("fixed-point coefficients must fit the configured format")
        self.coefficients = values
        self.overflowed = bool(overflowed)

    @classmethod
    def from_reals(cls, coefficients: Iterable[Real], fmt: FixedPointFormat | None = None):
        selected = fmt or FixedPointFormat()
        encoded = [selected.encode(value) for value in coefficients]
        return cls([value for value, _ in encoded], selected, any(flag for _, flag in encoded))

    def to_reals(self) -> tuple[float, ...]:
        return tuple(self.format.decode(value) for value in self.coefficients)

    def _check_compatible(self, other: "FixedPointMultivector") -> None:
        if not isinstance(other, FixedPointMultivector):
            raise TypeError("operation requires a FixedPointMultivector")
        if self.format != other.format:
            raise ValueError("fixed-point formats must match")

    def _from_raw(self, values: list[int], overflowed: bool):
        narrowed = [self.format._saturate(value) for value in values]
        return FixedPointMultivector(
            [value for value, _ in narrowed],
            self.format,
            overflowed or any(flag for _, flag in narrowed),
        )

    def __add__(self, other):
        self._check_compatible(other)
        return self._from_raw(
            [a + b for a, b in zip(self.coefficients, other.coefficients)],
            self.overflowed or other.overflowed,
        )

    def __sub__(self, other):
        self._check_compatible(other)
        return self._from_raw(
            [a - b for a, b in zip(self.coefficients, other.coefficients)],
            self.overflowed or other.overflowed,
        )

    def negated(self):
        return self._from_raw([-value for value in self.coefficients], self.overflowed)

    def scale(self, value: Real):
        raw_scalar, conversion_overflow = self.format.encode(value)
        return self._product(other_raw=[raw_scalar], scalar_mode=True,
                             inherited_overflow=self.overflowed or conversion_overflow)

    def _product(self, other_raw, scalar_mode=False, inherited_overflow=False):
        if scalar_mode:
            raw_sum = [coefficient * other_raw[0] for coefficient in self.coefficients]
        else:
            raw_sum = [0] * 8
            for left_index, left_mask in enumerate(BASIS_MASKS):
                for right_index, right_mask in enumerate(BASIS_MASKS):
                    output_index = MASK_TO_INDEX[left_mask ^ right_mask]
                    raw_sum[output_index] += (
                        _blade_product_sign(left_mask, right_mask)
                        * self.coefficients[left_index] * other_raw[right_index]
                    )
        narrowed = [self.format.rescale_product_sum(value) for value in raw_sum]
        return FixedPointMultivector(
            [value for value, _ in narrowed],
            self.format,
            inherited_overflow or any(flag for _, flag in narrowed),
        )

    def geometric_product(self, other):
        self._check_compatible(other)
        return self._product(other.coefficients, inherited_overflow=self.overflowed or other.overflowed)

    def wedge(self, other):
        self._check_compatible(other)
        raw_sum = [0] * 8
        for left_index, left_mask in enumerate(BASIS_MASKS):
            for right_index, right_mask in enumerate(BASIS_MASKS):
                if left_mask & right_mask:
                    continue
                raw_sum[MASK_TO_INDEX[left_mask ^ right_mask]] += (
                    _blade_product_sign(left_mask, right_mask)
                    * self.coefficients[left_index] * other.coefficients[right_index]
                )
        narrowed = [self.format.rescale_product_sum(value) for value in raw_sum]
        return FixedPointMultivector(
            [value for value, _ in narrowed],
            self.format,
            self.overflowed or other.overflowed or any(flag for _, flag in narrowed),
        )

    def hestenes_inner(self, other):
        self._check_compatible(other)
        raw_sum = [0] * 8
        for left_index, left_mask in enumerate(BASIS_MASKS):
            left_grade = BASIS_GRADES[left_index]
            for right_index, right_mask in enumerate(BASIS_MASKS):
                right_grade = BASIS_GRADES[right_index]
                output_mask = left_mask ^ right_mask
                if left_grade > right_grade or output_mask.bit_count() != right_grade - left_grade:
                    continue
                raw_sum[MASK_TO_INDEX[output_mask]] += (
                    _blade_product_sign(left_mask, right_mask)
                    * self.coefficients[left_index] * other.coefficients[right_index]
                )
        narrowed = [self.format.rescale_product_sum(value) for value in raw_sum]
        return FixedPointMultivector(
            [value for value, _ in narrowed],
            self.format,
            self.overflowed or other.overflowed or any(flag for _, flag in narrowed),
        )

    def grade_projection(self, grade: int):
        if not isinstance(grade, int) or isinstance(grade, bool) or not 0 <= grade <= 3:
            raise ValueError("grade must be an integer in the range 0..3")
        return FixedPointMultivector(
            [value if BASIS_GRADES[index] == grade else 0 for index, value in enumerate(self.coefficients)],
            self.format,
            self.overflowed,
        )

    def _sign_by_grade(self, predicate):
        return self._from_raw(
            [value if predicate(grade) else -value for value, grade in zip(self.coefficients, BASIS_GRADES)],
            self.overflowed,
        )

    def reverse(self):
        return self._sign_by_grade(lambda grade: grade in (0, 1))

    def grade_involution(self):
        return self._sign_by_grade(lambda grade: grade % 2 == 0)

    def clifford_conjugation(self):
        return self.reverse().grade_involution()

    def norm_squared(self):
        """Compute scalar norm squared: sum(a_k^2), rounded and saturated back to Q16.16."""
        raw_sum = sum(val * val for val in self.coefficients)
        narrowed, ovf = self.format.rescale_product_sum(raw_sum)
        return FixedPointMultivector([narrowed] + [0] * 7, self.format, self.overflowed or ovf)

    def scale_multivector(self, other: "FixedPointMultivector"):
        """Scale by scalar component other.coefficients[0]."""
        self._check_compatible(other)
        raw_scalar = other.coefficients[0]
        return self._product(other_raw=[raw_scalar], scalar_mode=True, inherited_overflow=self.overflowed or other.overflowed)

    def sandwich(self, target: "FixedPointMultivector"):
        """Compute rotor sandwich transformation: R * target * ~R."""
        self._check_compatible(target)
        return self.geometric_product(target).geometric_product(self.reverse())
