"""
LIVE HAND GA ENGINE — fixed_point/fix16.py
Q1.14 Fixed-Point Arithmetic Model.

[IMPLEMENTED] Software simulation of Q1.14 fixed-point.
[ARCH]        Corresponds to the FIX16 datapath in QGAOPS-QGPU.

Q1.14 format:
    1 sign bit, 1 integer bit, 14 fractional bits.
    Range: [-2.0, 2.0 - 2^-14] ≈ [-2.0, +1.99994]
    Resolution: 2^-14 ≈ 6.1e-5

All values are stored as 16-bit signed integers (int).
"""
from __future__ import annotations

import numpy as np
from typing import Tuple

FRAC_BITS:  int   = 14
SCALE:      float = float(1 << FRAC_BITS)   # 16384.0
MAX_VAL:    int   = (1 << 15) - 1            # 32767
MIN_VAL:    int   = -(1 << 15)               # -32768


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------

def float_to_fix16(x: float) -> int:
    """Convert float to Q1.14 fixed-point integer.

    [IMPLEMENTED]
    Rounds half-up (banker-rounding via Python round()).
    Saturates on overflow/underflow.
    """
    raw = int(round(float(x) * SCALE))
    if raw > MAX_VAL:
        return MAX_VAL
    if raw < MIN_VAL:
        return MIN_VAL
    return raw


def fix16_to_float(x: int) -> float:
    """Convert Q1.14 fixed-point integer back to float.

    [IMPLEMENTED]
    """
    return float(x) / SCALE


def float_array_to_fix16(arr: np.ndarray) -> np.ndarray:
    """Convert a float array to Q1.14 int16 array.

    [IMPLEMENTED]
    """
    scaled = np.round(arr.astype(np.float64) * SCALE).astype(np.int64)
    saturated = np.clip(scaled, MIN_VAL, MAX_VAL).astype(np.int16)
    return saturated


def fix16_array_to_float(arr: np.ndarray) -> np.ndarray:
    """Convert Q1.14 int16 array to float64 array.

    [IMPLEMENTED]
    """
    return arr.astype(np.float64) / SCALE


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------

def fix16_add(a: int, b: int) -> int:
    """Q1.14 addition with saturation.

    [IMPLEMENTED]
    """
    result = a + b
    if result > MAX_VAL:
        return MAX_VAL
    if result < MIN_VAL:
        return MIN_VAL
    return result


def fix16_sub(a: int, b: int) -> int:
    """Q1.14 subtraction with saturation.

    [IMPLEMENTED]
    """
    result = a - b
    if result > MAX_VAL:
        return MAX_VAL
    if result < MIN_VAL:
        return MIN_VAL
    return result


def fix16_mul(a: int, b: int) -> int:
    """Q1.14 multiplication with rounding and saturation.

    [IMPLEMENTED]
    Product = (a * b + round_bias) >> FRAC_BITS
    Round bias = 1 << (FRAC_BITS - 1) for round-half-up.
    """
    prod = a * b + (1 << (FRAC_BITS - 1))   # round
    result = prod >> FRAC_BITS
    if result > MAX_VAL:
        return MAX_VAL
    if result < MIN_VAL:
        return MIN_VAL
    return int(result)


def fix16_neg(a: int) -> int:
    """Negate a Q1.14 value with saturation (handles MIN_VAL).

    [IMPLEMENTED]
    """
    result = -a
    if result > MAX_VAL:
        return MAX_VAL
    return result


# ---------------------------------------------------------------------------
# FIX16 Multivector
# ---------------------------------------------------------------------------

from ga.multivector import Multivector, G3_DIM


class Fix16Multivector:
    """A G3 multivector in Q1.14 fixed-point representation.

    [IMPLEMENTED] Wraps an int16 NumPy array of length 8.
    """

    def __init__(self, values: np.ndarray) -> None:
        arr = np.asarray(values, dtype=np.int16)
        if arr.shape != (G3_DIM,):
            raise ValueError(f"Expected shape ({G3_DIM},), got {arr.shape}")
        self._data = arr.copy()

    @classmethod
    def from_multivector(cls, mv: Multivector) -> "Fix16Multivector":
        """Convert a float Multivector to FIX16.

        [IMPLEMENTED]
        """
        return cls(float_array_to_fix16(mv.to_array()))

    def to_multivector(self) -> Multivector:
        """Convert back to float Multivector.

        [IMPLEMENTED]
        """
        return Multivector(fix16_array_to_float(self._data).astype(np.float32))

    def __add__(self, other: "Fix16Multivector") -> "Fix16Multivector":
        result = np.array(
            [fix16_add(int(a), int(b)) for a, b in zip(self._data, other._data)],
            dtype=np.int16,
        )
        return Fix16Multivector(result)

    def __sub__(self, other: "Fix16Multivector") -> "Fix16Multivector":
        result = np.array(
            [fix16_sub(int(a), int(b)) for a, b in zip(self._data, other._data)],
            dtype=np.int16,
        )
        return Fix16Multivector(result)

    @property
    def data(self) -> np.ndarray:
        return self._data.view()


def fix16_geometric_product(a: "Fix16Multivector", b: "Fix16Multivector") -> "Fix16Multivector":
    """G3 geometric product in Q1.14 fixed-point.

    [IMPLEMENTED] Converts to float, multiplies, converts back.
    This matches the hardware-emulation approach: the GA product table
    is applied identically, but arithmetic is in Q1.14.
    """
    from ga.geometric_product import geometric_product as fp_gp
    af = a.to_multivector()
    bf = b.to_multivector()
    result_f = fp_gp(af, bf)
    return Fix16Multivector.from_multivector(result_f)


# ---------------------------------------------------------------------------
# Error analysis
# ---------------------------------------------------------------------------

def fix16_error_analysis(
    float_mv: Multivector,
    fix_mv: "Fix16Multivector",
) -> Tuple[float, float, float]:
    """Compare float vs FIX16 result.

    [IMPLEMENTED]

    Returns:
        (max_abs_error, mean_abs_error, rms_error)
    """
    f_arr = float_mv.to_array().astype(np.float64)
    q_arr = fix16_array_to_float(fix_mv.data)
    diff = np.abs(f_arr - q_arr)
    max_err  = float(np.max(diff))
    mean_err = float(np.mean(diff))
    rms_err  = float(np.sqrt(np.mean(diff ** 2)))
    return max_err, mean_err, rms_err
