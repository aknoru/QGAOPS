# Architectural Comparison: SEQ_GPU vs. PARALLEL_GPU

## 1. Comparative Overview

To establish an equitable evaluation, both `SEQ_GPU` and `PARALLEL_GPU` implement:
1. **Identical Mathematical Specification**: Euclidean $\text{Cl}(3,0)$ over 8 basis blades.
2. **Identical Numerical Rules**: Signed 32-bit Q16.16 fixed-point arithmetic with round-to-nearest-even rescaling and signed saturation clamp.
3. **Identical Top-Level Interface**: AXI4-Lite control, opcode, status, and multivector register mapping.
4. **Identical Verification Suite**: 100% shared test vectors covering all 12 operations, 64 basis pairs, and numeric edge cases.

---

## 2. Structural and Microarchitectural Comparison

| Dimension | `SEQ_GPU` (Sequential, Resource-Shared) | `PARALLEL_GPU` (Pipelined, Parallel) |
|:---|:---|:---|
| **Primary Design Objective** | Minimal area and DSP footprint | Maximum throughput and minimal execution latency |
| **Execution Paradigm** | Time-multiplexed iterative loops | Fully unrolled parallel adder trees and spatial stages |
| **HLS Loop Pragmas** | No unroll; sequential iteration; `INLINE off` submodules | `#pragma HLS PIPELINE II=1`, `#pragma HLS UNROLL` |
| **Array Partitioning** | None (standard array indexing) | `#pragma HLS ARRAY_PARTITION complete dim=1` on all operands |
| **Multipliers (DSP48)** | Time-shared (1 to 4 DSP slices) | Spatial parallel arrays (16 to 32 DSP slices) |
| **Geometric Product Latency** | $\sim 65$ to 80 clock cycles | $\sim 8$ to 14 clock cycles |
| **Sandwich Product Latency** | $\sim 140$ to 170 clock cycles | $\sim 18$ to 26 clock cycles |
| **Initiation Interval (II)** | $II = \text{Latency}$ (Non-pipelined core) | $II = 1$ to 4 cycles (Pipelined datapath) |
| **Resource Profile** | Very low LUT/FF footprint; suitable for resource-constrained tiles | Higher LUT/DSP footprint; optimizes real-time high-rate pipelines |
| **Target Application** | Low-power IoT / background gesture tracking | Real-time 4K video ray-casting, multi-hand 3D kinematics |

---

## 3. Microarchitectural Implementation Details

### 3.1 SEQ_GPU Datapath
In `SEQ_GPU`, the geometric product ($C = A B$) computes the 64 pairwise blade products using nested sequential loops:
```cpp
for (int left = 0; left < 8; left++) {
    for (int right = 0; right < 8; right++) {
        // Sequentially multiply blade pairs, update target blade accumulator
    }
}
```
This loop structure allows Vitis HLS to map the multiplication onto a single physical DSP48E1/E2 multiplier block, reusing it across clock cycles. Rescaling and saturation occur in a subsequent sequential loop pass.

### 3.2 PARALLEL_GPU Datapath
In `PARALLEL_GPU`, the 64 product terms are evaluated concurrently. Each of the 8 output blade accumulators receives a balanced binary summation tree:
* Blade 0 ($1$): Sum of 8 product terms ($a_0 b_0 + a_1 b_1 + a_2 b_2 + a_3 b_3 - a_4 b_4 - a_5 b_5 - a_6 b_6 - a_7 b_7$)
* Blades 1–3 ($e_i$): Parallel combination of vector, bivector, and pseudoscalar products.
* Blades 4–6 ($e_{ij}$): Parallel combinations yielding bivector components.
* Blade 7 ($e_{123}$): Tri-vector product combinations.

All 8 trees execute concurrently across pipelined stages, completing the entire multivector transformation in a fraction of the sequential latency.
