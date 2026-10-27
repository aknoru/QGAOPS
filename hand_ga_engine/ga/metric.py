"""
LIVE HAND GA ENGINE — ga/metric.py
Metric tensor for G(p,q,r).

[IMPLEMENTED] Supports arbitrary diagonal metric signatures.
[ARCH]        Corresponds to the Metric Engine hardware block.
"""
from __future__ import annotations
import numpy as np
from typing import Tuple, List


class Metric:
    """Diagonal metric tensor for G(p,q,r).

    For G(3,0,0): signature = (1, 1, 1) — all positive.
    For G(4,1,0): signature = (1, 1, 1, 1, -1).

    Attributes:
        signature: Tuple of +1 / -1 / 0 values for each basis vector.
        dimension: Total number of basis vectors = p + q + r.
    """

    def __init__(self, signature: Tuple[int, ...]) -> None:
        if not all(s in (1, -1, 0) for s in signature):
            raise ValueError(f"Signature elements must be +1, -1, or 0. Got {signature}")
        self.signature = signature
        self.dimension = len(signature)
        self._diag = np.array(signature, dtype=np.float32)

    # ------------------------------------------------------------------
    # Metric coefficient of e_A * e_B
    # ------------------------------------------------------------------

    def metric_coefficient(self, mask_a: int, mask_b: int) -> float:
        """Return the metric scalar for e_A * e_B.

        For basis vectors that share indices (A AND B != 0):
            e_i * e_i = g(i, i) = signature[i]

        Only diagonal terms contribute (off-diagonal = 0).
        """
        shared = mask_a & mask_b
        coeff = 1.0
        for i in range(self.dimension):
            if shared & (1 << i):
                coeff *= float(self._diag[i])
        return coeff

    def __repr__(self) -> str:
        return f"Metric(signature={self.signature})"


# ---------------------------------------------------------------------------
# Pre-built standard metrics
# ---------------------------------------------------------------------------

G3_METRIC    = Metric((1, 1, 1))        # G(3,0,0) — 3D Euclidean
G4_1_METRIC  = Metric((1, 1, 1, 1, -1)) # G(4,1,0) — Conformal GA
PGA_METRIC   = Metric((0, 1, 1, 1))     # G(3,0,1) — Projective GA
PAULI_METRIC = Metric((1, 1, 1))        # Cl(3) Pauli algebra


def metric_from_name(name: str) -> Metric:
    """Look up a named metric."""
    table = {
        "G3":   G3_METRIC,
        "CGA":  G4_1_METRIC,
        "PGA":  PGA_METRIC,
        "G3_0_0": G3_METRIC,
        "G4_1_0": G4_1_METRIC,
    }
    if name not in table:
        raise ValueError(f"Unknown metric '{name}'. Available: {list(table)}")
    return table[name]
