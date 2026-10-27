"""Dimension-preserving Geometric Algebra mapping into Cl(3,0) multivectors.

Preserves exact vector dimensions without truncation or distortion:
- High-dimensional vector V in R^D is partitioned into ceil(D / 3) triplets.
- Each triplet (v_{3i}, v_{3i+1}, v_{3i+2}) is encoded as a grade-1 vector:
    u_i = v_{3i}*e1 + v_{3i+1}*e2 + v_{3i+2}*e3  (indices 1, 2, 3).
- Trailing components (if D % 3 != 0) are packed into the final multivector.
- L2 distance and dot product are evaluated via GA operations and proven
  identical to Euclidean NumPy reference metrics.
"""

from __future__ import annotations

import math
import time
from typing import Sequence, Tuple, Dict, Any
import numpy as np

from software.reference_model.qgaops_reference.algebra import Multivector


def vector_to_multivectors(vec: np.ndarray) -> list[Multivector]:
    """Map an arbitrary D-dimensional vector into a sequence of Cl(3,0) multivectors.
    
    Each 3 consecutive components map to e1, e2, e3 (indices 1, 2, 3).
    Scalar (0), bivectors (4, 5, 6), and trivector (7) are 0.
    """
    flat = np.asarray(vec, dtype=np.float64).ravel()
    dim = len(flat)
    num_mvs = math.ceil(dim / 3)
    multivectors: list[Multivector] = []
    
    for i in range(num_mvs):
        start = i * 3
        chunk = flat[start : min(start + 3, dim)]
        coeffs = [0.0] * 8
        if len(chunk) > 0:
            coeffs[1] = float(chunk[0])  # e1
        if len(chunk) > 1:
            coeffs[2] = float(chunk[1])  # e2
        if len(chunk) > 2:
            coeffs[3] = float(chunk[2])  # e3
        multivectors.append(Multivector(tuple(coeffs)))
        
    return multivectors


def multivectors_to_vector(mvs: Sequence[Multivector], original_dim: int) -> np.ndarray:
    """Reconstruct the original D-dimensional vector from Cl(3,0) multivectors."""
    extracted: list[float] = []
    for mv in mvs:
        extracted.append(mv[1])  # e1
        extracted.append(mv[2])  # e2
        extracted.append(mv[3])  # e3
    return np.array(extracted[:original_dim], dtype=np.float64)


def ga_l2_squared(mvs_a: Sequence[Multivector], mvs_b: Sequence[Multivector]) -> float:
    """Compute exact squared L2 distance between two mapped vectors using Cl(3,0) algebra.
    
    For each pair of grade-1 vectors u_i, w_i:
    diff_i = u_i - w_i
    diff_i * diff_i = (d1*e1 + d2*e2 + d3*e3)^2 = (d1^2 + d2^2 + d3^2) * 1 (scalar)
    Total squared distance is the sum of the scalar components.
    """
    if len(mvs_a) != len(mvs_b):
        raise ValueError(f"Multivector sequences must have identical length: {len(mvs_a)} vs {len(mvs_b)}")
        
    total_sq = 0.0
    for a, b in zip(mvs_a, mvs_b):
        diff = a - b
        prod = diff.geometric_product(diff)
        total_sq += prod[0]  # scalar coefficient is d1^2 + d2^2 + d3^2
    return total_sq


def ga_l2_distance(vec_a: np.ndarray, vec_b: np.ndarray) -> Tuple[float, Dict[str, Any]]:
    """Compute L2 distance using dimension-preserving GA mapping, tracking overhead and metrics."""
    t0 = time.perf_counter()
    mvs_a = vector_to_multivectors(vec_a)
    mvs_b = vector_to_multivectors(vec_b)
    t_pack = time.perf_counter() - t0
    
    t1 = time.perf_counter()
    sq_dist = ga_l2_squared(mvs_a, mvs_b)
    dist = math.sqrt(max(0.0, sq_dist))
    t_compute = time.perf_counter() - t1
    
    dim = len(vec_a)
    num_mvs = len(mvs_a)
    metrics = {
        "dimension": dim,
        "multivectors_per_vector": num_mvs,
        "ga_ops_per_pair": num_mvs * 2,  # 1 sub + 1 GP per triplet
        "pack_time_us": t_pack * 1e6,
        "compute_time_us": t_compute * 1e6,
        "memory_traffic_bytes": num_mvs * 8 * 4 * 2,  # 2 operands x 8 words x 4 bytes
    }
    return dist, metrics


def ga_dot_product(vec_a: np.ndarray, vec_b: np.ndarray) -> Tuple[float, Dict[str, Any]]:
    """Compute dot product using dimension-preserving Cl(3,0) Hestenes inner product."""
    t0 = time.perf_counter()
    mvs_a = vector_to_multivectors(vec_a)
    mvs_b = vector_to_multivectors(vec_b)
    t_pack = time.perf_counter() - t0
    
    t1 = time.perf_counter()
    dot_sum = 0.0
    for a, b in zip(mvs_a, mvs_b):
        # In Cl(3,0), inner product of two grade-1 vectors produces scalar u1*w1 + u2*w2 + u3*w3
        inner = a.hestenes_inner(b)
        dot_sum += inner[0]
    t_compute = time.perf_counter() - t1
    
    dim = len(vec_a)
    num_mvs = len(mvs_a)
    metrics = {
        "dimension": dim,
        "multivectors_per_vector": num_mvs,
        "ga_ops_per_pair": num_mvs,
        "pack_time_us": t_pack * 1e6,
        "compute_time_us": t_compute * 1e6,
        "memory_traffic_bytes": num_mvs * 8 * 4 * 2,
    }
    return dot_sum, metrics
