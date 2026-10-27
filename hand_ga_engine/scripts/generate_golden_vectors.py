"""
scripts/generate_golden_vectors.py
QGAOPS-QGPU Golden Vector Generator

[GOLDEN MODEL] Generates reference vectors for HLS testbench validation.

Output: golden/golden_vectors.json
        results/hardware/fixed_point_accuracy.csv

Usage:
    python scripts/generate_golden_vectors.py

These vectors MUST be used by:
    hardware/hls/tb/tb_qgpu_accelerator.cpp
    hardware/linux/benchmark.c

The HLS testbench must pass ALL vectors before RTL co-simulation.
"""
from __future__ import annotations

import json
import math
import pathlib
import sys
import time
import csv

# Add project root to path
_HERE = pathlib.Path(__file__).parent.parent
sys.path.insert(0, str(_HERE))

import numpy as np
from ga.multivector import Multivector
from ga.geometric_product import geometric_product, outer_product, inner_product, dot
from ga.rotor import rotor_from_axis_angle, sandwich_product, rotor_reverse
from ga.operations import reverse, norm, dual
from fixed_point.fix16 import (
    Fix16Multivector, float_to_fix16, fix16_to_float,
    float_array_to_fix16, fix16_array_to_float,
    fix16_error_analysis, FRAC_BITS, SCALE
)

OUTPUT_DIR = _HERE / "golden"
RESULTS_DIR = _HERE / "results" / "hardware"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

FIX16_ERROR_BUDGET = 1.0 / 4096.0  # 2^-12


def mv_to_fix16_list(mv: Multivector) -> list[int]:
    """Convert multivector to list of 8 FIX16 int16 values."""
    return float_array_to_fix16(mv.to_array()).tolist()


def generate_vectors() -> dict:
    """Generate all golden test vectors."""
    vectors = {
        "metadata": {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source": "ga/ Python golden model",
            "fix16_format": "Q1.14 signed, scale=16384",
            "error_budget": FIX16_ERROR_BUDGET,
            "algebra": "G3 (3D Euclidean GA)",
            "label": "GOLDEN_MODEL",
        },
        "tests": []
    }

    tests = vectors["tests"]

    # ================================================================
    # SECTION 1: BASIS PRODUCT TESTS (MANDATORY)
    # ================================================================

    # e0 * e0 = scalar(1)
    e0 = Multivector.vector(1, 0, 0)
    e1 = Multivector.vector(0, 1, 0)
    e2 = Multivector.vector(0, 0, 1)

    r = geometric_product(e0, e0)
    tests.append({
        "id": "gp_e0_e0",
        "name": "e0 * e0 = scalar(+1.0)",
        "opcode": "GP",
        "section": "BASIS_PRODUCTS",
        "A": mv_to_fix16_list(e0),
        "B": mv_to_fix16_list(e0),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # e0 * e1 = e01
    r = geometric_product(e0, e1)
    tests.append({
        "id": "gp_e0_e1",
        "name": "e0 * e1 = +e01",
        "opcode": "GP",
        "section": "BASIS_PRODUCTS",
        "A": mv_to_fix16_list(e0),
        "B": mv_to_fix16_list(e1),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # e1 * e0 = -e01 (anticommutation)
    r = geometric_product(e1, e0)
    tests.append({
        "id": "gp_e1_e0",
        "name": "e1 * e0 = -e01 (anticommutation)",
        "opcode": "GP",
        "section": "BASIS_PRODUCTS",
        "A": mv_to_fix16_list(e1),
        "B": mv_to_fix16_list(e0),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # e1 * e1 = scalar(1)
    r = geometric_product(e1, e1)
    tests.append({
        "id": "gp_e1_e1",
        "name": "e1 * e1 = scalar(+1.0)",
        "opcode": "GP",
        "section": "BASIS_PRODUCTS",
        "A": mv_to_fix16_list(e1),
        "B": mv_to_fix16_list(e1),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # e2 * e2 = scalar(1)
    r = geometric_product(e2, e2)
    tests.append({
        "id": "gp_e2_e2",
        "name": "e2 * e2 = scalar(+1.0)",
        "opcode": "GP",
        "section": "BASIS_PRODUCTS",
        "A": mv_to_fix16_list(e2),
        "B": mv_to_fix16_list(e2),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # ================================================================
    # SECTION 2: WEDGE PRODUCT TESTS
    # ================================================================

    # e0 ^ e1 = e01
    r = outer_product(e0, e1)
    tests.append({
        "id": "wedge_e0_e1",
        "name": "e0 ^ e1 = +e01",
        "opcode": "WEDGE",
        "section": "WEDGE",
        "A": mv_to_fix16_list(e0),
        "B": mv_to_fix16_list(e1),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # e0 ^ e0 = 0 (self-wedge is zero)
    r = outer_product(e0, e0)
    tests.append({
        "id": "wedge_e0_e0",
        "name": "e0 ^ e0 = 0",
        "opcode": "WEDGE",
        "section": "WEDGE",
        "A": mv_to_fix16_list(e0),
        "B": mv_to_fix16_list(e0),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": True,
    })

    # (0.6*e0 + 0.8*e1) ^ (0.8*e0 - 0.6*e1)
    a = Multivector.vector(0.6, 0.8, 0)
    b = Multivector.vector(0.8, -0.6, 0)
    r = outer_product(a, b)
    tests.append({
        "id": "wedge_area",
        "name": "unit vectors 90deg wedge = e01 magnitude 1",
        "opcode": "WEDGE",
        "section": "WEDGE",
        "A": mv_to_fix16_list(a),
        "B": mv_to_fix16_list(b),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": False,
    })

    # ================================================================
    # SECTION 3: INNER PRODUCT TESTS
    # ================================================================

    r = inner_product(e0, e0)
    tests.append({
        "id": "inner_e0_e0",
        "name": "e0 . e0 = scalar(1)",
        "opcode": "INNER",
        "section": "INNER",
        "A": mv_to_fix16_list(e0),
        "B": mv_to_fix16_list(e0),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": False,
    })

    r = inner_product(e0, e1)
    tests.append({
        "id": "inner_e0_e1",
        "name": "e0 . e1 = 0 (orthogonal)",
        "opcode": "INNER",
        "section": "INNER",
        "A": mv_to_fix16_list(e0),
        "B": mv_to_fix16_list(e1),
        "expected": mv_to_fix16_list(r),
        "expected_float": r.to_list(),
        "mandatory": False,
    })

    # ================================================================
    # SECTION 4: NORM TESTS
    # ================================================================

    tests.append({
        "id": "norm_e0",
        "name": "norm(e0) = 1.0",
        "opcode": "NORM",
        "section": "NORM",
        "A": mv_to_fix16_list(e0),
        "B": None,
        "expected_scalar_float": norm(e0),
        "expected_scalar_fix16": float_to_fix16(norm(e0)),
        "mandatory": True,
    })

    v = Multivector.vector(0.6, 0.8, 0)
    tests.append({
        "id": "norm_unit_vector",
        "name": "norm(0.6*e0 + 0.8*e1) = 1.0",
        "opcode": "NORM",
        "section": "NORM",
        "A": mv_to_fix16_list(v),
        "B": None,
        "expected_scalar_float": norm(v),
        "expected_scalar_fix16": float_to_fix16(norm(v)),
        "mandatory": False,
    })

    # ================================================================
    # SECTION 5: ROTOR TESTS (MANDATORY)
    # ================================================================

    # R_z90 = rotor_from_axis_angle([0,0,1], pi/2)
    R_z90 = rotor_from_axis_angle(np.array([0.0, 0.0, 1.0]), math.pi / 2)
    tests.append({
        "id": "rotor_z90",
        "name": "rotor_from_axis_angle([0,0,1], pi/2)",
        "opcode": "ROTOR",
        "section": "ROTOR",
        "axis": [0.0, 0.0, 1.0],
        "angle_rad": math.pi / 2,
        "half_angle_fix16": float_to_fix16(math.pi / 4),
        "expected": mv_to_fix16_list(R_z90),
        "expected_float": R_z90.to_list(),
        "mandatory": True,
        "notes": "R[0] ≈ 0.7071 (cos(pi/4)), R[3] ≈ -0.7071 (-sin(pi/4)*1)"
    })

    # ================================================================
    # SECTION 6: SANDWICH PRODUCT TESTS (MANDATORY)
    # ================================================================

    # sandwich(R_z90, e0) = e1
    rotated = sandwich_product(R_z90, e0)
    tests.append({
        "id": "sandwich_z90_e0",
        "name": "R_z90 * e0 * ~R_z90 = e1 (90° rotation about z)",
        "opcode": "SANDWICH",
        "section": "SANDWICH",
        "A": mv_to_fix16_list(R_z90),  # Rotor
        "B": mv_to_fix16_list(e0),     # Vector
        "expected": mv_to_fix16_list(rotated),
        "expected_float": rotated.to_list(),
        "mandatory": True,
    })

    # sandwich(R_z90, e1) = -e0
    rotated2 = sandwich_product(R_z90, e1)
    tests.append({
        "id": "sandwich_z90_e1",
        "name": "R_z90 * e1 * ~R_z90 = -e0",
        "opcode": "SANDWICH",
        "section": "SANDWICH",
        "A": mv_to_fix16_list(R_z90),
        "B": mv_to_fix16_list(e1),
        "expected": mv_to_fix16_list(rotated2),
        "expected_float": rotated2.to_list(),
        "mandatory": True,
    })

    # Arbitrary rotor
    R_x45 = rotor_from_axis_angle(np.array([1.0, 0.0, 0.0]), math.pi / 4)
    rotated3 = sandwich_product(R_x45, e1)
    tests.append({
        "id": "sandwich_x45_e1",
        "name": "R_x45 * e1 * ~R_x45 (45° rotation about x)",
        "opcode": "SANDWICH",
        "section": "SANDWICH",
        "A": mv_to_fix16_list(R_x45),
        "B": mv_to_fix16_list(e1),
        "expected": mv_to_fix16_list(rotated3),
        "expected_float": rotated3.to_list(),
        "mandatory": False,
    })

    # ================================================================
    # SECTION 7: REVERSE TESTS
    # ================================================================

    all_ones = Multivector(np.ones(8, dtype=np.float32))
    rev = reverse(all_ones)
    tests.append({
        "id": "reverse_all_ones",
        "name": "reverse([1,1,1,1,1,1,1,1]) = [1,1,1,-1,1,-1,-1,-1]",
        "opcode": "REVERSE",
        "section": "REVERSE",
        "A": mv_to_fix16_list(all_ones),
        "B": None,
        "expected": mv_to_fix16_list(rev),
        "expected_float": rev.to_list(),
        "mandatory": True,
    })

    # ================================================================
    # SECTION 8: DISTANCE TESTS
    # ================================================================

    p1 = Multivector.vector(0.5, 0.5, 0)
    p2 = Multivector.vector(0.5, 0.5 + 0.5, 0)
    diff = p2 - p1
    d = norm(diff)
    tests.append({
        "id": "distance_vectors",
        "name": "distance(p1, p2) = 0.5",
        "opcode": "DISTANCE",
        "section": "DISTANCE",
        "A": mv_to_fix16_list(p1),
        "B": mv_to_fix16_list(p2),
        "expected_scalar_float": d,
        "expected_scalar_fix16": float_to_fix16(d),
        "mandatory": False,
    })

    # ================================================================
    # SECTION 9: QUANTUM-GA GATE TESTS
    # ================================================================

    # Qubit encoding: |ψ⟩ = a*scalar + b*e01
    # |0⟩: scalar=1, e01=0
    # |1⟩: scalar=0, e01=1
    def make_qubit(a: float, b: float) -> Multivector:
        return Multivector.from_dict({0: a, 3: b})

    ket_0 = make_qubit(1.0, 0.0)
    ket_1 = make_qubit(0.0, 1.0)

    # X|0⟩ = |1⟩
    X_result = make_qubit(0.0, 1.0)  # swap
    tests.append({
        "id": "qgate_x_0",
        "name": "X|0> = |1>",
        "opcode": "QGATE_X",
        "section": "QUANTUM",
        "A": mv_to_fix16_list(ket_0),
        "B": None,
        "expected": mv_to_fix16_list(X_result),
        "expected_float": X_result.to_list(),
        "mandatory": True,
    })

    # Z|1⟩ = -|1⟩
    Z_result = make_qubit(0.0, -1.0)
    tests.append({
        "id": "qgate_z_1",
        "name": "Z|1> = -|1>",
        "opcode": "QGATE_Z",
        "section": "QUANTUM",
        "A": mv_to_fix16_list(ket_1),
        "B": None,
        "expected": mv_to_fix16_list(Z_result),
        "expected_float": Z_result.to_list(),
        "mandatory": True,
    })

    # H|0⟩ = (|0⟩ + |1⟩)/√2
    inv_sqrt2 = 1.0 / math.sqrt(2)
    H_result = make_qubit(inv_sqrt2, inv_sqrt2)
    tests.append({
        "id": "qgate_h_0",
        "name": "H|0> = (|0>+|1>)/sqrt(2)",
        "opcode": "QGATE_H",
        "section": "QUANTUM",
        "A": mv_to_fix16_list(ket_0),
        "B": None,
        "expected": mv_to_fix16_list(H_result),
        "expected_float": H_result.to_list(),
        "expected_scalar_coeffs": [inv_sqrt2, inv_sqrt2],
        "mandatory": True,
    })

    # Y|0⟩ = i|1⟩ → real encoding: |1⟩
    Y_result = make_qubit(0.0, 1.0)
    tests.append({
        "id": "qgate_y_0",
        "name": "Y|0> = |1> (real GA encoding of i|1>)",
        "opcode": "QGATE_Y",
        "section": "QUANTUM",
        "A": mv_to_fix16_list(ket_0),
        "B": None,
        "expected": mv_to_fix16_list(Y_result),
        "expected_float": Y_result.to_list(),
        "mandatory": True,
    })

    # T|1⟩ = exp(i*pi/4)|1⟩ → real encoding: 1/sqrt(2) * |1⟩
    T_result = make_qubit(0.0, inv_sqrt2)
    tests.append({
        "id": "qgate_t_1",
        "name": "T|1> = (1/sqrt(2))|1> (real GA encoding)",
        "opcode": "QGATE_T",
        "section": "QUANTUM",
        "A": mv_to_fix16_list(ket_1),
        "B": None,
        "expected": mv_to_fix16_list(T_result),
        "expected_float": T_result.to_list(),
        "mandatory": True,
    })

    # ================================================================
    # SECTION 10: ALGEBRAIC IDENTITY TESTS
    # ================================================================

    # GP decomposition: a*b = a.b + a^b (for vectors)
    a = Multivector.vector(0.5, 0.3, 0)
    b = Multivector.vector(0.7, 0.4, 0)
    gp_ab = geometric_product(a, b)
    ip_ab = inner_product(a, b)
    op_ab = outer_product(a, b)
    decomp = ip_ab + op_ab
    tests.append({
        "id": "gp_decomp",
        "name": "GP(a,b) = INNER(a,b) + WEDGE(a,b) for grade-1 vectors",
        "opcode": "GP",
        "section": "ALGEBRAIC_IDENTITY",
        "A": mv_to_fix16_list(a),
        "B": mv_to_fix16_list(b),
        "expected": mv_to_fix16_list(gp_ab),
        "expected_float": gp_ab.to_list(),
        "decomp_inner": decomp.to_list(),
        "mandatory": False,
        "notes": "gp_ab == ip_ab + op_ab must hold"
    })

    return vectors


def generate_fixed_point_accuracy_report(vectors: dict) -> None:
    """Generate fixed_point_accuracy.csv comparing float vs FIX16."""
    csv_path = RESULTS_DIR / "fixed_point_accuracy.csv"

    rows = []
    for test in vectors["tests"]:
        if "expected" not in test or test["expected"] is None:
            continue
        expected_float = test.get("expected_float", [])
        expected_fix16 = test.get("expected", [])
        if not expected_float or not expected_fix16:
            continue

        # Convert fix16 back to float for comparison
        fix16_as_float = [fix16_to_float(v) for v in expected_fix16]

        errors = [abs(f - q) for f, q in zip(expected_float, fix16_as_float)]
        max_err = max(errors) if errors else 0.0
        mean_err = sum(errors) / len(errors) if errors else 0.0

        rows.append({
            "test_id": test["id"],
            "opcode": test["opcode"],
            "max_abs_error": f"{max_err:.8f}",
            "mean_abs_error": f"{mean_err:.8f}",
            "error_budget": f"{FIX16_ERROR_BUDGET:.8f}",
            "pass_fail": "PASS" if max_err <= FIX16_ERROR_BUDGET else "FAIL",
            "label": "GOLDEN_MODEL",
        })

    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)

    print(f"  Fixed-point accuracy report: {csv_path}")
    passed = sum(1 for r in rows if r["pass_fail"] == "PASS")
    print(f"  {passed}/{len(rows)} tests within FIX16 error budget ({FIX16_ERROR_BUDGET:.6f})")


def main() -> None:
    print("=" * 60)
    print("  QGAOPS-QGPU Golden Vector Generator")
    print("  Source: ga/ Python golden model")
    print("=" * 60)

    print("\n[1] Generating test vectors from Python golden model...")
    vectors = generate_vectors()

    # Save to JSON
    out_path = OUTPUT_DIR / "golden_vectors.json"
    with open(out_path, "w") as f:
        json.dump(vectors, f, indent=2)
    print(f"  Golden vectors: {out_path}")
    print(f"  Total tests: {len(vectors['tests'])}")
    print(f"  Mandatory: {sum(1 for t in vectors['tests'] if t.get('mandatory'))}")

    print("\n[2] Generating fixed-point accuracy report...")
    generate_fixed_point_accuracy_report(vectors)

    print("\n[3] Summary:")
    by_section: dict[str, int] = {}
    for t in vectors["tests"]:
        s = t.get("section", "OTHER")
        by_section[s] = by_section.get(s, 0) + 1
    for section, count in sorted(by_section.items()):
        print(f"    {section:<25} {count:3d} tests")

    print("\n  DONE. Use golden_vectors.json in HLS testbench.")
    print("  Validate HLS results against these before proceeding to RTL.")


if __name__ == "__main__":
    main()
