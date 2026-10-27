"""
LIVE HAND GA ENGINE — ga/operations.py
Additional GA operations: reverse, dual, norm, grade extraction,
commutator, anticommutator.

[IMPLEMENTED] All operations are pure Python/NumPy.
"""
from __future__ import annotations

import numpy as np
from .basis import G3_BASIS, G3_MASK_TO_INDEX, grade as _grade
from .multivector import Multivector, G3_DIM


# ---------------------------------------------------------------------------
# Reverse
# ---------------------------------------------------------------------------

def reverse(mv: Multivector) -> Multivector:
    """Compute the reverse ~A of a multivector.

    [IMPLEMENTED]
    For a grade-k blade B:  ~B = (-1)^(k(k-1)/2) * B

    Grade table:
        grade 0: sign = +1
        grade 1: sign = +1
        grade 2: sign = -1
        grade 3: sign = -1
    """
    result = mv.to_array()
    for basis in G3_BASIS:
        k = basis.grade
        sign = (-1) ** (k * (k - 1) // 2)
        if sign < 0:
            idx = G3_MASK_TO_INDEX[basis.mask]
            result[idx] = -result[idx]
    return Multivector(result)


# ---------------------------------------------------------------------------
# Grade extraction
# ---------------------------------------------------------------------------

def grade_involution(mv: Multivector) -> Multivector:
    """Grade involution: Â = (-1)^grade * A.

    For each blade: sign = (-1)^k.
    """
    result = mv.to_array()
    for basis in G3_BASIS:
        k = basis.grade
        if k % 2 == 1:
            idx = G3_MASK_TO_INDEX[basis.mask]
            result[idx] = -result[idx]
    return Multivector(result)


# ---------------------------------------------------------------------------
# Dual
# ---------------------------------------------------------------------------

# G3 pseudoscalar I = e012, mask=7
_I_MASK = 7

def dual(mv: Multivector) -> Multivector:
    """Compute the dual: A* = A * I^{-1}.

    [IMPLEMENTED]
    In G(3,0,0), I = e012, I^{-1} = -e012 (since I*I = -1 in G3).
    The dual maps:
        scalar  <-> e012  (pseudoscalar)
        e0      <-> -e12
        e1      <->  e02
        e2      <-> -e01
    """
    from .geometric_product import geometric_product
    I_inv = Multivector.from_dict({_I_MASK: -1.0})
    return geometric_product(mv, I_inv)


# ---------------------------------------------------------------------------
# Commutator / Anticommutator
# ---------------------------------------------------------------------------

def commutator(a: Multivector, b: Multivector) -> Multivector:
    """Commutator product: [A, B] = (A*B - B*A) / 2.

    [IMPLEMENTED]
    """
    from .geometric_product import geometric_product
    ab = geometric_product(a, b)
    ba = geometric_product(b, a)
    return (ab - ba) * 0.5


def anticommutator(a: Multivector, b: Multivector) -> Multivector:
    """Anticommutator product: {A, B} = (A*B + B*A) / 2.

    [IMPLEMENTED]
    """
    from .geometric_product import geometric_product
    ab = geometric_product(a, b)
    ba = geometric_product(b, a)
    return (ab + ba) * 0.5


# ---------------------------------------------------------------------------
# Norm and normalization
# ---------------------------------------------------------------------------

def norm(mv: Multivector) -> float:
    """Compute the Euclidean norm of a multivector.

    [IMPLEMENTED]
    sqrt(sum of squared coefficients).
    """
    return mv.norm()


def normalize(mv: Multivector) -> Multivector:
    """Return a unit multivector.

    [IMPLEMENTED]
    """
    return mv.normalized()


def scalar_product(a: Multivector, b: Multivector) -> float:
    """Scalar product: <A * ~B>_0 (grade-0 part of A * reverse(B)).

    [IMPLEMENTED]
    """
    from .geometric_product import geometric_product
    r = reverse(b)
    prod = geometric_product(a, r)
    return prod.scalar_part()


# ---------------------------------------------------------------------------
# Vector utilities
# ---------------------------------------------------------------------------

def vector_angle(a: Multivector, b: Multivector) -> float:
    """Angle between two grade-1 vectors in radians.

    [IMPLEMENTED]
    """
    va = a.vector_part().astype(np.float64)
    vb = b.vector_part().astype(np.float64)
    na = np.linalg.norm(va)
    nb = np.linalg.norm(vb)
    if na < 1e-12 or nb < 1e-12:
        return 0.0
    cos_theta = np.clip(np.dot(va, vb) / (na * nb), -1.0, 1.0)
    return float(np.arccos(cos_theta))


def vector_length(mv: Multivector) -> float:
    """Length (norm) of the grade-1 vector part.

    [IMPLEMENTED]
    """
    return float(np.linalg.norm(mv.vector_part()))


def bivector_magnitude(mv: Multivector) -> float:
    """Magnitude of the grade-2 (bivector) part.

    [IMPLEMENTED]
    Represents the area of the parallelogram spanned by two vectors.
    """
    return float(np.linalg.norm(mv.bivector_part()))
