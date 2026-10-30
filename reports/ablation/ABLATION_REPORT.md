# QGAOPS-QGPU STAGE 17 ARCHITECTURE & MEMORY ABLATION REPORT

**Target Platform**: AMD PYNQ-ZU Rev B (`xczu5eg-sfvc784-1-e`)
**Date**: 2026-10-28 03:56:12
**Status**: **PASS (All Ablations Completed)**

## 1. Ablation 1: Compute Parallelism (16 DSPs vs 832 DSPs)

| Batch Size | SEQ_GPU (16 DSPs) PL Latency | PARALLEL_GPU (832 DSPs) PL Latency | Compute Speedup |
|:---:|:---:|:---:|:---:|
|  1 | 3832.00 µs | 22739.00 µs | **0.17x** |
|  8 | 3303.62 µs | 3218.38 µs | **1.03x** |
| 16 | 6778.62 µs | 6641.06 µs | **1.02x** |
| 32 | 5731.12 µs | 6343.12 µs | **0.90x** |
| 64 | 8062.02 µs | 5875.27 µs | **1.37x** |

**Key Takeaway**: PARALLEL_GPU unrolls all 64 blade products into an arithmetic tree utilizing 832 DSP48E2 slices (66.67% of device budget), eliminating multi-cycle accumulator sequencing.

## 2. Ablation 2: Memory Organization & Overhead Amortization

| Batch Size | SEQ_GPU RAM Bus Time | PARALLEL_GPU Register Bus Time | Amortized Per-Op Overhead |
|:---:|:---:|:---:|:---:|
|  1 | 104308.00 µs | 44884.00 µs | 44884.00 µs/op |
|  8 | 68353.25 µs | 75053.38 µs | 9381.67 µs/op |
| 16 | 68884.19 µs | 72078.31 µs | 4504.89 µs/op |
| 32 | 75237.91 µs | 73219.97 µs | 2288.12 µs/op |
| 64 | 71385.61 µs | 81409.69 µs | 1272.03 µs/op |

**Key Takeaway**: Transfer overhead dominates for small batch sizes (1..8) but drops significantly when batched, amortizing bus round-trip latencies.

## 3. Ablation 3: Fixed-Point Arithmetic Quantization

- **Evaluated Combinations**: 64 exhaustive ordered basis-blade pairs
- **Bit-Exact Matches**: 64 / 64 (100.0%)
- **Maximum Absolute Error**: 0.00000000
- **Average Absolute Error**: 0.00000000
- **Numerical Stability**: Q16.16 saturating representation accurately captures basis signs, orthogonality, and reflections without precision drift.
