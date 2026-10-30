# SEQ_GPU: Sequential Resource-Shared Geometric Algebra Accelerator

## 1. Component Overview

* **Component Name**: `SEQ_GPU`
* **Top-Level Function**: `seq_gpu`
* **Hardware Paradigm**: Sequential, resource-shared execution model.
* **Algebra**: $\text{Cl}(3,0)$ over 8 basis blades $\{1, e_1, e_2, e_3, e_{12}, e_{13}, e_{23}, e_{123}\}$.
* **Arithmetic**: Signed 32-bit Q16.16 fixed-point arithmetic with round-to-nearest-even rescaling and signed boundary saturation.
* **Target Device**: AMD/Xilinx Zynq UltraScale+ MPSoC `xczu5eg-sfvc784-1-e` (or Zynq-7000 `xc7z020clg400-1`).
* **Target Clock**: $100\text{ MHz}$ ($10.0\text{ ns}$ clock period, $2.7\text{ ns}$ uncertainty for UltraScale+; $1.5\text{ ns}$ for Zynq-7000).

---

## 2. Source Files and Structure

```text
HW/hls/SEQ_GPU/
├── README.md                      # This manual and component specification
├── include/
│   └── seq_gpu.h                  # Top-level function prototypes and declarations
├── src/
│   └── seq_gpu.cpp                # Sequential synthesizable C++ implementation
├── testbench/
│   └── tb_seq_gpu.cpp             # Self-checking C++ verification testbench
└── reports/
    └── README.md                  # Report capture location and metric instructions
```

---

## 3. Microarchitecture and Resource-Sharing Rationale

`SEQ_GPU` is designed to minimize FPGA slice and DSP footprint by executing multivector operations sequentially over time:
1. **Time-Multiplexed Product**: Rather than implementing 64 parallel hardware multipliers, the geometric product ($C = A B$) sequentially iterates through an outer loop ($left = 0 \dots 7$) and inner loop ($right = 0 \dots 7$).
2. **Shared Accumulator**: A single 67-bit intermediate accumulator buffer is iteratively updated, guaranteeing zero intermediate truncation without replicating wide addition trees.
3. **Dedicated Submodules with `INLINE off`**: Submodule routines (`seq_product_core`, `seq_op_add`, `seq_op_sub`, `seq_op_scalar_mul`, `seq_op_grade_proj`, `seq_op_reverse`, `seq_op_grade_involution`, `seq_op_clifford_conj`, `seq_op_rotor_norm`, `seq_op_sandwich`) are decorated with `#pragma HLS INLINE off`. This ensures distinct hardware module boundaries in synthesis reports and Vitis Analyzer call graphs.
4. **No Unroll Directives**: Loops run strictly iteratively, maximizing hardware reuse.

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
2. Set **Component name**: `SEQ_GPU`.
3. Set **Component location**: Select a workspace directory (e.g. `d:/QGPU/HW/hls/SEQ_GPU/workspace`). Click **Next**.

### Step 3: Add Source and Header Files
1. In the **Design Files** section, click **Add Files...** and browse to:
   * `d:/QGPU/HW/hls/SEQ_GPU/src/seq_gpu.cpp`
2. In the **Top Function** box, click **Browse...** and select `seq_gpu`.
3. In **Include Paths**, click **Add...** and add:
   * `d:/QGPU/HW/hls/common/include`
   * `d:/QGPU/HW/hls/SEQ_GPU/include`
4. In **CFLAGs**, enter: `-std=c++14 -I d:/QGPU/HW/hls/common/include -I d:/QGPU/HW/hls/SEQ_GPU/include`. Click **Next**.

### Step 4: Add Testbench Files
1. In the **Testbench Files** section, click **Add Files...** and browse to:
   * `d:/QGPU/HW/hls/SEQ_GPU/testbench/tb_seq_gpu.cpp`
2. In **Testbench CFLAGs**, enter: `-std=c++14 -I d:/QGPU/HW/hls/common/include -I d:/QGPU/HW/hls/SEQ_GPU/include`. Click **Next**.

### Step 5: Configure Target Part and Clock
1. In the **Hardware** / **Part Selection** step:
   * For **PYNQ-ZU / Zynq UltraScale+**: Search for and select part `xczu5eg-sfvc784-1-e`.
   * For **PYNQ-Z2 / Zynq-7000**: Search for and select part `xc7z020clg400-1`.
2. In **Clock Settings**:
   * **Clock Period**: `10` ns ($100\text{ MHz}$).
   * **Clock Uncertainty**: `2.7` ns (for UltraScale+) or `1.5` ns (for Zynq-7000).
3. In **Flow Target**: Select `Vivado IP Flow` (or `Vitis Kernel Flow` if building an `.xo` package).
4. Click **Finish**.

### Step 6: Run C Simulation
1. In the Flow navigator on the left, click **C SIMULATION** $\rightarrow$ **Run**.
2. Select **Optimized Mode** or **Debug Mode**, ensure **Clean Build** is checked.
3. Click **OK**.
4. In the Console, verify that all 285 regression tests execute and pass:
   ```text
   ==================================================================
     SEQ_GPU VERIFICATION SUMMARY
     Total Tested: 285
     PASSED:       285
     FAILED:       0
   ==================================================================
   >>> RESULT: ALL SEQ_GPU TESTS PASSED SUCCESSFULLY! <<<
   ```

### Step 7: Run C Synthesis
1. In the Flow navigator, click **C SYNTHESIS** $\rightarrow$ **Run**.
2. When synthesis finishes, the **Synthesis Summary Report** opens automatically.
3. Inspect key performance and area metrics:
   * **Timing**: Target $10.0\text{ ns}$, Estimated clock period $< 8.5\text{ ns}$ (slack met).
   * **Latency**: Typical sequential latency $\sim 70$ cycles for GP, $\sim 150$ cycles for sandwich product.
   * **Resource Utilization**: BRAM: $0$, DSP: $\le 4$, FF: low, LUT: low.

### Step 8: Save Reports
Save the synthesis report from:
`<workspace>/SEQ_GPU/solution1/syn/report/seq_gpu_csynth.rpt`
into:
`d:/QGPU/HW/hls/SEQ_GPU/reports/`

### Step 9: Export IP (When Ready)
1. In the Flow navigator, click **PACKAGE** $\rightarrow$ **Run**.
2. Set Format to **IP Catalog**, Vendor: `QGAOPS`, Library: `QGPU`, Version: `1.0`.
3. The exported zip will be located in `<workspace>/SEQ_GPU/solution1/impl/ip/`.
