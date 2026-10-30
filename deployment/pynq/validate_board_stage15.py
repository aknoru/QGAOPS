#!/usr/bin/env python3
"""
validate_board_stage15.py - PYNQ-ZU Hardware Transaction & Mathematical Validation Driver
Stage 15 Validation Script for QGAOPS-QGPU (SEQ_GPU_PYNQZU & PARALLEL_GPU_PYNQZU)

Target Hardware: PYNQ-ZU Rev B (XCZU5EG-SFVC784-1-E)
Supports:
  1. Direct register-based AXI4-Lite transactions
  2. All 12 Cl(3,0) Geometric Algebra operations
  3. All 8 canonical blades [1, e1, e2, e3, e12, e13, e23, e123] in Q16.16 fixed point
  4. Interrupt handling (GIER, IER, ISR acknowledgment) and polling
  5. Error state recovery and invalid opcode detection
  6. Automated regression test execution from golden_vectors_295.json
"""

import sys
import os
import time
import json
import argparse
import numpy as np

# AXI4-Lite Register Map Offsets for PARALLEL_GPU
PARALLEL_REGMAP = {
    "ADDR_AP_CTRL": 0x000,
    "ADDR_GIER":    0x004,
    "ADDR_IP_IER":  0x008,
    "ADDR_IP_ISR":  0x00C,
    "ADDR_A_BASE":  0x010,  # 8 blades, stride = 0x08 (0x10, 0x18, 0x20, 0x28, 0x30, 0x38, 0x40, 0x48)
    "A_STRIDE":     0x08,
    "ADDR_B_BASE":  0x050,  # 8 blades, stride = 0x08 (0x50, 0x58, 0x60, 0x68, 0x70, 0x78, 0x80, 0x88)
    "B_STRIDE":     0x08,
    "ADDR_C_BASE":  0x090,  # 8 blades, stride = 0x10 (0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0x100)
    "C_STRIDE":     0x10,
    "ADDR_OPCODE":  0x110,  # Bits [15:0]: opcode, Bits [21:16]: slot
    "ADDR_STATUS":  0x118,  # Bit 0: overflow, Bit 1: invalid op, Bit 2: div0
    "ADDR_DMA_LEN": 0x128   # 0 = direct register mode
}

# AXI4-Lite Register Map Offsets for SEQ_GPU
SEQ_REGMAP = {
    "ADDR_AP_CTRL": 0x00,
    "ADDR_GIER":    0x04,
    "ADDR_IP_IER":  0x08,
    "ADDR_IP_ISR":  0x0C,
    "ADDR_A_BASE":  0x20,   # 8 blades, stride = 0x04 (0x20, 0x24, 0x28, 0x2C, 0x30, 0x34, 0x38, 0x3C)
    "A_STRIDE":     0x04,
    "ADDR_B_BASE":  0x40,   # 8 blades, stride = 0x04 (0x40, 0x44, 0x48, 0x4C, 0x50, 0x54, 0x58, 0x5C)
    "B_STRIDE":     0x04,
    "ADDR_C_BASE":  0x60,   # 8 blades, stride = 0x04 (0x60, 0x64, 0x68, 0x6C, 0x70, 0x74, 0x78, 0x7C)
    "C_STRIDE":     0x04,
    "ADDR_OPCODE":  0x10,   # Bits [15:0]: opcode, Bits [21:16]: slot
    "ADDR_STATUS":  0x80,   # Bit 0: overflow, Bit 1: invalid op, Bit 2: div0 (0x84: valid)
    "ADDR_DMA_LEN": None
}

BLADE_NAMES = ["1", "e1", "e2", "e3", "e12", "e13", "e23", "e123"]

OPCODE_NAMES = {
    1: "GEOMETRIC_PRODUCT",
    2: "WEDGE_PRODUCT",
    3: "INNER_PRODUCT",
    4: "ADDITION",
    5: "SUBTRACTION",
    6: "SCALAR_MUL",
    7: "GRADE_PROJECT",
    8: "REVERSION",
    9: "GRADE_INVOLUTION",
    10: "CLIFFORD_CONJ",
    11: "ROTOR_SANDWICH",
    12: "ROTOR_NORM"
}

class QGPUHardwareDriver:
    def __init__(self, bitstream_path=None, ip_name=None, variant="auto"):
        self.bitstream_path = bitstream_path
        self.ip = None
        self.is_hardware = False
        self.variant = variant
        
        # Determine variant
        var_lower = variant.lower()
        if var_lower == "seq" or (ip_name and "seq" in ip_name.lower()) or (bitstream_path and "seq" in bitstream_path.lower()):
            self.regmap = SEQ_REGMAP
            self.variant_name = "SEQ_GPU"
        else:
            self.regmap = PARALLEL_REGMAP
            self.variant_name = "PARALLEL_GPU"
        
        print(f"[QGPU] Selected accelerator register map: {self.variant_name}")
        
        if bitstream_path and os.path.exists(bitstream_path):
            try:
                from pynq import Overlay
                print(f"[PYNQ-ZU] Programming FPGA with bitstream: {bitstream_path} ...")
                t0 = time.time()
                self.ol = Overlay(bitstream_path)
                t_load = (time.time() - t0) * 1000.0
                print(f"[PYNQ-ZU] Bitstream configured successfully in {t_load:.1f} ms.")
                
                # Auto-detect IP name if not provided
                if ip_name is None:
                    candidates = ["seq_gpu_0", "parallel_gpu_0"]
                    for c in candidates:
                        if hasattr(self.ol, c):
                            ip_name = c
                            break
                    if ip_name is None:
                        # Fall back to first available IP block
                        for k in self.ol.ip_dict.keys():
                            if "gpu" in k:
                                ip_name = k
                                break
                                
                if ip_name and hasattr(self.ol, ip_name):
                    self.ip = getattr(self.ol, ip_name)
                    self.is_hardware = True
                    print(f"[PYNQ-ZU] Bound to accelerator IP: '{ip_name}' at base 0x{self.ol.ip_dict[ip_name]['phys_addr']:08X}")
                else:
                    raise RuntimeError(f"Could not find accelerator IP '{ip_name}' in overlay.")
            except ImportError:
                print("[WARNING] 'pynq' package not available. Simulating in software mock mode.")
            except Exception as e:
                print(f"[ERROR] Failed to load overlay on hardware: {e}")
                print("[WARNING] Falling back to mock verification mode.")
        else:
            print(f"[INFO] No physical bitstream loaded ({bitstream_path}). Running in mock verification mode.")

        if not self.is_hardware:
            self._mock_mem = {}

    def write_reg(self, offset: int, data: int):
        if self.is_hardware:
            self.ip.write(offset, int(data) & 0xFFFFFFFF)
        else:
            self._mock_mem[offset] = int(data) & 0xFFFFFFFF

    def read_reg(self, offset: int) -> int:
        if self.is_hardware:
            return self.ip.read(offset)
        else:
            return self._mock_mem.get(offset, 0)

    def execute_transaction(self, a_blades, b_blades, opcode, slot=0, use_interrupts=False, timeout_sec=1.0):
        """
        Executes a complete single-operation transaction via AXI4-Lite.
        """
        rm = self.regmap
        if rm["ADDR_DMA_LEN"] is not None:
            self.write_reg(rm["ADDR_DMA_LEN"], 0)

        # 1. Write Operand A (8 blades)
        for i in range(8):
            self.write_reg(rm["ADDR_A_BASE"] + i * rm["A_STRIDE"], int(a_blades[i]))

        # 2. Write Operand B (8 blades)
        for i in range(8):
            self.write_reg(rm["ADDR_B_BASE"] + i * rm["B_STRIDE"], int(b_blades[i]))

        # 3. Write Opcode & Slot
        full_op = (opcode & 0xFFFF) | ((slot & 0x3F) << 16)
        self.write_reg(rm["ADDR_OPCODE"], full_op)

        # Configure interrupts if requested
        if use_interrupts:
            self.write_reg(rm["ADDR_GIER"], 1)    # Global interrupt enable
            self.write_reg(rm["ADDR_IP_IER"], 1)  # ap_done interrupt enable

        # 4. Start accelerator (ap_start = 1)
        t_start = time.perf_counter()
        self.write_reg(rm["ADDR_AP_CTRL"], 0x01)

        # 5. Wait for completion (ap_done = 1)
        done = False
        t_expire = t_start + timeout_sec
        while time.perf_counter() < t_expire:
            if self.is_hardware:
                ctrl = self.read_reg(rm["ADDR_AP_CTRL"])
                if ctrl & 0x02:  # ap_done bit
                    done = True
                    break
            else:
                done = True
                break

        t_end = time.perf_counter()
        latency_us = (t_end - t_start) * 1e6

        if not done:
            raise TimeoutError(f"Accelerator timed out waiting for ap_done (opcode {opcode}) after {timeout_sec}s")

        # 6. Read back 8 result blades
        c_blades = []
        for i in range(8):
            raw = self.read_reg(rm["ADDR_C_BASE"] + i * rm["C_STRIDE"])
            c_blades.append(int(np.int32(raw)))

        # 7. Read Status Register
        status = self.read_reg(rm["ADDR_STATUS"])

        # 8. Clear interrupt if used (Toggle-On-Write)
        if use_interrupts:
            self.write_reg(rm["ADDR_IP_ISR"], 1)

        return c_blades, status, latency_us

def run_regression_suite(driver: QGPUHardwareDriver, vectors_path: str, max_tests: int = None):
    if not os.path.exists(vectors_path):
        print(f"[ERROR] Test vector file not found: {vectors_path}")
        return False

    with open(vectors_path, "r") as f:
        vectors = json.load(f)

    if max_tests:
        vectors = vectors[:max_tests]

    total_tests = len(vectors)
    passed_tests = 0
    blade_matches = 0
    total_blades = total_tests * 8
    latencies = []

    print(f"\n================================================================================")
    print(f"  RUNNING QGPU VALIDATION SUITE ({driver.variant_name}): {total_tests} TEST VECTORS")
    print(f"================================================================================")

    for idx, vec in enumerate(vectors):
        v_id = vec["id"]
        op_code = vec["opcode"]
        op_name = vec["op_name"]
        a_vec = vec["a"]
        b_vec = vec["b"]
        expected_c = vec["expected"]
        expected_stat = vec.get("expected_status", 0)

        try:
            actual_c, actual_stat, latency_us = driver.execute_transaction(a_vec, b_vec, op_code)
            latencies.append(latency_us)

            # Compare all 8 blades
            test_pass = True
            for k in range(8):
                if actual_c[k] == expected_c[k]:
                    blade_matches += 1
                else:
                    test_pass = False

            if test_pass and (actual_stat == expected_stat):
                passed_tests += 1
            else:
                print(f"[-] Test {v_id:3d} ({op_name:20s}) FAILED: Expected {expected_c}, got {actual_c}")
        except Exception as e:
            print(f"[-] Test {v_id:3d} ({op_name:20s}) ERROR: {e}")

    avg_latency = np.mean(latencies) if latencies else 0.0
    print(f"--------------------------------------------------------------------------------")
    print(f"  SUMMARY RESULTS:")
    print(f"  Accelerator:       {driver.variant_name}")
    print(f"  Total Tests:       {total_tests}")
    print(f"  Passed Tests:      {passed_tests}/{total_tests} ({(passed_tests/total_tests)*100.0:.2f}%)")
    print(f"  Blade Matches:     {blade_matches}/{total_blades} ({(blade_matches/total_blades)*100.0:.2f}%)")
    print(f"  Avg Latency:       {avg_latency:.2f} us per transaction")
    print(f"================================================================================\n")
    return passed_tests == total_tests

def main():
    parser = argparse.ArgumentParser(description="QGAOPS-QGPU PYNQ-ZU Board Validation")
    parser.add_argument("--overlay", type=str, default=None, help="Path to .bit bitstream file")
    parser.add_argument("--ip", type=str, default=None, help="Name of accelerator IP block in BD")
    parser.add_argument("--variant", type=str, default="auto", choices=["auto", "seq", "parallel"], help="Accelerator variant")
    parser.add_argument("--vectors", type=str, default="HW/vivado/verification/data/golden_vectors_295.json", help="Path to test vector JSON")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of tests to run")
    args = parser.parse_args()

    driver = QGPUHardwareDriver(args.overlay, args.ip, args.variant)
    success = run_regression_suite(driver, args.vectors, args.limit)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
