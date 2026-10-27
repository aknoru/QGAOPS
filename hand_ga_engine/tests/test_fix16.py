"""
tests/test_fix16.py — FIX16 unit tests.
[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest
from fixed_point.fix16 import (
    float_to_fix16, fix16_to_float, fix16_add, fix16_sub, fix16_mul,
    Fix16Multivector, fix16_geometric_product, fix16_error_analysis,
    MAX_VAL, MIN_VAL, SCALE, fix16_neg,
)
from ga.multivector import Multivector


# ---------------------------------------------------------------------------
# Conversion round-trip
# ---------------------------------------------------------------------------

def test_float_to_fix16_zero():
    assert float_to_fix16(0.0) == 0

def test_float_to_fix16_one():
    q = float_to_fix16(1.0)
    assert q == int(SCALE)

def test_fix16_to_float_zero():
    assert fix16_to_float(0) == pytest.approx(0.0)

def test_round_trip(vals=(0.5, -0.5, 0.333, -1.0, 0.7854)):
    for v in vals:
        assert fix16_to_float(float_to_fix16(v)) == pytest.approx(v, abs=1e-3)


# ---------------------------------------------------------------------------
# Saturation
# ---------------------------------------------------------------------------

def test_saturation_overflow():
    assert float_to_fix16(100.0) == MAX_VAL

def test_saturation_underflow():
    assert float_to_fix16(-100.0) == MIN_VAL


# ---------------------------------------------------------------------------
# Arithmetic
# ---------------------------------------------------------------------------

def test_fix16_add():
    a = float_to_fix16(0.5)
    b = float_to_fix16(0.25)
    r = fix16_add(a, b)
    assert abs(fix16_to_float(r) - 0.75) < 1e-3

def test_fix16_sub():
    a = float_to_fix16(0.75)
    b = float_to_fix16(0.25)
    r = fix16_sub(a, b)
    assert abs(fix16_to_float(r) - 0.50) < 1e-3

def test_fix16_mul():
    a = float_to_fix16(0.5)
    b = float_to_fix16(0.5)
    r = fix16_mul(a, b)
    assert abs(fix16_to_float(r) - 0.25) < 1e-3

def test_fix16_mul_negative():
    a = float_to_fix16(-0.5)
    b = float_to_fix16(0.5)
    r = fix16_mul(a, b)
    assert abs(fix16_to_float(r) - (-0.25)) < 1e-3

def test_fix16_add_saturation():
    r = fix16_add(MAX_VAL, 1)
    assert r == MAX_VAL

def test_fix16_sub_saturation():
    r = fix16_sub(MIN_VAL, 1)
    assert r == MIN_VAL

def test_fix16_neg():
    a = float_to_fix16(0.5)
    r = fix16_neg(a)
    assert abs(fix16_to_float(r) - (-0.5)) < 1e-3


# ---------------------------------------------------------------------------
# Fix16Multivector
# ---------------------------------------------------------------------------

def test_fix16_mv_round_trip():
    mv = Multivector.vector(0.6, 0.8, 0.0)
    fmv = Fix16Multivector.from_multivector(mv)
    mv_back = fmv.to_multivector()
    assert mv.is_close(mv_back, atol=1e-3)

def test_fix16_mv_add():
    a = Fix16Multivector.from_multivector(Multivector.vector(0.5, 0.0, 0.0))
    b = Fix16Multivector.from_multivector(Multivector.vector(0.5, 0.0, 0.0))
    c = a + b
    mv = c.to_multivector()
    assert abs(mv.vector_part()[0] - 1.0) < 1e-3


# ---------------------------------------------------------------------------
# FIX16 GP error analysis
# ---------------------------------------------------------------------------

def test_fix16_gp_low_error():
    a = Multivector.vector(0.6, 0.8, 0.0)
    b = Multivector.vector(0.3, 0.5, 0.7)
    fa = Fix16Multivector.from_multivector(a)
    fb = Fix16Multivector.from_multivector(b)
    fix_gp = fix16_geometric_product(fa, fb)
    from ga.geometric_product import geometric_product
    float_gp = geometric_product(a, b)
    max_e, mean_e, rms_e = fix16_error_analysis(float_gp, fix_gp)
    assert max_e < 0.01, f"max error {max_e:.2e} too large"

def test_fix16_error_analysis_returns_tuple():
    a = Multivector.vector(1.0, 0.0, 0.0)
    fa = Fix16Multivector.from_multivector(a)
    result = fix16_error_analysis(a, fa)
    assert len(result) == 3
    assert all(isinstance(v, float) for v in result)
