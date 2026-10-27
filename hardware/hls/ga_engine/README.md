# QGAOPS-QGPU Synthesizable Geometric Algebra HLS Engine

## 1. Overview
This directory contains the synthesizable C/C++ Geometric Algebra accelerator IP for the **Xilinx Zynq-7000 XC7Z020** FPGA (PYNQ-Z2 board).

- **Normative Algebra**: Euclidean $Cl(3,0)$, canonical 8-blade order `[1, e1, e2, e3, e12, e13, e23, e123]`
- **Arithmetic Precision**: Signed 32-bit Q16.16 (`ap_fixed<32,16>`) with exact round-half-even rescaling and saturation
- **Intermediate Accumulator**: Mathematically justified signed **66-bit accumulator** (`ap_int<66>`) guaranteeing zero intermediate overflow during summation of 8 products of signed 32-bit numbers ($8 \times 2^{62} = 2^{65}$).

---

## 2. Directory Layout
```
hardware/hls/ga_engine/
├── include/
│   ├── qgpu_ga_engine.h      # C API, opcodes, and top-level function declarations
│   └── hls_compat.h          # Fixed-point math, 66-bit accumulator, and round-half-even helpers
├── src/
│   ├── qgpu_ga_top.cpp       # Top-level HLS entry point with AXI4-Lite interface
│   ├── qgpu_ga_engine_shared.cpp    # Variant A: Resource-Shared architecture
│   └── qgpu_ga_engine_parallel.cpp  # Variant B: Parallel pipelined architecture
├── tb/
│   ├── tb_qgpu_ga_engine.cpp # Independent C/C++ testbench
│   └── tb_qgpu_ga_engine.exe # Compiled executable
├── vectors/
│   ├── golden_vectors.csv    # 271 independent golden vectors (exhaustive, edge, random, invalid)
│   └── golden_vectors.json   # Machine-readable vector database
├── scripts/
│   ├── run_hls_csim.tcl      # Vitis HLS C simulation script
│   ├── run_hls_synthesis.tcl # Vitis HLS synthesis script (Variants A & B)
│   ├── run_hls_cosim.tcl     # Vitis HLS C/RTL co-simulation script
│   ├── export_hls_ip.tcl     # Vitis HLS IP packaging script
│   └── Makefile              # Build automation
└── README.md
```

---

## 3. Execution & Verification Instructions

### A. Host C++ Simulation (MinGW GCC / Clang)
To verify the synthesizable kernels against all 271 independent reference golden vectors without needing Vivado/Vitis installed:
```powershell
cd D:\QGPU
C:\mingw64\bin\g++.exe -O3 -Wall -Wextra -I hardware/hls/ga_engine/include `
    hardware/hls/ga_engine/tb/tb_qgpu_ga_engine.cpp `
    hardware/hls/ga_engine/src/qgpu_ga_top.cpp `
    hardware/hls/ga_engine/src/qgpu_ga_engine_shared.cpp `
    hardware/hls/ga_engine/src/qgpu_ga_engine_parallel.cpp `
    -o hardware/hls/ga_engine/tb/tb_qgpu_ga_engine.exe

hardware\hls\ga_engine\tb\tb_qgpu_ga_engine.exe hardware/hls/ga_engine/vectors/golden_vectors.csv
```

### B. Vitis HLS Toolchain Flow (When Vitis HLS is Installed)
Run from the `hardware/hls/ga_engine/scripts/` directory:
```bash
# 1. C Simulation
vitis_hls -f run_hls_csim.tcl

# 2. Synthesis for both Variant A and Variant B
vitis_hls -f run_hls_synthesis.tcl

# 3. C/RTL Co-Simulation
vitis_hls -f run_hls_cosim.tcl

# 4. Export Packaged IP for Vivado
vitis_hls -f export_hls_ip.tcl
```

---

## 4. Vivado Block Design Integration Guide (Downstream Stage 14)
Once the IP is exported:
1. In Vivado, open **Tools -> Settings -> IP -> Repository** and add the directory containing the packaged IP.
2. In the Block Design, instantiate the `QGPU_GA_Engine` IP.
3. Connect the AXI4-Lite slave interface `s_axi_control` to the Zynq Processing System `M_AXI_GP0` port via an AXI Interconnect.
4. Connect the PL fabric clock (`FCLK_CLK0`, 100 MHz) and active-low reset (`ARESETN`).
5. Assign base address `0x43C00000` in the Vivado Address Editor.
