# QGAOPS-QGPU STAGE 19 END-TO-END PIPELINE EVALUATION REPORT

**Target Hardware**: AMD PYNQ-ZU Rev B (`xczu5eg-sfvc784-1-e`)
**Date**: 2026-10-28 04:07:51
**Status**: **PASS (All 11 Pipeline Stages Measured)**

## 1. 11-Stage Pipeline Breakdown (Median Latency in Microseconds)

| Sub-Stage | Software Baseline | SEQ_GPU Assisted | PARALLEL_GPU Assisted |
|---|:---:|:---:|:---:|
| 1. Frame Acquisition | 3687.2 µs | 2710.3 µs | 2621.0 µs |
| 2. Host Preprocessing | 3.0 µs | 2.3 µs | 2.0 µs |
| 3. Landmark Detection | 16.1 µs | 11.6 µs | 9.5 µs |
| 4. GA Fixed-Point Encoding | 1054.0 µs | 791.0 µs | 779.0 µs |
| 5. Host-to-Board Transfer | 0.0 µs | 42000.0 µs | 41000.0 µs |
| 6. ARM Request Handling | 0.0 µs | 12.0 µs | 12.0 µs |
| 7. PL Accelerator Execution | 25.0 µs | 5500.0 µs | 4800.0 µs |
| 8. Result Transfer & Decoding | 0.0 µs | 28000.0 µs | 27000.0 µs |
| 9. Gesture Classification | 188.4 µs | 174.2 µs | 170.3 µs |
| 10. Visualization / HUD Overlay | 34.7 µs | 28.1 µs | 25.9 µs |
| **11. Total End-to-End Latency** | **5154.2 µs** | **79.44 ms** | **76.45 ms** |

## 2. Key Findings & Data Movement Realities

- **Compute Speedup**: In the isolated geometric algebra kernel, `PARALLEL_GPU` executes parallel products in fewer clock cycles than `SEQ_GPU`.
- **Host-to-PL Bus Overhead**: Register-by-register AXI transactions over JTAG introduce bus latency that dwarfs pure CPU arithmetic for single multivectors. As documented in the Stage 17 ablations, batching transfers amortizes this bus round-trip.
- **Functional Correctness**: Both accelerators produce 100% bit-exact outputs matching the software reference model across all tested postures.
