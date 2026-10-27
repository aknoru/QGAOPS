"""
tests/test_rotor.py — Rotor unit tests.
[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest
from ga.multivector import Multivector
from ga.rotor import (
    rotor_from_axis_angle, rotor_reverse, rotor_compose,
    sandwich_product, rotor_norm, verify_rotor_unit, extract_axis_angle,
    rotor_from_two_vectors,
)


# ---------------------------------------------------------------------------

@pytest.fixture
def v_x(): return Multivector.vector(1.0, 0.0, 0.0)
@pytest.fixture
def v_y(): return Multivector.vector(0.0, 1.0, 0.0)
@pytest.fixture
def v_z(): return Multivector.vector(0.0, 0.0, 1.0)
@pytest.fixture
def axis_z(): return np.array([0.0, 0.0, 1.0])
@pytest.fixture
def axis_x(): return np.array([1.0, 0.0, 0.0])


# ---------------------------------------------------------------------------
# Unit norm
# ---------------------------------------------------------------------------

def test_rotor_unit_norm_zero_angle(axis_z):
    R = rotor_from_axis_angle(axis_z, 0.0)
    assert verify_rotor_unit(R, atol=1e-5)

def test_rotor_unit_norm_90(axis_z):
    R = rotor_from_axis_angle(axis_z, np.pi / 2)
    assert verify_rotor_unit(R, atol=1e-5)

def test_rotor_unit_norm_180(axis_z):
    R = rotor_from_axis_angle(axis_z, np.pi)
    assert verify_rotor_unit(R, atol=1e-5)

def test_rotor_unit_norm_arbitrary_axis():
    axis = np.array([0.577, 0.577, 0.577])
    R = rotor_from_axis_angle(axis, 1.23)
    assert verify_rotor_unit(R, atol=1e-5)


# ---------------------------------------------------------------------------
# Sandwich product correctness
# ---------------------------------------------------------------------------

def test_sandwich_zero_rotation_identity(v_x, axis_z):
    R = rotor_from_axis_angle(axis_z, 0.0)
    rotated = sandwich_product(R, v_x)
    assert rotated.is_close(v_x, atol=1e-5)

def test_sandwich_90_z_rotates_x_to_y(v_x, v_y, axis_z):
    """Rotating e0 by 90° around z should give e1."""
    R = rotor_from_axis_angle(axis_z, np.pi / 2)
    rotated = sandwich_product(R, v_x)
    # rotated should be close to e1
    vp = rotated.vector_part()
    assert abs(vp[1] - 1.0) < 0.01, f"Expected y≈1, got {vp}"

def test_sandwich_180_x_to_neg_x(v_x, axis_z):
    """Rotating e0 by 180° around z gives -e0."""
    R = rotor_from_axis_angle(axis_z, np.pi)
    rotated = sandwich_product(R, v_x)
    expected = Multivector.vector(-1.0, 0.0, 0.0)
    assert rotated.is_close(expected, atol=0.01)

def test_sandwich_preserves_length(v_x, axis_z):
    R = rotor_from_axis_angle(axis_z, 1.23)
    rotated = sandwich_product(R, v_x)
    assert abs(rotated.norm() - v_x.norm()) < 1e-4


# ---------------------------------------------------------------------------
# Rotor reverse
# ---------------------------------------------------------------------------

def test_rotor_reverse_double_inverse(axis_z):
    R = rotor_from_axis_angle(axis_z, 0.7)
    R_rev = rotor_reverse(R)
    # R * ~R = 1 (scalar)
    from ga.geometric_product import geometric_product
    prod = geometric_product(R, R_rev)
    assert abs(prod.scalar_part() - 1.0) < 1e-5
    assert abs(prod.norm() - 1.0) < 1e-5


# ---------------------------------------------------------------------------
# Rotor composition
# ---------------------------------------------------------------------------

def test_rotor_compose_double_90(v_x, axis_z):
    """Two 90° rotations around z = one 180° rotation."""
    R90 = rotor_from_axis_angle(axis_z, np.pi / 2)
    R180 = rotor_from_axis_angle(axis_z, np.pi)
    R_composed = rotor_compose(R90, R90)

    rotated_composed = sandwich_product(R_composed, v_x)
    rotated_180      = sandwich_product(R180, v_x)
    assert rotated_composed.is_close(rotated_180, atol=0.02)


# ---------------------------------------------------------------------------
# Axis-angle extraction
# ---------------------------------------------------------------------------

def test_extract_axis_angle_round_trip(axis_z):
    angle_in = 1.234
    R = rotor_from_axis_angle(axis_z, angle_in)
    axis_out, angle_out = extract_axis_angle(R)
    assert abs(angle_out - angle_in) < 0.01


# ---------------------------------------------------------------------------
# Two-vector rotor
# ---------------------------------------------------------------------------

def test_rotor_from_two_vectors_aligns(v_x, v_y):
    """Rotor from v_x → v_y should rotate v_x to v_y."""
    R = rotor_from_two_vectors(v_x, v_y)
    rotated = sandwich_product(R, v_x)
    vp = rotated.vector_part()
    # Should be close to y direction
    assert abs(vp[1]) > 0.9, f"Expected y-aligned, got {vp}"
