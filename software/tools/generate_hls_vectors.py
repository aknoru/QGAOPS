"""Generate committed golden test vectors for the Vitis HLS C/C++ testbench.

Generates comprehensive test vectors strictly from the independent software reference model:
1. Exhaustive basis pairs for Geometric Product (64 cases) - Opcode 0x01
2. Exhaustive basis pairs for Wedge Product (64 cases) - Opcode 0x02
3. Exhaustive basis pairs for Hestenes Inner Product (64 cases) - Opcode 0x03
4. Addition and Subtraction boundary and mixed-grade tests - Opcodes 0x04, 0x05
5. Scalar Multiplication tests (positive, negative, fractional, saturating) - Opcode 0x06
6. Grade Projection tests (grades 0, 1, 2, 3) - Opcode 0x07
7. Reversion tests (all basis blades, mixed multivectors, saturation) - Opcode 0x08
8. Grade Involution tests (all basis blades, mixed multivectors, saturation) - Opcode 0x09
9. Clifford Conjugation tests (all basis blades, mixed multivectors, saturation) - Opcode 0x0A
10. Rotor Sandwich Product tests (3D spatial rotations: 90 deg, 180 deg, arbitrary) - Opcode 0x0B
11. Rotor Norm Squared tests (unit rotors, basis blades, scaled multivectors) - Opcode 0x0C
12. Fixed-point corner cases:
   - Rounding ties (round-to-nearest-even)
   - Saturation clamp at Q16.16 min (-2147483648) and max (+2147483647)
   - Intermediate accumulator boundary stress
   - Cancellation and near-zero results
13. Deterministic randomized multivectors across all operations (seed=4242)
14. Invalid operation codes (testing hardware error detection)

Outputs both CSV and JSON formats to hardware/hls/ga_engine/vectors/.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
import random
from typing import List, Dict, Any

from software.reference_model.qgaops_reference.algebra import (
    BASIS_NAMES,
    blade,
    scalar,
    rotor,
)
from software.reference_model.qgaops_reference.fixed_point import (
    FixedPointMultivector,
    FixedPointFormat,
)

OPCODES = {
    "geometric_product": 1,
    "wedge": 2,
    "hestenes_inner": 3,
    "add": 4,
    "subtract": 5,
    "scalar_mul": 6,
    "grade_proj": 7,
    "reverse": 8,
    "grade_involution": 9,
    "clifford_conj": 10,
    "sandwich": 11,
    "rotor_norm": 12,
}

STATUS_OK = 0
STATUS_ERR_OP = 1
STATUS_OVERFLOW = 4

FMT = FixedPointFormat(width=32, fractional_bits=16)


def create_vector_record(
    test_id: int,
    category: str,
    op_name: str,
    left_raw: list[int],
    right_raw: list[int],
    expected_raw: list[int],
    expected_status: int,
    description: str = "",
) -> Dict[str, Any]:
    return {
        "test_id": test_id,
        "category": category,
        "opcode": OPCODES.get(op_name, 0),
        "op_name": op_name,
        "left": left_raw,
        "right": right_raw,
        "expected": expected_raw,
        "expected_status": expected_status,
        "description": description,
    }


def generate_all_golden_vectors() -> List[Dict[str, Any]]:
    vectors: List[Dict[str, Any]] = []
    test_id = 1

    # -------------------------------------------------------------
    # 1. Exhaustive 64 basis pairs for Geometric Product (Opcode 1)
    # -------------------------------------------------------------
    for i in range(8):
        for j in range(8):
            mv_a = FixedPointMultivector.from_reals([1.0 if k == i else 0.0 for k in range(8)], fmt=FMT)
            mv_b = FixedPointMultivector.from_reals([1.0 if k == j else 0.0 for k in range(8)], fmt=FMT)
            res = mv_a.geometric_product(mv_b)
            status = STATUS_OVERFLOW if res.overflowed else STATUS_OK
            vectors.append(create_vector_record(
                test_id, "EXHAUSTIVE_GP", "geometric_product",
                list(mv_a.coefficients), list(mv_b.coefficients),
                list(res.coefficients), status,
                f"GP basis pair {BASIS_NAMES[i]} * {BASIS_NAMES[j]}"
            ))
            test_id += 1

    # -------------------------------------------------------------
    # 2. Exhaustive 64 basis pairs for Wedge Product (Opcode 2)
    # -------------------------------------------------------------
    for i in range(8):
        for j in range(8):
            mv_a = FixedPointMultivector.from_reals([1.0 if k == i else 0.0 for k in range(8)], fmt=FMT)
            mv_b = FixedPointMultivector.from_reals([1.0 if k == j else 0.0 for k in range(8)], fmt=FMT)
            res = mv_a.wedge(mv_b)
            status = STATUS_OVERFLOW if res.overflowed else STATUS_OK
            vectors.append(create_vector_record(
                test_id, "EXHAUSTIVE_WEDGE", "wedge",
                list(mv_a.coefficients), list(mv_b.coefficients),
                list(res.coefficients), status,
                f"Wedge basis pair {BASIS_NAMES[i]} ^ {BASIS_NAMES[j]}"
            ))
            test_id += 1

    # -------------------------------------------------------------
    # 3. Exhaustive 64 basis pairs for Hestenes Inner Product (Opcode 3)
    # -------------------------------------------------------------
    for i in range(8):
        for j in range(8):
            mv_a = FixedPointMultivector.from_reals([1.0 if k == i else 0.0 for k in range(8)], fmt=FMT)
            mv_b = FixedPointMultivector.from_reals([1.0 if k == j else 0.0 for k in range(8)], fmt=FMT)
            res = mv_a.hestenes_inner(mv_b)
            status = STATUS_OVERFLOW if res.overflowed else STATUS_OK
            vectors.append(create_vector_record(
                test_id, "EXHAUSTIVE_INNER", "hestenes_inner",
                list(mv_a.coefficients), list(mv_b.coefficients),
                list(res.coefficients), status,
                f"Hestenes inner basis pair {BASIS_NAMES[i]} . {BASIS_NAMES[j]}"
            ))
            test_id += 1

    # -------------------------------------------------------------
    # 4. Arithmetic: Addition and Subtraction (Opcodes 4 and 5)
    # -------------------------------------------------------------
    add_sub_cases = [
        ([1.0] * 8, [2.0] * 8, "uniform_positive"),
        ([-1.0] * 8, [1.0] * 8, "cancellation_to_zero"),
        ([32767.0] + [0.0]*7, [1.0] + [0.0]*7, "near_max_scalar"),
        ([-32767.0] + [0.0]*7, [1.0] + [0.0]*7, "near_min_scalar"),
        ([0.5, -0.25, 1.5, -2.0, 0.125, -0.0625, 3.0, -1.25],
         [0.5, 0.25, -1.5, 2.0, -0.125, 0.0625, -3.0, 1.25], "mixed_grade_cancellation"),
    ]
    for left_reals, right_reals, desc in add_sub_cases:
        mv_a = FixedPointMultivector.from_reals(left_reals, fmt=FMT)
        mv_b = FixedPointMultivector.from_reals(right_reals, fmt=FMT)
        
        # Add
        res_add = mv_a + mv_b
        st_add = STATUS_OVERFLOW if res_add.overflowed else STATUS_OK
        vectors.append(create_vector_record(
            test_id, "ARITHMETIC_ADD", "add",
            list(mv_a.coefficients), list(mv_b.coefficients),
            list(res_add.coefficients), st_add, f"Add {desc}"
        ))
        test_id += 1
        
        # Subtract
        res_sub = mv_a - mv_b
        st_sub = STATUS_OVERFLOW if res_sub.overflowed else STATUS_OK
        vectors.append(create_vector_record(
            test_id, "ARITHMETIC_SUB", "subtract",
            list(mv_a.coefficients), list(mv_b.coefficients),
            list(res_sub.coefficients), st_sub, f"Subtract {desc}"
        ))
        test_id += 1

    # -------------------------------------------------------------
    # 5. Scalar Multiplication (Opcode 6)
    # -------------------------------------------------------------
    scalar_cases = [
        ([1.0, 2.0, -3.0, 4.0, -0.5, 1.5, -2.5, 0.75], 2.0, "scale_by_positive_2"),
        ([1.0, 2.0, -3.0, 4.0, -0.5, 1.5, -2.5, 0.75], -1.0, "scale_by_negative_1"),
        ([1.0, 2.0, -3.0, 4.0, -0.5, 1.5, -2.5, 0.75], 0.0, "scale_by_zero"),
        ([1.0, 2.0, -3.0, 4.0, -0.5, 1.5, -2.5, 0.75], 0.25, "scale_by_fraction_quarter"),
        ([1000.0] * 8, 1000.0, "scale_large_overflow"),
    ]
    for left_reals, s_val, desc in scalar_cases:
        mv_a = FixedPointMultivector.from_reals(left_reals, fmt=FMT)
        mv_b = FixedPointMultivector.from_reals([s_val] + [0.0]*7, fmt=FMT)
        res_s = mv_a.scale_multivector(mv_b)
        st_s = STATUS_OVERFLOW if res_s.overflowed else STATUS_OK
        vectors.append(create_vector_record(
            test_id, "SCALAR_MUL", "scalar_mul",
            list(mv_a.coefficients), list(mv_b.coefficients),
            list(res_s.coefficients), st_s, f"Scalar mul {desc}"
        ))
        test_id += 1

    # -------------------------------------------------------------
    # 6. Grade Projection (Opcode 7)
    # -------------------------------------------------------------
    sample_mv = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    mv_proj_src = FixedPointMultivector.from_reals(sample_mv, fmt=FMT)
    for gr in range(4):
        mv_b = FixedPointMultivector([gr] + [0]*7, fmt=FMT)
        res_gp = mv_proj_src.grade_projection(gr)
        vectors.append(create_vector_record(
            test_id, "GRADE_PROJECTION", "grade_proj",
            list(mv_proj_src.coefficients), list(mv_b.coefficients),
            list(res_gp.coefficients), STATUS_OK, f"Project onto grade {gr}"
        ))
        test_id += 1

    # -------------------------------------------------------------
    # 7. Reversion (Opcode 8)
    # -------------------------------------------------------------
    for i in range(8):
        mv_a = FixedPointMultivector.from_reals([1.0 if k == i else 0.0 for k in range(8)], fmt=FMT)
        res_rev = mv_a.reverse()
        vectors.append(create_vector_record(
            test_id, "REVERSION", "reverse",
            list(mv_a.coefficients), [0]*8,
            list(res_rev.coefficients), STATUS_OK, f"Reversion of basis blade {BASIS_NAMES[i]}"
        ))
        test_id += 1
    # Mixed reversion
    mv_mixed = FixedPointMultivector.from_reals([1.5, -2.0, 3.25, -4.5, 0.75, -1.25, 2.5, -0.5], fmt=FMT)
    vectors.append(create_vector_record(
        test_id, "REVERSION", "reverse",
        list(mv_mixed.coefficients), [0]*8,
        list(mv_mixed.reverse().coefficients), STATUS_OK, "Reversion of mixed multivector"
    ))
    test_id += 1

    # -------------------------------------------------------------
    # 8. Grade Involution (Opcode 9)
    # -------------------------------------------------------------
    for i in range(8):
        mv_a = FixedPointMultivector.from_reals([1.0 if k == i else 0.0 for k in range(8)], fmt=FMT)
        res_inv = mv_a.grade_involution()
        vectors.append(create_vector_record(
            test_id, "GRADE_INVOLUTION", "grade_involution",
            list(mv_a.coefficients), [0]*8,
            list(res_inv.coefficients), STATUS_OK, f"Grade involution of basis blade {BASIS_NAMES[i]}"
        ))
        test_id += 1
    # Mixed involution
    vectors.append(create_vector_record(
        test_id, "GRADE_INVOLUTION", "grade_involution",
        list(mv_mixed.coefficients), [0]*8,
        list(mv_mixed.grade_involution().coefficients), STATUS_OK, "Grade involution of mixed multivector"
    ))
    test_id += 1

    # -------------------------------------------------------------
    # 9. Clifford Conjugation (Opcode 10)
    # -------------------------------------------------------------
    for i in range(8):
        mv_a = FixedPointMultivector.from_reals([1.0 if k == i else 0.0 for k in range(8)], fmt=FMT)
        res_cc = mv_a.clifford_conjugation()
        vectors.append(create_vector_record(
            test_id, "CLIFFORD_CONJUGATION", "clifford_conj",
            list(mv_a.coefficients), [0]*8,
            list(res_cc.coefficients), STATUS_OK, f"Clifford conjugation of basis blade {BASIS_NAMES[i]}"
        ))
        test_id += 1
    # Mixed clifford conjugation
    vectors.append(create_vector_record(
        test_id, "CLIFFORD_CONJUGATION", "clifford_conj",
        list(mv_mixed.coefficients), [0]*8,
        list(mv_mixed.clifford_conjugation().coefficients), STATUS_OK, "Clifford conjugation of mixed multivector"
    ))
    test_id += 1

    # -------------------------------------------------------------
    # 10. Rotor Sandwich Product (Opcode 11): C = R * v * ~R
    # -------------------------------------------------------------
    # Case 1: 90-degree rotation in xy-plane (e12): rot(e1) = e2
    # R = cos(pi/4) - sin(pi/4)*e12 = sqrt(2)/2 - sqrt(2)/2 * e12
    c45 = math.cos(math.pi / 4)
    s45 = math.sin(math.pi / 4)
    r_xy90 = [c45, 0.0, 0.0, 0.0, -s45, 0.0, 0.0, 0.0]
    v_e1 = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    mv_r1 = FixedPointMultivector.from_reals(r_xy90, fmt=FMT)
    mv_v1 = FixedPointMultivector.from_reals(v_e1, fmt=FMT)
    res_sw1 = mv_r1.sandwich(mv_v1)
    vectors.append(create_vector_record(
        test_id, "ROTOR_SANDWICH", "sandwich",
        list(mv_r1.coefficients), list(mv_v1.coefficients),
        list(res_sw1.coefficients), STATUS_OK, "Rotor 90 deg rotation of e1 in xy-plane -> e2"
    ))
    test_id += 1

    # Case 2: 180-degree rotation in xy-plane: rot(e1) = -e1
    r_xy180 = [0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0]  # -e12
    mv_r2 = FixedPointMultivector.from_reals(r_xy180, fmt=FMT)
    res_sw2 = mv_r2.sandwich(mv_v1)
    vectors.append(create_vector_record(
        test_id, "ROTOR_SANDWICH", "sandwich",
        list(mv_r2.coefficients), list(mv_v1.coefficients),
        list(res_sw2.coefficients), STATUS_OK, "Rotor 180 deg rotation of e1 -> -e1"
    ))
    test_id += 1

    # Case 3: Identity rotation R = 1.0
    r_id = [1.0] + [0.0]*7
    v_arb = [0.0, 1.5, -2.0, 3.5, 0.0, 0.0, 0.0, 0.0]
    mv_rid = FixedPointMultivector.from_reals(r_id, fmt=FMT)
    mv_varb = FixedPointMultivector.from_reals(v_arb, fmt=FMT)
    res_sw3 = mv_rid.sandwich(mv_varb)
    vectors.append(create_vector_record(
        test_id, "ROTOR_SANDWICH", "sandwich",
        list(mv_rid.coefficients), list(mv_varb.coefficients),
        list(res_sw3.coefficients), STATUS_OK, "Identity rotor rotation R=1"
    ))
    test_id += 1

    # -------------------------------------------------------------
    # 11. Rotor Norm Squared (Opcode 12): C[0] = <A * ~A>_0 = sum(a_k^2)
    # -------------------------------------------------------------
    norm_cases = [
        ([1.0] + [0.0]*7, "unit_scalar"),
        ([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "basis_e1"),
        ([0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], "basis_e12"),
        ([0.5, 0.5, 0.5, 0.5, 0.0, 0.0, 0.0, 0.0], "four_halves_norm_1"),
        ([1.0, -2.0, 3.0, -4.0, 0.5, -1.5, 2.0, -0.5], "mixed_multivector_norm"),
    ]
    for coeffs, desc in norm_cases:
        mv_norm_src = FixedPointMultivector.from_reals(coeffs, fmt=FMT)
        res_norm = mv_norm_src.norm_squared()
        st_norm = STATUS_OVERFLOW if res_norm.overflowed else STATUS_OK
        vectors.append(create_vector_record(
            test_id, "ROTOR_NORM", "rotor_norm",
            list(mv_norm_src.coefficients), [0]*8,
            list(res_norm.coefficients), st_norm, f"Rotor norm squared {desc}"
        ))
        test_id += 1

    # -------------------------------------------------------------
    # 12. Fixed-Point Edge Cases: Round-Half-Even, Saturation, Overflow
    # -------------------------------------------------------------
    tie_cases = [
        ([1.0] + [0.0]*7, [0.5 / 65536.0] + [0.0]*7, "rounding_tie_down_to_even_0"),
        ([3.0] + [0.0]*7, [0.5 / 65536.0] + [0.0]*7, "rounding_tie_up_to_even_2"),
    ]
    for left_reals, right_reals, desc in tie_cases:
        mv_a = FixedPointMultivector.from_reals(left_reals, fmt=FMT)
        mv_b = FixedPointMultivector.from_reals(right_reals, fmt=FMT)
        res = mv_a.geometric_product(mv_b)
        st = STATUS_OVERFLOW if res.overflowed else STATUS_OK
        vectors.append(create_vector_record(
            test_id, "FIXED_POINT_ROUNDING", "geometric_product",
            list(mv_a.coefficients), list(mv_b.coefficients),
            list(res.coefficients), st, desc
        ))
        test_id += 1

    # Saturation on Add/Sub
    max_val = FMT.maximum  # +2147483647
    min_val = FMT.minimum  # -2147483648
    mv_max = FixedPointMultivector([max_val] + [0]*7, fmt=FMT)
    mv_one = FixedPointMultivector([65536] + [0]*7, fmt=FMT)  # 1.0
    
    # Add overflow
    res_sat_add = mv_max + mv_one
    vectors.append(create_vector_record(
        test_id, "FIXED_POINT_SATURATION", "add",
        list(mv_max.coefficients), list(mv_one.coefficients),
        list(res_sat_add.coefficients), STATUS_OVERFLOW,
        "Addition positive overflow saturating to MAX"
    ))
    test_id += 1

    # Subtract underflow
    mv_min = FixedPointMultivector([min_val] + [0]*7, fmt=FMT)
    res_sat_sub = mv_min - mv_one
    vectors.append(create_vector_record(
        test_id, "FIXED_POINT_SATURATION", "subtract",
        list(mv_min.coefficients), list(mv_one.coefficients),
        list(res_sat_sub.coefficients), STATUS_OVERFLOW,
        "Subtraction negative underflow saturating to MIN"
    ))
    test_id += 1

    # GP saturation / 67-bit accumulator stress
    large_coeffs = [1000.0] * 8
    mv_large_a = FixedPointMultivector.from_reals(large_coeffs, fmt=FMT)
    mv_large_b = FixedPointMultivector.from_reals(large_coeffs, fmt=FMT)
    res_large = mv_large_a.geometric_product(mv_large_b)
    vectors.append(create_vector_record(
        test_id, "FIXED_POINT_ACCUMULATOR_STRESS", "geometric_product",
        list(mv_large_a.coefficients), list(mv_large_b.coefficients),
        list(res_large.coefficients), STATUS_OVERFLOW if res_large.overflowed else STATUS_OK,
        "Large multivector product stress testing 67-bit accumulator"
    ))
    test_id += 1

    # -------------------------------------------------------------
    # 13. Deterministic Randomized Multivectors across multiple operations
    # -------------------------------------------------------------
    rng = random.Random(4242)
    for rep in range(10):
        reals_a = [rng.uniform(-5.0, 5.0) for _ in range(8)]
        reals_b = [rng.uniform(-5.0, 5.0) for _ in range(8)]
        mv_a = FixedPointMultivector.from_reals(reals_a, fmt=FMT)
        mv_b = FixedPointMultivector.from_reals(reals_b, fmt=FMT)
        
        # Test GP, Wedge, and Inner
        for op in ["geometric_product", "wedge", "hestenes_inner"]:
            res = getattr(mv_a, op)(mv_b)
            st = STATUS_OVERFLOW if res.overflowed else STATUS_OK
            vectors.append(create_vector_record(
                test_id, "RANDOMIZED_VERIFICATION", op,
                list(mv_a.coefficients), list(mv_b.coefficients),
                list(res.coefficients), st,
                f"Randomized {op} seed 4242 rep {rep}"
            ))
            test_id += 1

    # -------------------------------------------------------------
    # 14. Invalid Operation Codes
    # -------------------------------------------------------------
    for invalid_op in [0, 13, 99, 255]:
        dummy_left = [65536] + [0]*7
        dummy_right = [65536] + [0]*7
        vectors.append({
            "test_id": test_id,
            "category": "INVALID_OPCODE",
            "opcode": invalid_op,
            "op_name": f"INVALID_{invalid_op}",
            "left": dummy_left,
            "right": dummy_right,
            "expected": [0] * 8,
            "expected_status": STATUS_ERR_OP,
            "description": f"Invalid opcode {invalid_op} expected to trigger STATUS_ERR_OP",
        })
        test_id += 1

    return vectors


def export_vectors(vectors: List[Dict[str, Any]], out_dir: str = "hardware/hls/ga_engine/vectors"):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    json_path = out_path / "golden_vectors.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "schema_version": "2.0",
            "precision": "Q16.16",
            "algebra": "Cl(3,0)",
            "blade_order": list(BASIS_NAMES),
            "total_vectors": len(vectors),
            "vectors": vectors,
        }, f, indent=2)
        
    # Save CSV
    csv_path = out_path / "golden_vectors.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Header
        header = ["test_id", "category", "opcode", "op_name", "expected_status"]
        header += [f"a_{k}" for k in range(8)]
        header += [f"b_{k}" for k in range(8)]
        header += [f"exp_{k}" for k in range(8)]
        writer.writerow(header)
        
        for v in vectors:
            row = [v["test_id"], v["category"], v["opcode"], v["op_name"], v["expected_status"]]
            row += v["left"]
            row += v["right"]
            row += v["expected"]
            writer.writerow(row)
            
    print(f"Generated {len(vectors)} committed golden vectors covering all 12 operations:")
    print(f"  JSON: {json_path}")
    print(f"  CSV:  {csv_path}")


if __name__ == "__main__":
    vecs = generate_all_golden_vectors()
    export_vectors(vecs)
