"""
LIVE HAND GA ENGINE — tests/test_ga.py
Unit tests for GA operations.

[IMPLEMENTED] [SOFTWARE-VALIDATED]
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

import numpy as np
import pytest
from ga.multivector import Multivector
from ga.geometric_product import (
    geometric_product, outer_product, inner_product, dot, wedge,
    verify_distributivity, verify_associativity, verify_gp_decomposition,
)
from ga.operations import reverse, dual, norm, normalize, vector_angle, commutator
from ga.basis import G3_BASIS, grade, sign_product


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def v_x():
    return Multivector.vector(1.0, 0.0, 0.0)

@pytest.fixture
def v_y():
    return Multivector.vector(0.0, 1.0, 0.0)

@pytest.fixture
def v_z():
    return Multivector.vector(0.0, 0.0, 1.0)

@pytest.fixture
def v_xy():
    return Multivector.vector(0.6, 0.8, 0.0)

@pytest.fixture
def v_xyz():
    return Multivector.vector(0.577, 0.577, 0.577)


# ---------------------------------------------------------------------------
# Basis tests
# ---------------------------------------------------------------------------

def test_grade_scalar():
    assert grade(0) == 0

def test_grade_vector():
    assert grade(1) == 1
    assert grade(2) == 1
    assert grade(4) == 1

def test_grade_bivector():
    assert grade(3) == 2
    assert grade(5) == 2
    assert grade(6) == 2

def test_grade_trivector():
    assert grade(7) == 3

def test_sign_product_commutes_sign():
    # e0*e1 = -e1*e0
    s01 = sign_product(1, 2)
    s10 = sign_product(2, 1)
    assert s01 == -s10

def test_sign_product_same_index():
    # e0*e0: sign = +1 (metric handles the value)
    s = sign_product(1, 1)
    assert s == 1


# ---------------------------------------------------------------------------
# Multivector arithmetic
# ---------------------------------------------------------------------------

def test_add(v_x, v_y):
    result = v_x + v_y
    assert abs(result[1] - 1.0) < 1e-6   # e0
    assert abs(result[2] - 1.0) < 1e-6   # e1

def test_sub(v_x, v_y):
    result = v_x - v_y
    assert abs(result[1] - 1.0) < 1e-6
    assert abs(result[2] - (-1.0)) < 1e-6

def test_scalar_mul(v_x):
    result = v_x * 2.0
    assert abs(result[1] - 2.0) < 1e-6

def test_neg(v_x):
    result = -v_x
    assert abs(result[1] - (-1.0)) < 1e-6

def test_norm_unit(v_x):
    assert abs(v_x.norm() - 1.0) < 1e-6

def test_norm_xy(v_xy):
    assert abs(v_xy.norm() - 1.0) < 1e-5   # (0.6)^2 + (0.8)^2 = 1

def test_normalize(v_xyz):
    n = normalize(v_xyz)
    assert abs(n.norm() - 1.0) < 1e-5

def test_scalar_part():
    mv = Multivector.scalar(3.14)
    assert abs(mv.scalar_part() - 3.14) < 1e-5

def test_vector_part(v_x):
    vp = v_x.vector_part()
    assert np.allclose(vp, [1.0, 0.0, 0.0], atol=1e-6)


# ---------------------------------------------------------------------------
# Geometric product
# ---------------------------------------------------------------------------

def test_gp_self_vectors_gives_scalar(v_x, v_y):
    # e0 * e0 = 1 (scalar, metric +1)
    gp = geometric_product(v_x, v_x)
    assert abs(gp.scalar_part() - 1.0) < 1e-5

def test_gp_orthogonal_vectors_gives_bivector(v_x, v_y):
    # e0 * e1 = e01 (purely bivector)
    gp = geometric_product(v_x, v_y)
    assert abs(gp.scalar_part()) < 1e-5
    bp = gp.bivector_part()
    assert np.linalg.norm(bp) > 0.5

def test_gp_decomposition_vx_vy(v_x, v_y):
    assert verify_gp_decomposition(v_x, v_y)

def test_gp_decomposition_xy_xyz(v_xy, v_xyz):
    assert verify_gp_decomposition(v_xy, v_xyz)

def test_gp_distributivity(v_x, v_y, v_z):
    assert verify_distributivity(v_x, v_y, v_z)

def test_gp_associativity(v_x, v_y, v_z):
    assert verify_associativity(v_x, v_y, v_z)

def test_gp_anticommutes_for_orthogonal(v_x, v_y):
    # e0*e1 = -e1*e0
    gp_xy = geometric_product(v_x, v_y)
    gp_yx = geometric_product(v_y, v_x)
    assert (gp_xy + gp_yx).is_close(Multivector(), atol=1e-5)


# ---------------------------------------------------------------------------
# Outer (wedge) product
# ---------------------------------------------------------------------------

def test_wedge_anticommutes(v_x, v_y):
    w_xy = outer_product(v_x, v_y)
    w_yx = outer_product(v_y, v_x)
    assert (w_xy + w_yx).is_close(Multivector(), atol=1e-5)

def test_wedge_self_zero(v_x):
    # v ∧ v = 0
    w = outer_product(v_x, v_x)
    assert w.is_close(Multivector(), atol=1e-5)

def test_wedge_orthogonal(v_x, v_y):
    w = outer_product(v_x, v_y)
    bp = w.bivector_part()
    assert np.linalg.norm(bp) > 0.9

def test_wedge_magnitude_equals_cross_product_magnitude(v_xy, v_xyz):
    from ga.operations import bivector_magnitude
    from ga.geometric_product import cross_product_vec
    w = outer_product(v_xy, v_xyz)
    bv_mag = bivector_magnitude(w)
    cp = cross_product_vec(v_xy.vector_part(), v_xyz.vector_part())
    cp_mag = float(np.linalg.norm(cp))
    assert abs(bv_mag - cp_mag) < 1e-4


# ---------------------------------------------------------------------------
# Inner product
# ---------------------------------------------------------------------------

def test_inner_product_orthogonal_zero(v_x, v_y):
    ip = inner_product(v_x, v_y)
    assert abs(ip.scalar_part()) < 1e-5

def test_inner_product_self_metric(v_x):
    ip = inner_product(v_x, v_x)
    assert abs(ip.scalar_part() - 1.0) < 1e-5

def test_dot_matches_numpy(v_xy, v_xyz):
    d = dot(v_xy, v_xyz)
    expected = float(np.dot(v_xy.vector_part(), v_xyz.vector_part()))
    assert abs(d - expected) < 1e-5


# ---------------------------------------------------------------------------
# Reverse
# ---------------------------------------------------------------------------

def test_reverse_vector_unchanged(v_x):
    rv = reverse(v_x)
    assert rv.is_close(v_x)

def test_reverse_bivector_negated(v_x, v_y):
    bv = outer_product(v_x, v_y)
    rbv = reverse(bv)
    assert rbv.is_close(-bv)

def test_reverse_twice_identity(v_xyz):
    gp = geometric_product(v_xyz, Multivector.vector(1, 0, 0))
    assert reverse(reverse(gp)).is_close(gp)


# ---------------------------------------------------------------------------
# Dual
# ---------------------------------------------------------------------------

def test_dual_scalar_gives_pseudoscalar():
    s = Multivector.scalar(1.0)
    d = dual(s)
    # dual(1) = I^{-1} = -e012 in G3
    assert abs(d.pseudoscalar_part()) > 0.9

def test_dual_vector_gives_bivector(v_x):
    d = dual(v_x)
    # dual of grade-1 should be grade-2
    assert abs(d.bivector_part()).max() > 0.5


# ---------------------------------------------------------------------------
# Commutator
# ---------------------------------------------------------------------------

def test_commutator_antisymmetric(v_x, v_y):
    c_xy = commutator(v_x, v_y)
    c_yx = commutator(v_y, v_x)
    assert (c_xy + c_yx).is_close(Multivector(), atol=1e-5)

def test_commutator_self_zero(v_x):
    c = commutator(v_x, v_x)
    assert c.is_close(Multivector(), atol=1e-5)


# ---------------------------------------------------------------------------
# Vector angle
# ---------------------------------------------------------------------------

def test_angle_parallel(v_x):
    a = vector_angle(v_x, v_x)
    assert abs(a) < 1e-5

def test_angle_orthogonal(v_x, v_y):
    a = vector_angle(v_x, v_y)
    assert abs(a - np.pi / 2) < 1e-5

def test_angle_antiparallel(v_x):
    a = vector_angle(v_x, -v_x)
    assert abs(a - np.pi) < 1e-5
