# PARALLEL_GPU: Parallel Pipelined Geometric Algebra Accelerator

## 1. Component Overview

* **Component Name**: `PARALLEL_GPU`
* **Top-Level Function**: `parallel_gpu`
* **Hardware Paradigm**: Parallel, pipelined execution model with spatial blade reduction trees.
* **Algebra**: $\text{Cl}(3,0)$ over 8 basis blades $\{1, e_1, e_2, e_3, e_{12}, e_{13}, e_{23}, e_{123}\}$.
* **Arithmetic**: Signed 32-bit Q16.16 fixed-point arithmetic with round-to-nearest-even rescaling and signed boundary saturation.
* **Target Device**: AMD/Xilinx Zynq UltraScale+ MPSoC `xczu5eg-sfvc784-1-e` (or Zynq-7000 `xc7z020clg400-1`).
* **Target Clock**: $100\text{ MHz}$ ($10.0\text{ ns}$ clock period, $2.7\text{ ns}$ uncertainty for UltraScale+; $1.5\text{ ns}$ for Zynq-7000).

---

## 2. Source Files and Structure

```text
HW/hls/PARALLEL_GPU/
├── README.md                      # This manual and component specification
├── include/
│   └── parallel_gpu.h             # Top-level function prototypes and declarations
├── src/
│   └── parallel_gpu.cpp           # Parallel pipelined synthesizable C++ implementation
├── testbench/
│   └── tb_parallel_gpu.cpp        # Self-checking C++ verification testbench
└── reports/
    └── README.md                  # Report capture location and metric instructions
```

---

## 3. Microarchitecture and Pragma Analysis

`PARALLEL_GPU` is designed for high-performance applications where cycle latency and pipelining throughput are prioritized over silicon area:

### 3.1 Complete Array Partitioning
```cpp
#pragma HLS ARRAY_PARTITION variable=a complete dim=1
#pragma HLS ARRAY_PARTITION variable=b complete dim=1
#pragma HLS ARRAY_PARTITION variable=c complete dim=1
```
* **Rationale**: In standard C arrays, memory elements are mapped to single- or dual-port RAMs, allowing at most 2 simultaneous accesses per cycle. By completely partitioning the 8-blade arrays into discrete flip-flop registers, all 8 coefficients of $A$ and 8 coefficients of $B$ can be read simultaneously in parallel.
* **Cost**: Increases multiplexer and register routing overhead.

### 3.2 Parallel Blade Trees and Loop Unrolling
```cpp
#pragma HLS UNROLL
```
* **Rationale**: Applied to the 8 output blade accumulation networks (`PARALLEL_BLADE_LOOP` and `PARALLEL_SUM_TREE`). Each blade accumulator evaluates all 8 contributing bilinear product terms concurrently using balanced adder trees.
* **Cost**: Instantiates 64 parallel multiplication terms mapped to available DSP48E1/E2 slices.

### 3.3 Pipelined Datapath
```cpp
#pragma HLS PIPELINE II=1
```
* **Rationale**: Enforces an Initiation Interval of 1 cycle ($II=1$) for point-to-point vector operations (addition, subtraction, scaling) and minimizes pipeline depth for multivector products to $\sim 8$ to 12 clock cycles.

### 3.4 Dataflow Optimization for Sandwich Product
```cpp
#pragma HLS DATAFLOW
```
* **Rationale**: In the rotor sandwich transformation ($C = A B \widetilde{A}$), stage 1 ($T = A B$ and $A_{\text{rev}} = \widetilde{A}$) and stage 2 ($C = T A_{\text{rev}}$) execute in overlapping dataflow pipelines, reducing latency to $\sim 20$ clock cycles.

---

## 4. Manual Vitis HLS GUI Workflow (No Tcl Scripts Required)

Follow these exact steps in the Vitis HLS GUI (tested for AMD Vitis 2025.2 / 2024.x / 2023.x):

### Step 1: Launch Vitis HLS
Launch Vitis HLS from the Start Menu or command prompt:
```bat
C:\AMDDesignTools\2025.2\Vitis\bin\vitis_hls.bat
# or in the unified environment:
vitis -hls
```

### Step 2: Create a New HLS Component
1. On the Vitis Welcome screen, click **Create HLS Component** (or **File** $\rightarrow$ **New Component** $\rightarrow$ **HLS**).
2. Set **Component name**: `PARALLEL_GPU`.
3. Set **Component location**: Select a workspace directory (e.g. `d:/QGPU/HW/hls/PARALLEL_GPU/workspace`). Click **Next**.

### Step 3: Add Source and Header Files
1. In the **Design Files** section, click **Add Files...** and browse to:
   * `d:/QGPU/HW/hls/PARALLEL_GPU/src/parallel_gpu.cpp`
2. In the **Top Function** box, click **Browse...** and select `parallel_gpu`.
3. In **Include Paths**, click **Add...** and add:
   * `d:/QGPU/HW/hls/common/include`
   * `d:/QGPU/HW/hls/PARALLEL_GPU/include`
4. In **CFLAGs**, enter: `-std=c++14 -I d:/QGPU/HW/hls/common/include -I d:/QGPU/HW/hls/PARALLEL_GPU/include`. Click **Next**.

### Step 4: Add Testbench Files
1. In the **Testbench Files** section, click **Add Files...** and browse to:
   * `d:/QGPU/HW/hls/PARALLEL_GPU/testbench/tb_parallel_gpu.cpp`
2. In **Testbench CFLAGs**, enter: `-std=c++14 -I d:/QGPU/HW/hls/common/include -I d:/QGPU/HW/hls/PARALLEL_GPU/include`. Click **Next**.

### Step 5: Configure Target Part and Clock
1. In the **Hardware** / **Part Selection** step:
   * For **PYNQ-ZU / Zynq UltraScale+**: Search for and select part `xczu5eg-sfvc784-1-e`.
   * For **PYNQ-Z2 / Zynq-7000**: Search for and select part `xc7z020clg400-1`.
2. In **Clock Settings**:
   * **Clock Period**: `10` ns ($100\text{ MHz}$).
   * **Clock Uncertainty**: `2.7` ns (for UltraScale+) or `1.5` ns (for Zynq-7000).
3. In **Flow Target**: Select `Vivado IP Flow`.
4. Click **Finish**.

### Step 6: Run C Simulation
1. In the Flow navigator on the left, click **C SIMULATION** $\rightarrow$ **Run**.
2. Select **Optimized Mode** or **Debug Mode**, ensure **Clean Build** is checked.
3. Click **OK**.
4. In the Console, verify that all 285 regression tests execute and pass:
   ```text
   ==================================================================
     PARALLEL_GPU VERIFICATION SUMMARY
     Total Tested: 285
     PASSED:       285
     FAILED:       0
   ==================================================================
   >>> RESULT: ALL PARALLEL_GPU TESTS PASSED SUCCESSFULLY! <<<
   ```

### Step 7: Run C Synthesis
1. In the Flow navigator, click **C SYNTHESIS** $\rightarrow$ **Run**.
2. When synthesis finishes, the **Synthesis Summary Report** opens automatically.
3. Inspect key performance and area metrics:
   * **Timing**: Target $10.0\text{ ns}$, Estimated clock period $< 8.5\text{ ns}$ (slack met).
   * **Latency**: Geometric product latency $\sim 8$ to 12 cycles, sandwich product $\sim 20$ to 26 cycles.
   * **Resource Utilization**: BRAM: $0$, DSP: $\sim 16$ to 32, FF: moderate, LUT: moderate.

### Step 8: Save Reports
Save the synthesis report from:
`<workspace>/PARALLEL_GPU/solution1/syn/report/parallel_gpu_csynth.rpt`
into:
`d:/QGPU/HW/hls/PARALLEL_GPU/reports/`

### Step 9: Export IP (When Ready)
1. In the Flow navigator, click **PACKAGE** $\rightarrow$ **Run**.
2. Set Format to **IP Catalog**, Vendor: `QGAOPS`, Library: `QGPU`, Version: `1.0`.
3. The exported zip will be located in `<workspace>/PARALLEL_GPU/solution1/impl/ip/`.
