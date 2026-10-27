"""
LIVE HAND GA ENGINE — ga/multivector.py
Full Multivector type for G(3,0,0).

[IMPLEMENTED] 8-element coefficient array indexed by basis mask.
[ARCH]        Coefficient packing matches QGAOPS dense-representation format.

G3 Basis ordering (by mask):
    Index 0: mask=0  -> scalar   '1'
    Index 1: mask=1  -> e0
    Index 2: mask=2  -> e1
    Index 3: mask=3  -> e01
    Index 4: mask=4  -> e2
    Index 5: mask=5  -> e02
    Index 6: mask=6  -> e12
    Index 7: mask=7  -> e012

This is the canonical bitmask ordering used throughout the engine.
"""
from __future__ import annotations

import numpy as np
from typing import Dict, List, Optional, Union

from .basis import (
    G3_BASIS, G3_MASK_TO_INDEX, basis_name, grade, BasisElement
)

# Number of basis elements in G3
G3_DIM = 8


class Multivector:
    """A multivector in G(3,0,0).

    Stores 8 float32 coefficients ordered by bitmask index (0-7).

    Usage:
        Multivector.vector(1.0, 2.0, 3.0)     -> 1*e0 + 2*e1 + 3*e2
        Multivector.scalar(5.0)               -> 5.0
        Multivector.from_dict({1: 1.0, 2: 2.0}) -> 1*e0 + 2*e1
    """

    __slots__ = ("_coeffs",)

    def __init__(self, coeffs: Optional[np.ndarray] = None) -> None:
        if coeffs is None:
            self._coeffs = np.zeros(G3_DIM, dtype=np.float32)
        else:
            arr = np.asarray(coeffs, dtype=np.float32)
            if arr.shape != (G3_DIM,):
                raise ValueError(
                    f"Coefficients must have shape ({G3_DIM},), got {arr.shape}"
                )
            self._coeffs = arr.copy()

    # ------------------------------------------------------------------
    # Factory constructors
    # ------------------------------------------------------------------

    @classmethod
    def scalar(cls, s: float) -> "Multivector":
        """Create a pure scalar multivector."""
        c = np.zeros(G3_DIM, dtype=np.float32)
        c[0] = float(s)
        return cls(c)

    @classmethod
    def vector(cls, x: float, y: float, z: float) -> "Multivector":
        """Create a pure grade-1 vector: x*e0 + y*e1 + z*e2."""
        c = np.zeros(G3_DIM, dtype=np.float32)
        c[1] = float(x)   # e0, mask=1
        c[2] = float(y)   # e1, mask=2
        c[4] = float(z)   # e2, mask=4
        return cls(c)

    @classmethod
    def bivector(cls, b01: float, b02: float, b12: float) -> "Multivector":
        """Create a pure grade-2 bivector: b01*e01 + b02*e02 + b12*e12."""
        c = np.zeros(G3_DIM, dtype=np.float32)
        c[3] = float(b01)  # e01, mask=3
        c[5] = float(b02)  # e02, mask=5
        c[6] = float(b12)  # e12, mask=6
        return cls(c)

    @classmethod
    def pseudoscalar(cls, s: float = 1.0) -> "Multivector":
        """Create a pure pseudoscalar: s*e012."""
        c = np.zeros(G3_DIM, dtype=np.float32)
        c[7] = float(s)
        return cls(c)

    @classmethod
    def from_dict(cls, d: Dict[int, float]) -> "Multivector":
        """Create from {mask: coefficient} dict."""
        c = np.zeros(G3_DIM, dtype=np.float32)
        for mask, val in d.items():
            idx = G3_MASK_TO_INDEX.get(mask)
            if idx is None:
                raise ValueError(f"Invalid mask {mask} for G3")
            c[idx] = float(val)
        return cls(c)

    @classmethod
    def from_array(cls, arr: np.ndarray) -> "Multivector":
        """Create from a raw 8-element numpy array."""
        return cls(arr)

    # ------------------------------------------------------------------
    # Coefficient access
    # ------------------------------------------------------------------

    def __getitem__(self, mask: int) -> float:
        """Get coefficient for a given basis mask."""
        idx = G3_MASK_TO_INDEX.get(mask)
        if idx is None:
            raise KeyError(f"Invalid mask {mask} for G3")
        return float(self._coeffs[idx])

    def __setitem__(self, mask: int, val: float) -> None:
        idx = G3_MASK_TO_INDEX.get(mask)
        if idx is None:
            raise KeyError(f"Invalid mask {mask} for G3")
        self._coeffs[idx] = float(val)

    @property
    def coeffs(self) -> np.ndarray:
        """Read-only view of coefficient array."""
        return self._coeffs.view()

    def to_array(self) -> np.ndarray:
        """Return a copy of the coefficient array."""
        return self._coeffs.copy()

    # ------------------------------------------------------------------
    # Grade extraction
    # ------------------------------------------------------------------

    def grade_part(self, g: int) -> "Multivector":
        """Extract the grade-g part of this multivector."""
        c = np.zeros(G3_DIM, dtype=np.float32)
        for basis in G3_BASIS:
            if basis.grade == g:
                idx = G3_MASK_TO_INDEX[basis.mask]
                c[idx] = self._coeffs[idx]
        return Multivector(c)

    def scalar_part(self) -> float:
        """Return scalar (grade-0) coefficient."""
        return float(self._coeffs[0])

    def vector_part(self) -> np.ndarray:
        """Return [e0, e1, e2] as a 3-element array."""
        return np.array([
            self._coeffs[G3_MASK_TO_INDEX[1]],  # e0
            self._coeffs[G3_MASK_TO_INDEX[2]],  # e1
            self._coeffs[G3_MASK_TO_INDEX[4]],  # e2
        ], dtype=np.float32)

    def bivector_part(self) -> np.ndarray:
        """Return [e01, e02, e12] as a 3-element array."""
        return np.array([
            self._coeffs[G3_MASK_TO_INDEX[3]],  # e01
            self._coeffs[G3_MASK_TO_INDEX[5]],  # e02
            self._coeffs[G3_MASK_TO_INDEX[6]],  # e12
        ], dtype=np.float32)

    def pseudoscalar_part(self) -> float:
        """Return e012 coefficient."""
        return float(self._coeffs[G3_MASK_TO_INDEX[7]])

    # ------------------------------------------------------------------
    # Arithmetic
    # ------------------------------------------------------------------

    def __add__(self, other: "Multivector") -> "Multivector":
        return Multivector(self._coeffs + other._coeffs)

    def __sub__(self, other: "Multivector") -> "Multivector":
        return Multivector(self._coeffs - other._coeffs)

    def __neg__(self) -> "Multivector":
        return Multivector(-self._coeffs)

    def __rmul__(self, scalar: float) -> "Multivector":
        return Multivector(self._coeffs * float(scalar))

    def __mul__(self, other: Union[float, "Multivector"]) -> "Multivector":
        if isinstance(other, (int, float, np.floating)):
            return Multivector(self._coeffs * float(other))
        # Defer to geometric_product module to avoid circular imports
        from .geometric_product import geometric_product
        return geometric_product(self, other)

    def __truediv__(self, scalar: float) -> "Multivector":
        return Multivector(self._coeffs / float(scalar))

    # ------------------------------------------------------------------
    # Norm / Normalization
    # ------------------------------------------------------------------

    def norm_sq(self) -> float:
        """Squared norm (sum of squared coefficients)."""
        return float(np.dot(self._coeffs, self._coeffs))

    def norm(self) -> float:
        """Euclidean norm of coefficient array."""
        return float(np.linalg.norm(self._coeffs))

    def normalized(self) -> "Multivector":
        """Return unit multivector (divide by norm)."""
        n = self.norm()
        if n < 1e-12:
            raise ZeroDivisionError("Cannot normalize a zero multivector")
        return Multivector(self._coeffs / n)

    # ------------------------------------------------------------------
    # Comparison
    # ------------------------------------------------------------------

    def is_close(self, other: "Multivector", atol: float = 1e-6) -> bool:
        return bool(np.allclose(self._coeffs, other._coeffs, atol=atol))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Multivector):
            return self.is_close(other)
        return NotImplemented

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        terms = []
        for basis in G3_BASIS:
            idx = G3_MASK_TO_INDEX[basis.mask]
            c = self._coeffs[idx]
            if abs(c) > 1e-9:
                terms.append(f"{c:.4f}*{basis}")
        return " + ".join(terms) if terms else "0"

    def to_dict(self) -> Dict[str, float]:
        """Serialize to {label: coeff} dict."""
        d = {}
        for basis in G3_BASIS:
            idx = G3_MASK_TO_INDEX[basis.mask]
            c = float(self._coeffs[idx])
            if abs(c) > 1e-9:
                d[str(basis)] = c
        return d

    def to_list(self) -> List[float]:
        """Return coefficients as plain Python list."""
        return self._coeffs.tolist()

    def reverse(self) -> Multivector:
        """Compute the reversion (conjugate) ~A."""
        from .operations import reverse as _reverse
        return _reverse(self)


# ---------------------------------------------------------------------------
# Convenience zero / identity
# ---------------------------------------------------------------------------

ZERO_MV   = Multivector()
SCALAR_ONE = Multivector.scalar(1.0)
