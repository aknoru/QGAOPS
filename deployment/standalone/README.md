# QGAOPS-QGPU: Standalone / Bare-Metal Deployment Guide

## 1. Overview
This directory contains the standalone (bare-metal) C driver and application for the QGPU Cl(3,0) Geometric Algebra Accelerator targeting the dual-core ARM Cortex-A9 on the PYNQ-Z2 board.

Hardware platform definitions (XSA):
- `hardware/vivado/export/qgpu_par_platform.xsa`
- `hardware/vivado/export/qgpu_seq_platform.xsa`

---

## 2. Compilation and Usage in Vitis Embedded
1. Launch AMD Vitis 2025.2.
2. Create a new Platform Project from XSA:
   - Select `hardware/vivado/export/qgpu_par_platform.xsa`
   - Target processor: `ps7_cortexa9_0`
   - OS: `standalone`
3. Create an Application Project using the platform:
   - Language: `C`
   - Template: `Empty Application`
4. Add the source files from this directory:
   - `qgpu_standalone.h`
   - `qgpu_standalone.c`
   - `main.c`
5. Build the application and run on hardware via JTAG.
