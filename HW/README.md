# QGAOPS-QGPU Hardware Implementation (Stages 9–10)

This directory contains the canonical Stage 9 (Hardware Interface and Architecture Design) and Stage 10 (Baseline HLS Accelerator) implementation for the QGAOPS-QGPU project.

## Directory Structure

```text
HW/
├── README.md                              # This file
├── architecture/
│   ├── stage9_hardware_architecture.md    # System architecture, PS/PL partitioning, target specifications
│   ├── interface_contract.md              # Register maps, opcodes, transaction semantics, AXI4-Lite ABI
│   ├── memory_fabric_design.md            # On-chip operand storage, buffering, and memory hierarchy
│   └── architecture_comparison.md         # Comparative analysis between SEQ_GPU and PARALLEL_GPU
├── hls/
│   ├── common/
│   │   ├── include/
│   │   │   ├── qgpu_types.h               # Cl(3,0) basis blade definitions, types, constants
│   │   │   ├── qgpu_operations.h          # Canonical opcode declarations and signatures
│   │   │   └── qgpu_fixed_point.h         # Q16.16 arithmetic, 67-bit accumulator, round-to-even, saturation
│   │   └── tests/
│   │       └── test_vectors.h             # Golden regression vectors generated from reference model
│   ├── SEQ_GPU/
│   │   ├── README.md                      # Component documentation, synthesis guidelines, GUI workflow
│   │   ├── src/
│   │   │   └── seq_gpu.cpp                # Sequential resource-shared HLS implementation
│   │   ├── include/
│   │   │   └── seq_gpu.h                  # SEQ_GPU top-level header and declarations
│   │   ├── testbench/
│   │   │   └── tb_seq_gpu.cpp             # Self-checking C++ verification testbench
│   │   └── reports/
│   │       └── README.md                  # Report capture instructions
│   └── PARALLEL_GPU/
│       ├── README.md                      # Component documentation, pragma analysis, GUI workflow
│       ├── src/
│       │   └── parallel_gpu.cpp           # Parallel pipelined HLS implementation with unrolled blades
│       ├── include/
│       │   └── parallel_gpu.h             # PARALLEL_GPU top-level header and declarations
│       ├── testbench/
│       │   └── tb_parallel_gpu.cpp        # Self-checking C++ verification testbench
│       └── reports/
│           └── README.md                  # Report capture instructions
├── verification/
│   ├── stage9_stage10_test_plan.md        # Comprehensive verification strategy and gates
│   ├── operation_coverage.md              # Coverage mapping for all 12 GA operations and 64 basis pairs
│   └── fixed_point_validation.md          # Bit-exact numeric precision, saturation, and rounding proofs
└── reports/
    └── stage9_stage10_status.md           # Stage 9/10 audit, implementation status, and verification log
```

## Architectural Overview

* **Algebra**: 3D Euclidean Geometric Algebra $\text{Cl}(3,0)$ over 8 basis blades:
  $$\{1, e_1, e_2, e_3, e_{12}, e_{13}, e_{23}, e_{123}\}$$
* **Numeric Representation**: Signed 32-bit Q16.16 fixed-point arithmetic with round-to-nearest-even tie breaking and signed saturation at $[-32768.0, +32767.99998474121]$ (`0x80000000` to `0x7FFFFFFF`).
* **Components**:
  1. `SEQ_GPU`: Sequential, resource-shared accelerator minimizing DSP48 and LUT footprint via time-multiplexed accumulation.
  2. `PARALLEL_GPU`: Fully unrolled, pipelined accelerator optimizing latency and throughput via parallel blade trees.
