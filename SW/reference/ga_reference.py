#!/usr/bin/env python3
"""
ga_reference.py - Independent Mathematical Reference Model for Cl(3,0) Geometric Algebra
Supports:
  1. High-precision float64 reference arithmetic
  2. Bit-accurate Q16.16 saturating signed fixed-point arithmetic
  3. Canonical blade ordering: [1, e1, e2, e3, e12, e13, e23, e123]
  4. All 12 canonical operations + error detection
"""

import numpy as np

# Canonical basis blades in Cl(3,0)
BLADE_NAMES = ["1", "e1", "e2", "e3", "e12", "e13", "e23", "e123"]
BLADE_GRADES = [0, 1, 1, 1, 2, 2, 2, 3]

# Fixed-point Q16.16 constants
Q_SHIFT = 16
Q_ONE = 1 << Q_SHIFT
Q_MAX = 0x7FFFFFFF   # +32767.99998
Q_MIN = -0x80000000  # -32768.00000

# Canonical Cl(3,0) multiplication table for basis blades (sign, result_blade_idx)
# e1^2 = e2^2 = e3^2 = +1
# e12 = e1*e2, e13 = e1*e3, e23 = e2*e3, e123 = e1*e2*e3
# Basis index: 0:1, 1:e1, 2:e2, 3:e3, 4:e12, 5:e13, 6:e23, 7:e123
MULT_TABLE = [
    # 1 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
    # e1 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,1), (1,0), (1,4), (1,5), (1,2), (1,3), (1,7), (1,6)],
    # e2 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,2), (-1,4), (1,0), (1,6), (-1,1), (-1,7), (1,3), (-1,5)],
    # e3 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,3), (-1,5), (-1,6), (1,0), (1,7), (-1,1), (-1,2), (1,4)],
    # e12 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,4), (-1,2), (1,1), (1,7), (-1,0), (-1,6), (1,5), (-1,3)],
    # e13 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,5), (-1,3), (-1,7), (1,1), (1,6), (-1,0), (-1,4), (1,2)],
    # e23 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,6), (1,7), (-1,3), (1,2), (-1,5), (1,4), (-1,0), (-1,1)],
    # e123 * [1, e1, e2, e3, e12, e13, e23, e123]
    [(1,7), (-1,6), (1,5), (-1,4), (-1,3), (1,2), (-1,1), (-1,0)]
]

def to_q16(val_float):
    """Converts float to signed Q16.16 with saturation."""
    raw = int(np.round(val_float * Q_ONE))
    return int(np.clip(raw, Q_MIN, Q_MAX))

def from_q16(val_int):
    """Converts signed Q16.16 integer to float."""
    return float(val_int) / Q_ONE

def sat_add(a, b):
    res = a + b
    if res > Q_MAX: return Q_MAX
    if res < Q_MIN: return Q_MIN
    return res

def sat_sub(a, b):
    res = a - b
    if res > Q_MAX: return Q_MAX
    if res < Q_MIN: return Q_MIN
    return res

def q16_mul(a, b):
    """64-bit intermediate multiplication with Q16 scaling and saturation."""
    prod = (int(a) * int(b)) >> Q_SHIFT
    if prod > Q_MAX: return Q_MAX
    if prod < Q_MIN: return Q_MIN
    return prod

class Cl30Multivector:
    def __init__(self, blades=None, is_q16=False):
        if blades is None:
            self.blades = [0] * 8
        elif is_q16:
            self.blades = [int(x) for x in blades]
        else:
            self.blades = [to_q16(x) for x in blades]

    def to_floats(self):
        return [from_q16(x) for x in self.blades]

    def __repr__(self):
        parts = []
        for name, val in zip(BLADE_NAMES, self.to_floats()):
            if abs(val) > 1e-4:
                parts.append(f"{val:.3f}*{name}")
        return " + ".join(parts) if parts else "0"

    # 1. Geometric Product
    def geometric_product(self, other):
        res = [0] * 8
        for i in range(8):
            a_i = self.blades[i]
            if a_i == 0: continue
            for j in range(8):
                b_j = other.blades[j]
                if b_j == 0: continue
                sign, target_idx = MULT_TABLE[i][j]
                prod = q16_mul(a_i, b_j)
                if sign == -1:
                    prod = -prod
                res[target_idx] = sat_add(res[target_idx], prod)
        return Cl30Multivector(res, is_q16=True)

    # 2. Wedge / Outer Product
    def wedge_product(self, other):
        res = [0] * 8
        for i in range(8):
            a_i = self.blades[i]
            if a_i == 0: continue
            g_i = BLADE_GRADES[i]
            for j in range(8):
                b_j = other.blades[j]
                if b_j == 0: continue
                g_j = BLADE_GRADES[j]
                sign, target_idx = MULT_TABLE[i][j]
                if BLADE_GRADES[target_idx] == (g_i + g_j):
                    prod = q16_mul(a_i, b_j)
                    if sign == -1: prod = -prod
                    res[target_idx] = sat_add(res[target_idx], prod)
        return Cl30Multivector(res, is_q16=True)

    # 3. Hestenes Inner Product
    def inner_product(self, other):
        res = [0] * 8
        for i in range(8):
            a_i = self.blades[i]
            if a_i == 0: continue
            g_i = BLADE_GRADES[i]
            for j in range(8):
                b_j = other.blades[j]
                if b_j == 0: continue
                g_j = BLADE_GRADES[j]
                # In Hestenes inner product: grade = |g_i - g_j|, with g_i, g_j > 0
                if g_i == 0 or g_j == 0:
                    continue
                sign, target_idx = MULT_TABLE[i][j]
                if BLADE_GRADES[target_idx] == abs(g_i - g_j):
                    prod = q16_mul(a_i, b_j)
                    if sign == -1: prod = -prod
                    res[target_idx] = sat_add(res[target_idx], prod)
        return Cl30Multivector(res, is_q16=True)

    # 4. Addition
    def add(self, other):
        res = [sat_add(a, b) for a, b in zip(self.blades, other.blades)]
        return Cl30Multivector(res, is_q16=True)

    # 5. Subtraction
    def sub(self, other):
        res = [sat_sub(a, b) for a, b in zip(self.blades, other.blades)]
        return Cl30Multivector(res, is_q16=True)

    # 6. Scalar Multiplication
    def scalar_mul(self, scalar_q16):
        res = [q16_mul(a, scalar_q16) for a in self.blades]
        return Cl30Multivector(res, is_q16=True)

    # 7. Grade Projection
    def grade_project(self, grade):
        res = [self.blades[i] if BLADE_GRADES[i] == grade else 0 for i in range(8)]
        return Cl30Multivector(res, is_q16=True)

    # 8. Reversion
    def reversion(self):
        # Grade 0: +1, Grade 1: +1, Grade 2: -1, Grade 3: -1
        signs = [1, 1, 1, 1, -1, -1, -1, -1]
        res = [s * a for s, a in zip(signs, self.blades)]
        return Cl30Multivector(res, is_q16=True)

    # 9. Grade Involution
    def grade_involution(self):
        # Grade 0, 2: +1; Grade 1, 3: -1
        signs = [1, -1, -1, -1, 1, 1, 1, -1]
        res = [s * a for s, a in zip(signs, self.blades)]
        return Cl30Multivector(res, is_q16=True)

    # 10. Clifford Conjugation
    def clifford_conjugation(self):
        # Reversion of grade involution
        signs = [1, -1, -1, -1, -1, -1, -1, 1]
        res = [s * a for s, a in zip(signs, self.blades)]
        return Cl30Multivector(res, is_q16=True)

    # 11. Rotor Sandwich Product: R * v * R~
    def rotor_sandwich(self, vector_v):
        r_rev = self.reversion()
        temp = self.geometric_product(vector_v)
        return temp.geometric_product(r_rev)

    # 12. Rotor Norm Squared: <R * R~>_0
    def rotor_norm_sq(self):
        r_rev = self.reversion()
        prod = self.geometric_product(r_rev)
        return prod.grade_project(0)
