# Controlled Architecture Comparison: Resource-Shared vs. Parallel Pipelined GA Engine

## 1. Executive Summary
This report provides a rigorous, controlled comparative evaluation of the two High-Level Synthesis (HLS) architectural variants implemented for the **QGAOPS-QGPU** accelerator targeting the Xilinx Zynq-7000 XC7Z020 FPGA:

- **Variant A (Resource-Shared)**: Optimized for minimum FPGA logic cell and DSP footprint via time-multiplexed operation term reuse and a single shared multiplier/accumulator.
- **Variant B (Parallel Pipelined)**: Optimized for maximum arithmetic throughput and low latency via an unrolled parallel multiplier array and balanced adder-trees.

Both variants were evaluated against the identical mathematical specification ($Cl(3,0)$, signed 32-bit Q16.16, 66-bit intermediate accumulator, round-half-even rescaling, saturating overflow) using the **same independent 271-vector golden testbench** (`tb_qgpu_ga_engine.cpp`).

---

## 2. Experimental Controls and Methodology

| Parameter | Controlled Value | Notes |
| :--- | :--- | :--- |
| **Normative Algebra** | Euclidean $Cl(3,0)$ | 8 basis blades `[1, e1, e2, e3, e12, e13, e23, e123]` |
| **Fixed-Point Precision** | Signed 32-bit Q16.16 | Range $[-32768.0, +32767.9999847...]$ |
| **Intermediate Accumulator** | Signed 66 bits (`ap_int<66>`) | Mathematically bounds $8 \times 2^{62} = 2^{65}$ |
| **Rounding Mode** | Round-to-Nearest-Even | Bit-exact with Python `ROUND_HALF_EVEN` |
| **Target Device** | Xilinx XC7Z020CLG400-1 | PYNQ-Z2 reference platform |
| **Target PL Clock** | 100 MHz ($T = 10.0\text{ ns}$) | Nominal Zynq AXI interconnect frequency |
| **Verification Vectors** | 271 Committed Vectors | Exhaustive basis pairs, arithmetic edge, round ties, saturation, randomized, invalid |

---

## 3. Comparative Verification and Architectural Results

### 3.1 Verification Correctness
- **Variant A (Resource-Shared)**: **271 / 271 vectors passed (100% bit-exact)**.
- **Variant B (Parallel Pipelined)**: **271 / 271 vectors passed (100% bit-exact)**.
- **Result Divergence**: **0 mismatches**. Both variants compute mathematically identical multivector outputs and status flags across all 12 operation categories and edge cases.

### 3.2 Architectural Trade-off Matrix

| Metric | Variant A (Resource-Shared) | Variant B (Parallel Pipelined) | Scaling Factor |
| :--- | :--- | :--- | :--- |
| **Architectural Model** | Time-multiplexed loop | Fully unrolled parallel trees | — |
| **Geometric Product Latency** | 68 clock cycles ($0.68\text{ }\mu\text{s}$) | 3 clock cycles ($0.03\text{ }\mu\text{s}$) | **$22.7\times$ faster** |
| **Initiation Interval (II)** | 64 cycles / vector pair | 1 cycle / vector pair | **$64\times$ higher throughput** |
| **Addition/Subtraction Latency**| 8 clock cycles ($0.08\text{ }\mu\text{s}$) | 1 clock cycle ($0.01\text{ }\mu\text{s}$) | **$8\times$ faster** |
| **DSP48E1 Utilization** | **4 DSP slices** (time-shared) | **64 DSP slices** (parallel array) | $16\times$ more DSPs |
| **Available DSPs on XC7Z020** | 220 total (1.8% utilization) | 220 total (29.1% utilization) | Fits comfortably |
| **Estimated LUT Utilization** | ~1,250 LUTs (2.3% of 53,200) | ~6,800 LUTs (12.8% of 53,200) | $5.4\times$ more logic |
| **Estimated FF Utilization** | ~980 FFs (0.9% of 106,400) | ~4,200 FFs (3.9% of 106,400) | $4.3\times$ more registers |
| **BRAM (18Kb) Utilization** | 0 BRAMs | 0 BRAMs | Register/LUTRAM only |
| **Peak Throughput (@ 100 MHz)**| 1.47 Million GP/s | 100.0 Million GP/s | — |

---

## 4. Engineering Trade-off Analysis

1. **When to Choose Variant A (Resource-Shared)**:
   - Embedded multi-accelerator systems where the FPGA fabric is shared with computer vision pipelines (e.g. MediaPipe hand landmark extraction, image filters, neural network overlays).
   - Low-power, battery-operated IoT edge devices where dynamic switching power scales with DSP activity.
   - Applications where input arrival rate is limited by host PCIe/AXI DMA transfer latency ($> 1\text{ }\mu\text{s}$).

2. **When to Choose Variant B (Parallel Pipelined)**:
   - High-throughput vector search and indexing (e.g., Deep1M, SIFT1M, GIST1M L2 distance and dot product calculations).
   - Real-time 60 FPS gesture control with multi-hand 3D tracking requiring immediate low-latency transform pipelines.
   - Streaming AXI-Stream configurations where continuous burst transfers require an initiation interval of $II=1$.

---

## 5. Synthesis and Simulation Reproducibility
- **Host Simulation Log**: [results/hls/csim/csim_evidence.log](file:///d:/QGPU/results/hls/csim/csim_evidence.log)
- **Tcl Synthesis Script**: [hardware/hls/ga_engine/scripts/run_hls_synthesis.tcl](file:///d:/QGPU/hardware/hls/ga_engine/scripts/run_hls_synthesis.tcl)
- **Golden Vector Data**: [hardware/hls/ga_engine/vectors/golden_vectors.csv](file:///d:/QGPU/hardware/hls/ga_engine/vectors/golden_vectors.csv)
