# QGAOPS-QGPU: PYNQ-Z2 Deployment Guide

## 1. Overview
This directory contains the deployment runtime and driver for the **QGAOPS-QGPU** accelerator on the **PYNQ-Z2** board (Xilinx Zynq-7000 XC7Z020).

Two bitstream overlays are supported:
- **Project A (Sequential IP)**: `qgpu_seq.bit` + `qgpu_seq.hwh` (Minimal resource footprint)
- **Project B (Parallel IP)**: `qgpu_par.bit` + `qgpu_par.hwh` (High-performance pipelined multiplier array with AAMF Block RAM)

Bitstreams and hardware handoff files are located in:
`hardware/vivado/export/`

---

## 2. PYNQ-Z2 File Installation
Copy the overlay files and driver to your PYNQ board over SSH / SCP:
```bash
# From host PC to PYNQ board
scp hardware/vivado/export/qgpu_par.bit xilinx@192.168.2.99:/home/xilinx/jupyter_notebooks/qgpu/
scp hardware/vivado/export/qgpu_par.hwh xilinx@192.168.2.99:/home/xilinx/jupyter_notebooks/qgpu/
scp deployment/pynq/qgpu_overlay.py xilinx@192.168.2.99:/home/xilinx/jupyter_notebooks/qgpu/
scp deployment/pynq/test_qgpu_pynq.py xilinx@192.168.2.99:/home/xilinx/jupyter_notebooks/qgpu/
```

---

## 3. Python Quickstart on PYNQ

```python
from qgpu_overlay import QGPUAccelerator

# Initialize accelerator overlay
qgpu = QGPUAccelerator("qgpu_par.bit")

# Define two multivectors (8 blades: [1, e1, e2, e3, e12, e13, e23, e123])
a = [1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
b = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Compute Geometric Product: a * b
res, status = qgpu.execute_op(a, b, opcode=0x0001)
print("Result Multivector:", res)
print("Status (overflow/flags):", status)

# Compute Rotor Sandwich Rotation: R * v * ~R
rotor = [0.7071, 0.0, 0.0, 0.0, 0.7071, 0.0, 0.0, 0.0] # 90 degree rotation
vec   = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]        # e1 vector
rotated = qgpu.rotor_sandwich(rotor, vec)
print("Rotated Vector:", rotated)
```

---

## 4. Hardware Verification Test
Run the self-test suite directly on the board:
```bash
python3 test_qgpu_pynq.py
```
Expected output:
```text
============================================================
  QGPU PYNQ ACCELERATOR DRIVER VALIDATION TEST
============================================================
[PASS] Fixed-point Q16.16 conversion test passed.
[PASS] Opcode dispatch (ADD) succeeded without error.
[PASS] Rotor sandwich dispatch succeeded without error.
============================================================
  ALL PYNQ DRIVER UNIT TESTS PASSED!
============================================================
```
