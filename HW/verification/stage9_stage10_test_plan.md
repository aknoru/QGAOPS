# Stage 9 & Stage 10 Verification Test Plan

## 1. Scope and Mission

This document defines the comprehensive verification test plan for `SEQ_GPU` and `PARALLEL_GPU`. The objective is to validate 100% mathematical, algebraic, and numerical equivalence against the independent Python reference model ([`software/reference_model/qgaops_reference/`](file:///d:/QGPU/software/reference_model/qgaops_reference/)).

---

## 2. Verification Hierarchy and Milestones

1. **Host C++ Simulation**: Unit verification of kernel algorithms and numerical functions compiled with host compilers (`g++` / `clang`).
2. **Vitis HLS C Simulation (`csim_design`)**: Verification inside the Vitis HLS environment using arbitrary precision types (`ap_int<67>`).
3. **Vitis HLS C Synthesis (`csynth_design`)**: Hardware compilation validating timing closure at $100\text{ MHz}$, resource utilization, and II.
4. **Vitis HLS C/RTL Co-Simulation (`cosim_design`)**: Cycle-accurate simulation verifying AXI4-Lite handshaking and bus timing against the C testbench.

---

## 3. Required Test Categories and Coverage Metrics

The self-checking testbenches ([`tb_seq_gpu.cpp`](file:///d:/QGPU/HW/hls/SEQ_GPU/testbench/tb_seq_gpu.cpp) and [`tb_parallel_gpu.cpp`](file:///d:/QGPU/HW/hls/PARALLEL_GPU/testbench/tb_parallel_gpu.cpp)) execute 285 distinct test vectors structured into the following categories:

| Category # | Category Description | Vector Count | Opcode | Validation Target |
|:---:|:---|:---:|:---:|:---|
| **1** | Exhaustive Basis Pairs: Geometric Product | 64 | `0x01` | All $8 \times 8$ ordered basis-blade geometric products. |
| **2** | Exhaustive Basis Pairs: Wedge Product | 64 | `0x02` | All $8 \times 8$ basis pairs for exterior wedge product $A \wedge B$. |
| **3** | Exhaustive Basis Pairs: Hestenes Inner Product | 64 | `0x03` | All $8 \times 8$ basis pairs for inner product $A \cdot B$. |
| **4** | Multivector Addition & Subtraction | 8 | `0x04`, `0x05` | Vector arithmetic, zero-cancellation, boundary saturation. |
| **5** | Scalar Multiplication | 8 | `0x06` | Scaling by positive, negative, zero, and fractional scalars. |
| **6** | Grade Projection | 8 | `0x07` | Extraction of grades $k \in \{0, 1, 2, 3\}$ from mixed multivectors. |
| **7** | Involutions: Reversion | 8 | `0x08` | Grade 0, 1 invariance; grade 2, 3 sign reversal. |
| **8** | Involutions: Grade Involution | 8 | `0x09` | Grade 0, 2 invariance; grade 1, 3 sign reversal. |
| **9** | Involutions: Clifford Conjugation | 8 | `0x0A` | Grade 0, 3 invariance; grade 1, 2 sign reversal. |
| **10** | Rotor Sandwich Product | 8 | `0x0B` | $90^\circ$, $180^\circ$, and arbitrary 3D spatial rotations ($R v \widetilde{R}$). |
| **11** | Rotor Norm Squared | 8 | `0x0C` | $\langle R \widetilde{R} \rangle_0 = \sum a_k^2$ evaluation and normalization checks. |
| **12** | Fixed-Point Numerical Corner Cases | 12 | Mixed | Banker's round-to-nearest-even tie-breaking, saturation at `INT32_MIN` and `INT32_MAX`. |
| **13** | Deterministic Randomized Multivectors | 12 | Mixed | Randomized multivectors generated with fixed PRNG seed (`seed=4242`). |
| **14** | Invalid Opcode Error Handling | 5 | Invalid | Verification of `STATUS_ERR_OP` output and zeroed result registers. |
| **TOTAL** | **Comprehensive Regression Suite** | **285** | **All** | **100% Full Specification Coverage** |

---

## 4. Pass / Fail Criteria and Diagnostics

A test run is declared **PASSED** if and only if:
1. Every vector produces a bit-exact 32-bit integer match across all 8 multivector blade coefficients (`c_act[k] == tv->expected[k]`).
2. The hardware status register matches the expected status code (`status_act == tv->expected_status`).
3. The testbench returns an exit code of `0`.

If any discrepancy occurs:
* The testbench prints the failing Test ID, Opcode, Category, Expected vs. Actual Status, and full 8-blade coefficient arrays.
* The testbench returns an exit code of `1`.
