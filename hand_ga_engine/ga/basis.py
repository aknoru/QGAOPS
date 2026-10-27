"""
LIVE HAND GA ENGINE — ga/basis.py
Bitmask basis elements for G(p,q,r).

[IMPLEMENTED] Self-contained; does not depend on the parent QGPU library.
[ARCH]        XOR-mask product maps directly to future FPGA Basis/Metric Engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, List, Dict


# ---------------------------------------------------------------------------
# Grade (popcount)
# ---------------------------------------------------------------------------

def grade(mask: int) -> int:
    """Return the grade of a basis blade (number of set bits)."""
    return bin(mask).count("1")


# ---------------------------------------------------------------------------
# Permutation sign  s(A, B)
# ---------------------------------------------------------------------------

def sign_product(mask_a: int, mask_b: int) -> int:
    """Compute permutation sign for e_A * e_B using swap-count parity.

    Returns +1 or -1.
    [ARCH] Maps to XOR-tree parity logic in the Basis/Metric Engine.
    """
    n = 0
    b = mask_b
    while b:
        j = (b & -b).bit_length() - 1
        n += bin(mask_a >> (j + 1)).count("1")
        b &= b - 1
    return 1 if (n % 2 == 0) else -1


# ---------------------------------------------------------------------------
# Basis element
# ---------------------------------------------------------------------------

@dataclass(frozen=True, order=True)
class BasisElement:
    """Immutable basis element identified by its bitmask.

    Encoding:
        scalar = 0b000 = 0
        e0     = 0b001 = 1
        e1     = 0b010 = 2
        e2     = 0b100 = 4
        e01    = 0b011 = 3   (grade-2 bivector)
        e02    = 0b101 = 5
        e12    = 0b110 = 6
        e012   = 0b111 = 7   (grade-3 pseudoscalar)
    """
    mask: int
    label: Optional[str] = None

    def __post_init__(self) -> None:
        if self.mask < 0:
            raise ValueError(f"Basis mask must be non-negative, got {self.mask}")

    @property
    def grade(self) -> int:
        return grade(self.mask)

    def __repr__(self) -> str:
        lbl = self.label or basis_name(self.mask)
        return f"BasisElement({lbl}, mask={self.mask:#010b})"

    def __str__(self) -> str:
        return self.label or basis_name(self.mask)

    def __hash__(self) -> int:
        return hash(self.mask)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, BasisElement):
            return self.mask == other.mask
        return NotImplemented


# ---------------------------------------------------------------------------
# Human-readable name
# ---------------------------------------------------------------------------

def basis_name(mask: int) -> str:
    """Return a human-readable name for a basis mask.

    Examples:
        0  -> '1'       (scalar)
        1  -> 'e0'
        3  -> 'e01'
        7  -> 'e012'
    """
    if mask == 0:
        return "1"
    indices = [str(i) for i in range(32) if mask & (1 << i)]
    return "e" + "".join(indices)


# ---------------------------------------------------------------------------
# Basis set generation
# ---------------------------------------------------------------------------

def generate_basis(dimension: int) -> List[BasisElement]:
    """Generate all 2^n basis elements for an n-dimensional algebra.

    For G(3,0,0): dimension=3, returns 8 elements.
    """
    if not (0 <= dimension <= 16):
        raise ValueError(f"Dimension must be 0-16, got {dimension}")
    return [
        BasisElement(mask=m, label=basis_name(m))
        for m in range(1 << dimension)
    ]


def basis_by_grade(dimension: int) -> Dict[int, List[BasisElement]]:
    """Return all basis elements grouped by grade."""
    result: Dict[int, List[BasisElement]] = {}
    for be in generate_basis(dimension):
        g = be.grade
        result.setdefault(g, []).append(be)
    return result


# ---------------------------------------------------------------------------
# G3 canonical ordered basis
# ---------------------------------------------------------------------------

G3_BASIS: List[BasisElement] = generate_basis(3)
G3_MASK_TO_INDEX: Dict[int, int] = {b.mask: i for i, b in enumerate(G3_BASIS)}

# Convenience constants for G3
SCALAR = G3_BASIS[0]  # mask=0
E0     = G3_BASIS[1]  # mask=1
E1     = G3_BASIS[2]  # mask=2
E2     = G3_BASIS[4]  # mask=4
E01    = G3_BASIS[3]  # mask=3
E02    = G3_BASIS[5]  # mask=5
E12    = G3_BASIS[6]  # mask=6
E012   = G3_BASIS[7]  # mask=7
