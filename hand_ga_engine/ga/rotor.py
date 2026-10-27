"""
LIVE HAND GA ENGINE — ga/rotor.py
Rotor construction, reverse, composition, and sandwich product for G(3,0,0).

[IMPLEMENTED] Pure Python/NumPy.
[ARCH]        Maps to QGAOPS rotor/sandwich hardware path.

A rotor R represents a rotation by angle θ around unit axis n:
    R = cos(θ/2) - sin(θ/2) * B
where B = n₀*e01 + n₁*e02 + n₂*e12 is the unit bivector dual to n.

The sandwich product:
    v' = R * v * ~R
rotates vector v by the rotor R.
"""
from __future__ import annotations

import numpy as np
from typing import Tuple

from .multivector import Multivector
from .geometric_product import geometric_product
from .operations import reverse, norm


def rotor_from_axis_angle(
    axis: np.ndarray, angle_rad: float
) -> Multivector:
    """Construct a rotor from a rotation axis and angle.

    [IMPLEMENTED]

    Args:
        axis: Unit 3D vector (x, y, z) — will be normalized internally.
        angle_rad: Rotation angle in radians.

    Returns:
        Rotor R = cos(θ/2) - sin(θ/2) * B
        where B is the bivector dual to the axis.

    Note:
        In G(3,0,0), dual to axis (x,y,z) is:
            B = x*e12 - y*e02 + z*e01  (via right-hand duality in G3)
        We use the convention:
            axis e0 -> e12 bivector
            axis e1 -> -e02 bivector (sign from dual)
            axis e2 -> e01 bivector
    """
    ax = np.asarray(axis, dtype=np.float64)
    n = np.linalg.norm(ax)
    if n < 1e-12:
        return Multivector.scalar(1.0)  # identity rotor
    ax = ax / n

    half = angle_rad * 0.5
    c = float(np.cos(half))
    s = float(np.sin(half))

    # Bivector B = -sin(θ/2) * (ax[0]*e01 + ax[1]*e02 + ax[2]*e12)
    # Using right-hand convention for G3:
    #   rotation axis (1,0,0) -> bivector e12 (the plane ⊥ to e0... wait)
    # Standard convention: B_ij = axis_k * eps_ijk
    #   axis = (a,b,c) -> B = a*e01? No.
    # Let's use: if axis = e0, plane of rotation = e12 span
    #            if axis = e1, plane of rotation = e02 span
    #            if axis = e2, plane of rotation = e01 span
    b01 = -s * ax[2]   # e01 coefficient (rotation in plane of e0,e1, axis=e2)
    b02 =  s * ax[1]   # e02 coefficient (rotation in plane of e0,e2, axis=e1)
    b12 = -s * ax[0]   # e12 coefficient (rotation in plane of e1,e2, axis=e0)

    return Multivector.from_dict({
        0: c,    # scalar
        3: b01,  # e01
        5: b02,  # e02
        6: b12,  # e12
    })


def rotor_from_two_vectors(
    a: Multivector, b: Multivector
) -> Multivector:
    """Construct a rotor that rotates vector a to align with vector b.

    [IMPLEMENTED]
    R = (b*a + |ba|) / |b*a + |ba||
    or equivalently R = 1 + ba (unnormalized) then normalize.
    """
    # Normalize input vectors
    va = a.vector_part().astype(np.float64)
    vb = b.vector_part().astype(np.float64)
    na = np.linalg.norm(va)
    nb = np.linalg.norm(vb)
    if na < 1e-12 or nb < 1e-12:
        return Multivector.scalar(1.0)

    va = va / na
    vb = vb / nb
    an = Multivector.vector(*va.tolist())
    bn = Multivector.vector(*vb.tolist())

    # R = bn*an normalized: R = (1 + bn*an) / |1 + bn*an|
    prod = geometric_product(bn, an)
    prod_with_scalar = prod + Multivector.scalar(1.0)
    n = prod_with_scalar.norm()
    if n < 1e-12:
        # Antiparallel vectors — rotate 180° around any perpendicular axis
        perp = _perpendicular_axis(va)
        return rotor_from_axis_angle(perp, np.pi)
    return prod_with_scalar * (1.0 / n)


def rotor_reverse(r: Multivector) -> Multivector:
    """Compute the reverse (conjugate) of a rotor: ~R.

    [IMPLEMENTED]
    For a rotor R = s + B (scalar + bivector):
        ~R = s - B
    Uses the general reverse operation.
    """
    from .operations import reverse as _reverse
    return _reverse(r)


def rotor_compose(r2: Multivector, r1: Multivector) -> Multivector:
    """Compose two rotors: R_total = R2 * R1.

    [IMPLEMENTED]
    Applying R1 first, then R2:
        v'' = R2 * (R1 * v * ~R1) * ~R2
             = (R2*R1) * v * ~(R2*R1)
    """
    return geometric_product(r2, r1)


def sandwich_product(r: Multivector, v: Multivector) -> Multivector:
    """Apply rotor sandwich: v' = R * v * ~R.

    [IMPLEMENTED]
    Rotates multivector v by rotor R.

    Args:
        r: Rotor (normalized grade-even multivector).
        v: Vector or multivector to rotate.

    Returns:
        Rotated multivector v'.
    """
    r_rev = rotor_reverse(r)
    return geometric_product(geometric_product(r, v), r_rev)


def rotor_norm(r: Multivector) -> float:
    """Compute the norm of a rotor for normalization check.

    [IMPLEMENTED]
    For a unit rotor: R*~R = 1, so norm should be ~1.
    """
    r_rev = rotor_reverse(r)
    prod = geometric_product(r, r_rev)
    return float(np.sqrt(abs(prod.scalar_part())))


def verify_rotor_unit(r: Multivector, atol: float = 1e-5) -> bool:
    """Verify that R * ~R ≈ 1 (unit rotor condition).

    [IMPLEMENTED]
    """
    n = rotor_norm(r)
    return abs(n - 1.0) < atol


def extract_axis_angle(r: Multivector) -> Tuple[np.ndarray, float]:
    """Extract rotation axis and angle from a rotor.

    [IMPLEMENTED]
    R = cos(θ/2) + sin(θ/2) * B_normalized
    θ = 2 * arccos(scalar_part)
    axis = bivector_part / sin(θ/2)
    """
    s = r.scalar_part()
    s = float(np.clip(s, -1.0, 1.0))
    half_angle = float(np.arccos(s))
    angle = 2.0 * half_angle
    sin_half = float(np.sin(half_angle))

    bv = r.bivector_part()  # [b01, b02, b12]

    if abs(sin_half) < 1e-8:
        # Identity rotation
        return np.array([0.0, 0.0, 1.0]), 0.0

    # Recover axis from bivector (inverse of rotor_from_axis_angle encoding):
    #   b01 = -sin * ax[2]  -> ax[2] = -b01/sin
    #   b02 =  sin * ax[1]  -> ax[1] =  b02/sin
    #   b12 = -sin * ax[0]  -> ax[0] = -b12/sin
    ax = np.array([
        -bv[2] / sin_half,   # e12 -> axis[0]
         bv[1] / sin_half,   # e02 -> axis[1]
        -bv[0] / sin_half,   # e01 -> axis[2]
    ])
    n = np.linalg.norm(ax)
    if n > 1e-12:
        ax = ax / n
    return ax, angle


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _perpendicular_axis(v: np.ndarray) -> np.ndarray:
    """Find any unit vector perpendicular to v."""
    v = v / np.linalg.norm(v)
    if abs(v[0]) < 0.9:
        perp = np.cross(v, np.array([1.0, 0.0, 0.0]))
    else:
        perp = np.cross(v, np.array([0.0, 1.0, 0.0]))
    return perp / np.linalg.norm(perp)
