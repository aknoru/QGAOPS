# QGAOPS-QGPU System Requirements Specification

## 1. Research Hypothesis and Objectives

### Primary Research Hypothesis
An algebra-aware memory organization and dedicated fixed-point arithmetic datapath for Euclidean Clifford algebra $Cl(3,0)$ can provide a deterministic, measurable area, latency, and energy trade-off compared to general-purpose CPU SIMD architectures when executing geometric algebra kernels on resource-constrained embedded FPGA platforms (specifically the Xilinx Zynq-7000 XC7Z020 on the PYNQ-Z2 board).

### Measurable Evaluation Metrics
To preserve rigorous research integrity, all performance claims are stratified strictly by execution tier:
1. **[MEASURED-SOFTWARE]**: Real execution on host x86_64 CPU (AMD/Intel) running Python 3.13 / NumPy reference and optimized C++ kernels.
2. **[SIMULATED-HLS]**: Cycle-accurate cycle counts, initiation interval (II), and execution latency reported by Vitis HLS C simulation and C/RTL co-simulation.
3. **[SYNTHESIS-ESTIMATE]**: Resource utilization (LUTs, FFs, DSP48E1 slices, BRAMs) and maximum operating clock frequency ($F_{\text{max}}$) estimated by Vitis HLS and Vivado Logic Synthesis for the `xc7z020clg400-1` target part.
4. **[PHYSICAL-HARDWARE]**: Real on-chip hardware execution measured via AXI transaction timers on a physical PYNQ-Z2 board (Target Phase; labeled `NOT_CONNECTED` until physically deployed).

---

## 2. Normative Mathematical & Numerical Requirements

- **Algebraic Basis (REQ-MATH-01)**: Euclidean $Cl(3,0)$ with orthogonal basis vectors satisfying $e_1^2 = e_2^2 = e_3^2 = +1$.
- **Basis Blade Ordering (REQ-MATH-02)**: The normative coefficient vector must strictly follow the canonical 8-blade order:
  $$\mathbf{x} = [x_0, x_1, x_2, x_3, x_4, x_5, x_6, x_7] \equiv x_0 1 + x_1 e_1 + x_2 e_2 + x_3 e_3 + x_4 e_{12} + x_5 e_{13} + x_6 e_{23} + x_7 e_{123}$$
  Bitmask encoding: $1 \to 000_2, e_1 \to 001_2, e_2 \to 010_2, e_3 \to 100_2, e_{12} \to 011_2, e_{13} \to 101_2, e_{23} \to 110_2, e_{123} \to 111_2$.
- **Numerical Format (REQ-NUM-01)**: Primary hardware and fixed-point reference format is signed 32-bit Q16.16 (`ap_fixed<32, 16>`):
  - 1 sign bit, 15 integer bits, 16 fractional bits.
  - Scale factor: $2^{16} = 65536$.
  - Numerical range: $[-32768.0, +32767.9999847...]$.
  - Rounding mode: Round-to-nearest-even (`ROUND_HALF_EVEN`).
  - Overflow handling: Explicit saturating arithmetic with sticky overflow status reporting.
- **Accumulator Bit-Width Derivation (REQ-NUM-02)**:
  - Product of two signed 32-bit integers yields up to 62 bits of magnitude plus sign (requires 64 bits).
  - Geometric product accumulation sums up to 8 product terms per output coefficient ($8 \times 2^{62} = 2^{65}$).
  - A signed **66-bit accumulator** (`ap_int<66>`, range $[-2^{65}, +2^{65}-1]$) mathematically guarantees zero intermediate overflow during multivector multiplication before rescaling.

---

## 3. Mandatory Operation Coverage

The system must support the complete suite of 12 geometric algebra operations:
1. `ADD`: Multivector addition ($\mathbf{A} + \mathbf{B}$)
2. `SUBTRACT`: Multivector subtraction ($\mathbf{A} - \mathbf{B}$)
3. `GEOMETRIC_PRODUCT`: Full Clifford multiplication ($\mathbf{A}\mathbf{B}$)
4. `WEDGE`: Outer/wedge product ($\mathbf{A} \wedge \mathbf{B}$)
5. `HESTENES_INNER`: Hestenes inner product ($\mathbf{A} \cdot \mathbf{B}$) where grade restriction $k = |s - r|$ applies
6. `SCALAR_MUL`: Uniform scaling of all 8 multivector coefficients
7. `GRADE_PROJ`: Projection to homogeneous grade $k \in \{0, 1, 2, 3\}$
8. `REVERSE`: Multivector reversion ($\widetilde{\mathbf{A}} = \sum (-1)^{k(k-1)/2} \langle \mathbf{A} \rangle_k$)
9. `GRADE_INVOLUTION`: Parity involution ($\widehat{\mathbf{A}} = \sum (-1)^k \langle \mathbf{A} \rangle_k$)
10. `CLIFFORD_CONJ`: Clifford conjugation ($\overline{\mathbf{A}} = \widetilde{\widehat{\mathbf{A}}}$)
11. `ROTOR_GEN_NORM`: Rotor generation from bivector angle and normalization ($\mathbf{R} = \exp(-B/2)$)
12. `SANDWICH`: Rotor coordinate transformation ($\mathbf{v}' = \mathbf{R} \mathbf{v} \widetilde{\mathbf{R}}$)

---

## 4. Multi-Dataset Integration & GA Mapping Requirements

- **Leap Hand Gesture Recognition (REQ-DATA-01)**:
  - Format: 21 3D landmarks (63 coordinates) and pre-extracted feature vectors.
  - Classification: 27-pose dynamic and static hand expressions.
  - Metrics: Train/validation/test split accuracy, macro-F1, confusion matrix, per-class precision and recall.
- **Deep1M, SIFT1M, GIST1M (REQ-DATA-02)**:
  - Deep1M: 96-dimensional neural embedding vectors.
  - SIFT1M: 128-dimensional local image descriptor vectors.
  - GIST1M: 960-dimensional holistic scene descriptor vectors.
- **Dimension-Preserving GA Mapping (REQ-DATA-03)**:
  - High-dimensional $D$-vector $\mathbf{V} \in \mathbb{R}^D$ is partitioned into $\lceil D/3 \rceil$ triplets.
  - Each triplet $(v_{3i}, v_{3i+1}, v_{3i+2})$ is encoded as a grade-1 spatial vector $\mathbf{u}_i = v_{3i}e_1 + v_{3i+1}e_2 + v_{3i+2}e_3 \in Cl(3,0)$.
  - Any partial trailing group is zero-padded without altering mathematical norms.
  - Euclidean distance is computed by summing the squared multivector norms:
    $$\|\mathbf{V} - \mathbf{W}\|_2^2 = \sum_{i=0}^{\lceil D/3 \rceil - 1} \langle (\mathbf{u}_i - \mathbf{w}_i)(\mathbf{u}_i - \mathbf{w}_i)^\dagger \rangle_0$$
  - Exact equivalence with standard NumPy L2 distance must be maintained across all dimensions.

---

## 5. Hardware Interface and HLS Kernel Architecture

- **Target Device (REQ-HW-01)**: Xilinx Zynq-7000 XC7Z020 (`xc7z020clg400-1`), 100 MHz target PL clock ($T = 10.0\text{ ns}$).
- **Control Interface (REQ-HW-02)**: AXI4-Lite slave (`s_axilite`) providing:
  - `0x00`: Control register (`AP_START`, `AP_DONE`, `AP_IDLE`, `AP_READY`)
  - `0x10`: Opcode selection (1=GP, 2=WEDGE, 3=INNER, 4=ADD, 5=SUB)
  - `0x18`: Status / error register (overflow sticky flag, invalid opcode)
  - `0x20 - 0x3C`: 8 $\times$ 32-bit input operand A
  - `0x40 - 0x5C`: 8 $\times$ 32-bit input operand B
  - `0x60 - 0x7C`: 8 $\times$ 32-bit output result C
- **Architectural Variants (REQ-HW-03)**:
  - **Variant A (Resource-Shared)**: Time-multiplexed loop over the 64 product terms, single pipelined DSP multiplier and 66-bit accumulator to minimize FPGA area.
  - **Variant B (Parallel)**: Fully unrolled parallel multiplier array and pipelined adder-tree computing 8 output coefficients simultaneously with minimal initiation interval.
