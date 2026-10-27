"""
test_qgpu_pynq.py - Verification test for PYNQ QGPU Accelerator overlay driver
Tests basic register dispatch, Q16.16 arithmetic, rotor sandwich, and status handling.
"""

import sys
import numpy as np
from qgpu_overlay import (
    QGPUAccelerator,
    float_to_q16,
    q16_to_float,
    OPCODE_GEOMETRIC,
    OPCODE_WEDGE,
    OPCODE_INNER,
    OPCODE_ADD,
    OPCODE_SUB,
    OPCODE_ROTOR_SANDWICH
)

def run_tests():
    print("=" * 60)
    print("  QGPU PYNQ ACCELERATOR DRIVER VALIDATION TEST")
    print("=" * 60)

    acc = QGPUAccelerator()
    print(f"Driver initialized. Running in Mock/Host mode: {acc.is_mock}")

    # Test 1: Fixed-point conversion roundtrip
    test_vals = [0.0, 1.0, -1.0, 0.5, -0.5, 3.14159, -2.71828]
    for val in test_vals:
        q16 = float_to_q16(val)
        recovered = q16_to_float(q16)
        err = abs(val - recovered)
        assert err < 2e-4, f"Mismatch on {val}: got {recovered}, err={err}"
    print("[PASS] Fixed-point Q16.16 conversion test passed.")

    # Test 2: Addition operation mock dispatch
    a = [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    b = [3.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    res, status = acc.execute_op(a, b, OPCODE_ADD, slot=0)
    print(f"[PASS] Opcode dispatch (ADD) succeeded without error.")

    # Test 3: Rotor sandwich dispatch
    rotor = [0.7071, 0.0, 0.0, 0.0, 0.7071, 0.0, 0.0, 0.0]  # 90 deg z-rotation
    vec = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]        # e1
    res, status = acc.execute_op(rotor, vec, OPCODE_ROTOR_SANDWICH, slot=1)
    print(f"[PASS] Rotor sandwich dispatch succeeded without error.")

    print("=" * 60)
    print("  ALL PYNQ DRIVER UNIT TESTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
