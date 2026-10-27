# QGAOPS-QGPU Software Demonstrator — Performance Metrics Specification

This document provides formal engineering definitions, mathematical formulations, measurement methodologies, and reporting classifications for all performance, bandwidth, memory, and accelerator metrics implemented in the **Live Hand Geometric Algebra Engine**.

---

## 1. Research-Grade Metric Classification Taxonomy

To ensure research integrity, every metric displayed in the GUI, emitted in logs, or written to reports is strictly categorized into one of four classes:

1. **`[MEASURED SOFTWARE]`**: Quantities measured directly using high-resolution hardware timers (`time.perf_counter_ns()`), OS kernel APIs (`psutil`), or direct image/buffer dimensions on the running host computer.
2. **`[SOFTWARE MODEL]`**: Conceptual execution and memory fabric simulations (e.g., AAMF B0–B5 logical DDR traffic, scratchpad reuse ratios) computed from active operation Directed Acyclic Graphs (DAGs).
3. **`[CALCULATED]`**: Mathematical derivations, statistical aggregations, or ratios computed from measured metrics (e.g., standard deviation, P95 latency, percentiles, arithmetic intensity).
4. **`[N/A — FPGA NOT CONNECTED]`**: Hardware register counters (LUT, FF, BRAM, DSP, Fmax, physical AXI bandwidth, on-chip power). These fields explicitly return `NOT_AVAILABLE` until physical ZedBoard / Zynq hardware is attached.

---

## 2. Comprehensive Metric Definitions

### 2.1 Frame & Timing Metrics

| Metric | Classification | Unit | Formula / Definition | Measurement Method |
|---|---|---|---|---|
| **Camera FPS** | `[MEASURED SOFTWARE]` | fps | $f_{\text{cam}} = \frac{N_{\text{frames}}}{t_{\text{elapsed}}}$ | Total frames captured divided by wall-clock duration |
| **Processing FPS** | `[CALCULATED]` | fps | $f_{\text{proc}} = \frac{1000}{t_{\text{frame\_ms}}}$ | Instantaneous inverse of single-frame processing time |
| **End-to-End FPS** | `[CALCULATED]` | fps | $f_{\text{e2e}} = \frac{N_{\text{recent}}}{\sum_{i=1}^{N} t_i / 1000}$ | Harmonic mean FPS over rolling 120-frame window |
| **Frame Latency** | `[MEASURED SOFTWARE]` | ms | $t_{\text{frame}} = \sum_{k \in \text{stages}} t_k$ | Sum of all pipeline stage durations in milliseconds |
| **P50 Latency (Median)** | `[CALCULATED]` | ms | $\text{Percentile}(L, 50)$ | 50th percentile of rolling frame latency buffer $L$ |
| **P95 Latency** | `[CALCULATED]` | ms | $\text{Percentile}(L, 95)$ | 95th percentile latency (evaluates tail latency) |
| **P99 Latency** | `[CALCULATED]` | ms | $\text{Percentile}(L, 99)$ | 99th percentile latency (evaluates worst-case jitter) |

### 2.2 Pipeline Stage Latencies

Each stage is timed via monotonic nanosecond timestamps:
$$\Delta t_{\text{stage}} = \frac{t_{\text{end\_ns}} - t_{\text{start\_ns}}}{10^6} \quad [\text{ms}]$$

1. **`camera_acquisition`**: Frame capture and buffer decode from OpenCV `cv2.VideoCapture`.
2. **`hand_detection`**: MediaPipe neural network hand-landmark detection inference.
3. **`landmark_normalization`**: Origin translation to wrist $\mathbf{p}_0$ and palm scaling.
4. **`feature_extraction`**: Computation of 107 normalized geometric invariants.
5. **`expression_classification`**: Random Forest inference over geometric features.
6. **`ga_encoding`**: Generation of G(3,0,0) multivectors and QGAOPS IR bytecode.
7. **`algebra_analysis`**: DAG dependency analysis and memory lifetime allocation.
8. **`ga_computation`**: Execution of GA primitive operations (GP, WEDGE, ROTOR, etc.).
9. **`visualization`**: Matplotlib 3D rasterization and GUI dashboard composition.

---

### 2.3 Throughput & Operations/Second

| Metric | Classification | Unit | Formula / Definition | Measurement Method |
|---|---|---|---|---|
| **GA_OPS/s** | `[CALCULATED]` | ops/s | $\text{OPS}_{\text{GA}} = \frac{N_{\text{GA\_completed}}}{t_{\text{elapsed}}}$ | Total completed Clifford algebra operations divided by elapsed time |
| **FRAME_OPS/s** | `[CALCULATED]` | ops/s | $\text{OPS}_{\text{Frame}} = \frac{N_{\text{frames}}}{t_{\text{elapsed}}}$ | Total end-to-end pipeline cycles per second |

> [!NOTE]
> **Operation Definition:** Exactly one elementary Geometric Algebra operation (e.g., 1 Geometric Product, 1 Wedge Product, 1 Rotor Sandwich Product) constitutes 1 GA operation. Python loop iterations or CPU instructions are never reported as GA operations.

---

### 2.4 Software Bandwidth Accounting

| Metric | Classification | Unit | Formula / Definition |
|---|---|---|---|
| **Input Bandwidth** | `[MEASURED SOFTWARE]` | MB/s | $\text{BW}_{\text{in}} = \frac{\sum \text{Bytes}_{\text{frame}} + \text{Bytes}_{\text{landmarks}}}{1024^2 \cdot \Delta t}$ |
| **Output Bandwidth** | `[MEASURED SOFTWARE]` | MB/s | $\text{BW}_{\text{out}} = \frac{\sum \text{Bytes}_{\text{mv\_out}} + \text{Bytes}_{\text{IR}}}{1024^2 \cdot \Delta t}$ |
| **Total Logical Bandwidth** | `[CALCULATED]` | MB/s | $\text{BW}_{\text{total}} = \text{BW}_{\text{in}} + \text{BW}_{\text{out}}$ |

*Label: `[SOFTWARE / LOGICAL BANDWIDTH]`. This accounts for internal memory buffer transfers within host RAM and does not represent physical PCIe or DDR hardware bandwidth.*

---

### 2.5 Software Memory Model (QGAOPS B0–B5 Fabric)

Simulates memory movement within the proposed Algebra-Aware Memory Fabric (AAMF):

| Metric | Classification | Unit | Formula / Definition |
|---|---|---|---|
| **B0 Logical DDR Bytes** | `[SOFTWARE MODEL]` | Bytes | $B_0 = N_{\text{ops}} \times (2 \times 32 + 32) = 96 \times N_{\text{ops}}$ |
| **B5 Logical DDR Bytes** | `[SOFTWARE MODEL]` | Bytes | $B_5 = \text{Unique\_Inputs} \times 32 + \text{Final\_Outputs} \times 32$ |
| **Scratchpad Accesses** | `[SOFTWARE MODEL]` | Accesses | Count of fast on-chip BRAM / register file reads and writes |
| **Reuse Ratio** | `[CALCULATED]` | % | $R = \frac{B_0 - B_5}{B_0} \times 100\%$ |
| **Arithmetic Intensity** | `[CALCULATED]` | ops/byte | $I_{\text{arith}} = \frac{N_{\text{ops}}}{B_5}$ |

---

### 2.6 System Resource Metrics

| Metric | Classification | Unit | Measurement API |
|---|---|---|---|
| **CPU Utilization** | `[MEASURED SOFTWARE]` | % | `psutil.Process().cpu_percent()` |
| **Process RAM (RSS)** | `[MEASURED SOFTWARE]` | MB | `psutil.Process().memory_info().rss / (1024^2)` |
| **System RAM** | `[MEASURED SOFTWARE]` | MB | `psutil.virtual_memory().used / (1024^2)` |

---

### 2.7 Classifier Evaluation Metrics

| Metric | Classification | Formula | Range |
|---|---|---|---|
| **Accuracy** | `[CALCULATED]` | $\frac{TP + TN}{TP + TN + FP + FN}$ | $[0.0, 1.0]$ |
| **Precision (Weighted)** | `[CALCULATED]` | $\sum_c w_c \frac{TP_c}{TP_c + FP_c}$ | $[0.0, 1.0]$ |
| **Recall (Weighted)** | `[CALCULATED]` | $\sum_c w_c \frac{TP_c}{TP_c + FN_c}$ | $[0.0, 1.0]$ |
| **F1-Score** | `[CALCULATED]` | $2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}$ | $[0.0, 1.0]$ |

---

### 2.8 Fixed-Point Numerical Accuracy

| Metric | Classification | Formula | Description |
|---|---|---|---|
| **Max Absolute Error** | `[CALCULATED]` | $\max_i \|f_i - q_i\|$ | Maximum coefficient deviation between Float32 and FIX16 |
| **RMS Error** | `[CALCULATED]` | $\sqrt{\frac{1}{8} \sum_{i=0}^7 (f_i - q_i)^2}$ | Root-mean-square error across multivector coefficients |

---

### 2.9 Future Physical FPGA Counter Placeholders

All hardware accelerator registers return explicit non-fabricated status:
- **`LUT`**: `N/A — FPGA not connected`
- **`FF`**: `N/A — FPGA not connected`
- **`BRAM`**: `N/A — FPGA not connected`
- **`DSP`**: `N/A — FPGA not connected`
- **`Fmax`**: `N/A — FPGA not synthesized`
- **`Hardware Cycles`**: `N/A — FPGA not connected`
- **`On-Chip Power`**: `N/A — FPGA not connected`
- **`Energy / Op`**: `N/A — FPGA not connected`
