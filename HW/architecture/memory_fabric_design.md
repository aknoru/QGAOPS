# Memory Fabric and Storage Hierarchy Design

## 1. Storage Resource Classification and Allocation

This document specifies the exact physical storage resources utilized by `SEQ_GPU` and `PARALLEL_GPU`, distinguishing between synthesized on-chip register storage, intermediate pipeline buffers, and future Block RAM (BRAM18K) batch memories.

```
+-----------------------------------------------------------------------------+
|                          MEMORY HIERARCHY ARCHITECTURE                      |
|                                                                             |
|  [Host L1/L2 DDR4 Memory via PS]                                            |
|       |                                                                     |
|       v (AXI4-Lite Bus Access)                                              |
|  [AXI Slave Register Banks (64 Bytes Operands + 32 Bytes Results)]          |
|       |                                                                     |
|       +-------------------------------+------------------------------+      |
|       |                               |                              |      |
|       v                               v                              |      |
|  [SEQ_GPU Local Storage]        [PARALLEL_GPU Local Storage]         |      |
|  - Time-shared Register File    - Fully Partitioned Register Array   |      |
|  - Single 67-bit Accumulator    - 8 Independent 67-bit Accumulators  |      |
|  - In-place Temporary Buffer     - Balanced Pipeline Retiming Stage  |      |
|       |                               |                              |      |
|       +-------------------------------+------------------------------+      |
|                                       |                                     |
|  [Future Batch Memory Extension: Algebra-Aware Memory Fabric (AAMF)]        |
|  - 2x BRAM18K True Dual-Port Memory (64 Multivectors / Bank)                |
|  - (Documented as an architectural path; not inferred in single-step core)  |
+-----------------------------------------------------------------------------+
```

---

## 2. Kernel-Level Storage Implementation

### 2.1 SEQ_GPU Storage Design
In `SEQ_GPU`, the priority is minimal logic utilization and maximum resource sharing:
* **Operand Registers**: Operands $A$ and $B$ are stored in two 8-element 32-bit registers ($2 \times 8 \times 32\text{ bits} = 512\text{ bits}$ of distributed flip-flops).
* **Accumulator Storage**: Rather than instantiating 8 physical accumulators, `SEQ_GPU` uses an internal 8-element 67-bit temporary accumulator array (`accum[8]`), sequentially visited by an iterative state machine loop.
* **Compound Operations (Sandwich Product)**: For operations requiring sequential composition ($C = A B \widetilde{A}$), a single 8-element 32-bit temporary multivector register (`temp[8]`) holds the intermediate product $T = A B$ before feeding into $T \widetilde{A}$.
* **Hardware Cost**: Zero BRAM blocks are consumed; all storage is realized as distributed slice registers (FFs) and LUT-RAM.

### 2.2 PARALLEL_GPU Storage Design
In `PARALLEL_GPU`, the priority is high throughput and low initiation interval (II):
* **Partitioned Storage**: Operand arrays $A$, $B$, and result array $C$ are fully partitioned via `#pragma HLS ARRAY_PARTITION variable=... complete dim=1`.
* **Multiplexing Removal**: Partitioning completely eliminates RAM multiplexing overhead, transforming the array into 8 parallel 32-bit discrete registers directly feeding 8 parallel tree-adder networks.
* **Accumulator Trees**: 8 parallel 67-bit accumulation networks compute all 8 output blades concurrently within a single pipelined pass.
* **Hardware Cost**: 0 BRAM blocks are consumed in the core; logic utilizes approximately $3\times$ to $5\times$ more Flip-Flops and LUTs than `SEQ_GPU` to maintain parallel register bandwidth.

---

## 3. Explicit Clarification Regarding Block RAM (BRAM) Inference

> [!IMPORTANT]
> **No Fabricated BRAM Claims**:
> In Vitis HLS, an array of 8 words of 32 bits ($8 \times 4\text{ bytes} = 32\text{ bytes}$) is too small for Vivado to infer a dedicated Block RAM (a single BRAM18K slice contains 18,432 bits). Therefore, when synthesized as a standalone single-multivector core, **both `SEQ_GPU` and `PARALLEL_GPU` synthesize strictly into distributed Slice Flip-Flops and LUT-RAM, consuming 0 Block RAM (BRAM18K = 0)**.
>
> Any claim that a single 8-word multivector accelerator infers BRAM is physically incorrect and rejected.

---

## 4. Architectural Path to Memory-Centric Batch Acceleration (AAMF)

When extended to batch processing (e.g. processing $N = 64$ hand landmark vectors per video frame):
* An **Algebra-Aware Memory Fabric (AAMF)** is configured using dual-port on-chip BRAM18K blocks:
  * **Bank A**: 64 Multivectors $\times$ 8 blades $\times$ 32 bits $= 16,384\text{ bits}$ (fits in 1 BRAM18K).
  * **Bank B**: 64 Multivectors $\times$ 8 blades $\times$ 32 bits $= 16,384\text{ bits}$ (fits in 1 BRAM18K).
  * **Bank C (Results)**: 64 Multivectors $\times$ 8 blades $\times$ 32 bits $= 16,384\text{ bits}$ (fits in 1 BRAM18K).
* In this configuration, the host writes entire frames of multivectors into BRAM, and the compute core executes over the BRAM with burst efficiency.
