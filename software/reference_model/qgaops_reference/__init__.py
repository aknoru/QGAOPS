"""Independent floating-point and fixed-point Cl(3,0) reference models."""

from .algebra import (
    BASIS_NAMES,
    BASIS_MASKS,
    BASIS_GRADES,
    Multivector,
    blade,
    scalar,
)
from .fixed_point import FixedPointFormat, FixedPointMultivector

__all__ = [
    "BASIS_NAMES",
    "BASIS_MASKS",
    "BASIS_GRADES",
    "Multivector",
    "blade",
    "scalar",
    "FixedPointFormat",
    "FixedPointMultivector",
]
