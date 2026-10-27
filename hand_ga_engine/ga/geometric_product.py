"""
LIVE HAND GA ENGINE — ga/geometric_product.py
Full G(3,0,0) Geometric Product Engine.

[IMPLEMENTED] Pre-computed product table for G3.
[ARCH]        This module directly maps to the Shared Geometric Product Engine.

The geometric product of two multivectors A and B is computed via:
    C[mask_c] += A[mask_a] * B[mask_b] * sign(a,b) * metric(a,b)
    where mask_c = mask_a XOR mask_b

For grade-1 vectors:
    a * b = a·b  +  a∧b
where:
    a·b  (inner product / dot)  = grade-0 part
    a∧b  (outer product / wedge) = grade-2 part
"""
from __future__ import annotations

import numpy as np
from typing import List, Optional

from .basis import G3_BASIS, G3_MASK_TO_INDEX, sign_product, grade as _grade
from .metric import Metric, G3_METRIC
from .multivector import Multivector, G3_DIM


# ---------------------------------------------------------------------------
# Pre-compute G3 product table
# ---------------------------------------------------------------------------

def _build_product_table(metric: Metric) -> List[List[tuple]]:
    """Build product table: table[ia][ib] = list of (index_c, coeff).

    For each pair of basis blades (mask_a, mask_b):
        mask_c = mask_a XOR mask_b
        coeff  = sign_product(mask_a, mask_b) * metric.metric_coefficient(mask_a, mask_b)
    """
    n = len(G3_BASIS)
    table: List[List[tuple]] = [[None] * n for _ in range(n)]  # type: ignore

    for ia, ba in enumerate(G3_BASIS):
        for ib, bb in enumerate(G3_BASIS):
            mask_c = ba.mask ^ bb.mask
            ic = G3_MASK_TO_INDEX[mask_c]
            s = sign_product(ba.mask, bb.mask)
            m = metric.metric_coefficient(ba.mask, bb.mask)
            table[ia][ib] = (ic, s * m)
    return table


# Build once at module load time for G3
_G3_PRODUCT_TABLE = _build_product_table(G3_METRIC)


# ---------------------------------------------------------------------------
# Core operations
# ---------------------------------------------------------------------------

def geometric_product(
    a: Multivector,
    b: Multivector,
    metric: Optional[Metric] = None,
) -> Multivector:
    """Compute the full geometric product a * b in G(3,0,0).

    [IMPLEMENTED] [SOFTWARE-VALIDATED]

    Args:
        a, b: Input multivectors.
        metric: Optional custom metric (default: G3_METRIC).

    Returns:
        Multivector representing a*b.
    """
    if metric is None:
        table = _G3_PRODUCT_TABLE
    else:
        table = _build_product_table(metric)

    result = np.zeros(G3_DIM, dtype=np.float32)
    ca = a.coeffs
    cb = b.coeffs

    for ia in range(G3_DIM):
        if ca[ia] == 0.0:
            continue
        for ib in range(G3_DIM):
            if cb[ib] == 0.0:
                continue
            ic, coeff = table[ia][ib]
            result[ic] += ca[ia] * cb[ib] * coeff

    return Multivector(result)


def outer_product(a: Multivector, b: Multivector) -> Multivector:
    """Outer (wedge) product a ∧ b.

    [IMPLEMENTED] Grade-raising part of the geometric product.
    For grade-r blade A and grade-s blade B:
        A ∧ B = grade-(r+s) part of A*B
    """
    # For each pair, only include terms where mask_c has grade = grade_a + grade_b
    result = np.zeros(G3_DIM, dtype=np.float32)
    ca = a.coeffs
    cb = b.coeffs

    for ia, ba in enumerate(G3_BASIS):
        if ca[ia] == 0.0:
            continue
        grade_a = ba.grade
        for ib, bb in enumerate(G3_BASIS):
            if cb[ib] == 0.0:
                continue
            # Wedge: only if indices don't overlap
            if ba.mask & bb.mask:
                continue
            grade_b = bb.grade
            mask_c = ba.mask ^ bb.mask  # = ba.mask | bb.mask (no overlap)
            if _grade(mask_c) != grade_a + grade_b:
                continue
            ic = G3_MASK_TO_INDEX[mask_c]
            s = sign_product(ba.mask, bb.mask)
            result[ic] += ca[ia] * cb[ib] * s

    return Multivector(result)


def inner_product(a: Multivector, b: Multivector) -> Multivector:
    """Left inner (dot) product a · b.

    [IMPLEMENTED] Grade-lowering part.
    For grade-r blade A (r>0) and grade-s blade B (s>0):
        A · B = grade-|r-s| part of A*B
    Uses the Hestenes inner product convention (zero if either grade is 0).
    """
    result = np.zeros(G3_DIM, dtype=np.float32)
    ca = a.coeffs
    cb = b.coeffs

    for ia, ba in enumerate(G3_BASIS):
        if ca[ia] == 0.0:
            continue
        grade_a = ba.grade
        if grade_a == 0:
            continue
        for ib, bb in enumerate(G3_BASIS):
            if cb[ib] == 0.0:
                continue
            grade_b = bb.grade
            if grade_b == 0:
                continue
            mask_c = ba.mask ^ bb.mask
            expected_grade = abs(grade_a - grade_b)
            if _grade(mask_c) != expected_grade:
                continue
            ic = G3_MASK_TO_INDEX[mask_c]
            s = sign_product(ba.mask, bb.mask)
            m = G3_METRIC.metric_coefficient(ba.mask, bb.mask)
            result[ic] += ca[ia] * cb[ib] * s * m

    return Multivector(result)


def dot(a: Multivector, b: Multivector) -> float:
    """Scalar dot product for grade-1 vectors: a · b = Σ aᵢ bᵢ gᵢᵢ.

    [IMPLEMENTED] Equivalent to inner_product(a,b).scalar_part() for vectors.
    """
    va = a.vector_part()
    vb = b.vector_part()
    sig = np.array([1.0, 1.0, 1.0], dtype=np.float32)  # G(3,0,0)
    return float(np.dot(va * sig, vb))


def wedge(a: Multivector, b: Multivector) -> Multivector:
    """Alias for outer_product."""
    return outer_product(a, b)


def cross_product_mv(a: Multivector, b: Multivector) -> Multivector:
    """Compute cross product a × b as a vector.

    [IMPLEMENTED] In G3:  a × b = -dual(a ∧ b) as a grade-1 vector.
    """
    from .operations import dual
    w = outer_product(a, b)
    d = dual(w)
    # dual of bivector gives a vector with a sign; apply -1 for standard cross
    return d * (-1.0)


def cross_product_vec(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """NumPy cross product for 3D vectors (comparison reference).

    [IMPLEMENTED]
    """
    return np.cross(a, b).astype(np.float32)


# ---------------------------------------------------------------------------
# Identity verification helpers
# ---------------------------------------------------------------------------

def verify_distributivity(
    a: Multivector, b: Multivector, c: Multivector
) -> bool:
    """Verify (a+b)*c == a*c + b*c."""
    lhs = geometric_product(a + b, c)
    rhs = geometric_product(a, c) + geometric_product(b, c)
    return lhs.is_close(rhs)


def verify_associativity(
    a: Multivector, b: Multivector, c: Multivector
) -> bool:
    """Verify (a*b)*c == a*(b*c)."""
    lhs = geometric_product(geometric_product(a, b), c)
    rhs = geometric_product(a, geometric_product(b, c))
    return lhs.is_close(rhs)


def verify_gp_decomposition(a: Multivector, b: Multivector) -> bool:
    """Verify a*b = a·b + a∧b for grade-1 vectors."""
    gp  = geometric_product(a, b)
    ip  = inner_product(a, b)
    op  = outer_product(a, b)
    return gp.is_close(ip + op)
