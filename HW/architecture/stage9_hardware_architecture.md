# Stage 9: Hardware Interface and Architecture Design Specification

## 1. Executive Summary and Architectural Mission

This specification defines the hardware architecture and software/hardware boundary for the **QGAOPS-QGPU** accelerator. The primary objective is to implement a mathematically sound, bit-exact Clifford Geometric Algebra $\text{Cl}(3,0)$ accelerator on Xilinx/AMD FPGA SoC architectures, supporting both the **Zynq UltraScale+ MPSoC** (primary development target: `xczu5eg-sfvc784-1-e` / PYNQ-ZU) and **Zynq-7000** (`xc7z020clg400-1` / PYNQ-Z2).

The accelerator provides hardware execution of 12 canonical Geometric Algebra operations over 8-blade multivectors using signed 32-bit Q16.16 fixed-point arithmetic.

---

## 2. Target Platform and System Boundary

### 2.1 Processing System (PS) vs. Programmable Logic (PL) Partitioning

```
+-----------------------------------------------------------------------------+
|                         PROCESSING SYSTEM (PS)                              |
|                                                                             |
|  ARM Cortex-A53 (Quad-Core @ 1.2 GHz) / Cortex-A9 (Dual-Core @ 667 MHz)    |
|  - Embedded Linux OS / PYNQ Python Runtime Environment                     |
|  - High-level Gesture Recognition & Landmark Extraction (MediaPipe/OpenCV) |
|  - Multivector Construction & Q16.16 Encoding                              |
|  - Accelerator Driver & Task Scheduling                                     |
+-----------------------------------------------------------------------------+
                                      |
                      AXI4-Lite Host Control & Data Bus
                    (Base Address: e.g. 0xA000_0000, 4 KB)
                                      |
+-----------------------------------------------------------------------------+
|                      PROGRAMMABLE LOGIC (PL) ACCELERATOR                    |
|                                                                             |
|  +-----------------------------------------------------------------------+  |
|  |                     s_axi_control (AXI4-Lite Slave)                   |  |
|  |   - AP_START / AP_DONE / AP_IDLE / AP_READY Control Registers         |  |
|  |   - Opcode Selection (OPCODE_GP .. OPCODE_ROTOR_NORM)                 |  |
|  |   - Status & Overflow Flags                                           |  |
|  |   - Operand A Registers (8 x 32-bit Q16.16 words)                     |  |
|  |   - Operand B Registers (8 x 32-bit Q16.16 words)                     |  |
|  |   - Result C Registers  (8 x 32-bit Q16.16 words)                     |  |
|  +-----------------------------------------------------------------------+  |
|                                     |                                       |
|  +-----------------------------------------------------------------------+  |
|  |                        Geometric Algebra Core                         |  |
|  |   [SEQ_GPU: Time-multiplexed]  OR  [PARALLEL_GPU: Fully unrolled]     |  |
|  |   - 67-bit Precision Accumulator with Zero Intermediate Truncation    |  |
|  |   - Round-to-Nearest-Even Rescaling Unit (>> 16 with tie-breaking)   |  |
|  |   - Signed Saturation Limiter [-2147483648, +2147483647]              |  |
|  |   - Metric Evaluator: Euclidean Cl(3,0) (+1, +1, +1)                  |  |
|  +-----------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------+
```

### 2.2 Target FPGA Device and Toolchain Notes

* **Target Part**: AMD/Xilinx Zynq UltraScale+ MPSoC `xczu5eg-sfvc784-1-e` (or Zynq-7000 `xc7z020clg400-1`).
* **Clock Target**: $100\text{ MHz}$ ($T_{\text{clk}} = 10.0\text{ ns}$, Uncertainty $= 2.7\text{ ns}$ for UltraScale+, $1.5\text{ ns}$ for Zynq-7000).
* **Board Support Precondition**: While PYNQ-ZU and PYNQ-Z2 are targeted, standard Vivado installations may not include third-party board definition files (`board.xml`) by default. Therefore, all HLS IP components are generated at the **device part level** (`xczu5eg-sfvc784-1-e` or `xc7z020clg400-1`), guaranteeing toolchain independence without unverified board XML dependencies.

---

## 3. Mathematical Foundations and Coordinate Conventions

### 3.1 Basis Blade Indexing

The accelerator computes strictly in the real 8-dimensional Clifford algebra $\text{Cl}(3,0)$. Multivectors are ordered canonically by grade and index:

| Index | Basis Blade | Bitmask | Grade | Metric ($e_i^2$) | Semantic Description |
|:---:|:---:|:---:|:---:|:---:|:---|
| **0** | $1$ | `0b000` (0) | 0 | $+1$ | Scalar |
| **1** | $e_1$ | `0b001` (1) | 1 | $+1$ | Vector $x$-component |
| **2** | $e_2$ | `0b010` (2) | 1 | $+1$ | Vector $y$-component |
| **3** | $e_3$ | `0b100` (4) | 1 | $+1$ | Vector $z$-component |
| **4** | $e_{12}$ | `0b011` (3) | 2 | $-1$ | Bivector $xy$-plane |
| **5** | $e_{13}$ | `0b101` (5) | 2 | $-1$ | Bivector $xz$-plane |
| **6** | $e_{23}$ | `0b110` (6) | 2 | $-1$ | Bivector $yz$-plane |
| **7** | $e_{123}$| `0b111` (7) | 3 | $-1$ | Pseudoscalar volume |

### 3.2 Canonical Sign Rules for Euclidean Metric

For any two basis blades $e_L$ and $e_R$ with bitmasks $m_L$ and $m_R$:
$$e_L e_R = \text{sign}(m_L, m_R) \, e_{m_L \oplus m_R}$$
Where $\text{sign}(m_L, m_R) = (-1)^k$, and $k$ is the number of anticommuting basis vector transpositions:
$$k = \sum_{i=0}^2 \sum_{j=0}^{i-1} \left( [m_L \& (1 \ll i)] \neq 0 \right) \wedge \left( [m_R \& (1 \ll j)] \neq 0 \right)$$

---

## 4. Top-Level Interface Architecture

### 4.1 Interface Selection: AXI4-Lite Register Interface

Stage 9 implements a memory-mapped **AXI4-Lite** control and register interface (`s_axilite`) for both `SEQ_GPU` and `PARALLEL_GPU`.

**Rationale & Scope:**
1. **Low Latency for Single Transactions**: Gesture recognition and robotics control pipelines evaluate multivector operations in discrete steps (e.g. hand orientation rotor calculation, sandwich projection). AXI4-Lite avoids DMA engine configuration overhead for single-packet computations.
2. **Deterministic Handshaking**: Uses standard Xilinx `ap_ctrl_hs` protocol (`ap_start`, `ap_done`, `ap_idle`, `ap_ready`).
3. **Limitation Documentation**:
   * *Bandwidth Bottleneck*: For bulk batch processing (> 100,000 multivectors/sec), transferring 64 bytes of operands and reading 32 bytes of results word-by-word over AXI4-Lite incurs CPU MMIO transaction overhead.
   * *Future DMA Path*: Subsequent stages (Stage 11+) may wrap this core with an AXI-Stream/DMA converter for streaming batches, but Stage 9 explicitly avoids claiming DMA integration before it is designed and verified.

---

## 5. Transaction Semantics and Reset Behavior

1. **Power-On Reset**: Active-low `ap_rst_n` asserts all internal state registers to 0. `ap_idle` asserts high, `ap_done` deasserts low.
2. **Dispatch Sequence**:
   * Host writes Operand A coefficients ($8 \times 32$-bit words) to registers `0x40`–`0x5C`.
   * Host writes Operand B coefficients ($8 \times 32$-bit words) to registers `0x60`–`0x7C`.
   * Host writes Opcode to register `0x18`.
   * Host writes `0x01` (`ap_start`) to Control register `0x00`.
3. **Execution**:
   * `ap_start` initiates the computation. `ap_idle` drops to 0.
   * Accelerator computes result multivector and checks for overflow/saturation.
4. **Completion**:
   * Accelerator sets Result C coefficients in registers `0x80`–`0x9C`.
   * Accelerator updates Status register at `0x20` (setting `0x00` for OK, `0x04` for overflow, `0x01` for invalid opcode).
   * Accelerator pulses `ap_done` high for 1 clock cycle and returns to `ap_idle = 1`.
   * Host reads Status and Result C registers.
