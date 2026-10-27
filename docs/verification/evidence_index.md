# Truthful Evidence Index

| Evidence Artifact | Status | File Location | Key Metrics / Results |
|---|---|---|---|
| Python Full Test Suite | PASS | `pytest -v` | **197 passed** in 43.69s across reference model, datasets, gesture, fix16, and IR |
| Direct GCC Host Kernel Validation | HOST_TEST_PASS | `hardware/hls/ga_engine/tb/tb_qgpu_ga_engine_audit.exe` | 570 checks (285 vectors x 2 architectures), 0 failures, 100% bit-exact |
| Sequential Vitis C-Simulation | VITIS_CSIM_PASS | `hardware/hls/sequential/csim_console.log` | 285 independent vectors, 0 errors |
| Sequential C-Synthesis Report | VITIS_SYN_PASS | `hardware/hls/sequential/qgpu_ga_sequential/solution1/syn/report/csynth.rpt` | Latency: 14-598 cycles; Clock: 10.0ns (est 7.137ns, 140.11 MHz); 0 BRAM, 8 DSP (3%), 2455 FF (2%), 4915 LUT (9%) |
| Sequential C/RTL Co-Simulation | COSIM_PASS | `hardware/hls/sequential/qgpu_ga_sequential/solution1/sim/report/qgpu_ga_sequential_top_cosim.rpt` | Verilog in XSIM: Pass; Latency: min 15, avg 226, max 559 cycles; 285 vectors tested |
| Sequential IP Catalog Export | IP_EXPORT_PASS | `hardware/hls/sequential/qgpu_ga_sequential/solution1/impl/ip/` | IP archive: `qgpu_hls_qgpu_ga_sequential_top_1_0.zip`, `component.xml` |
| Parallel Vitis C-Simulation | VITIS_CSIM_PASS | `hardware/hls/adaptive_pipeline/csim_console.log` | 285 independent vectors, 0 errors |
| Parallel C-Synthesis Report | VITIS_SYN_PASS | `hardware/hls/adaptive_pipeline/qgpu_ga_parallel/solution1/syn/report/csynth.rpt` | Latency: 14-208 cycles; Clock: 10.0ns (est 9.032ns, 110.71 MHz); 0 BRAM, 32 DSP (14%), 12867 FF (12%), 13627 LUT (25%) |
| Parallel C/RTL Co-Simulation | COSIM_PASS | `hardware/hls/adaptive_pipeline/qgpu_ga_parallel/solution1/sim/report/qgpu_ga_parallel_top_cosim.rpt` | Verilog in XSIM: Pass; Latency: min 15, avg 70, max 207 cycles; 285 vectors tested |
| Parallel IP Catalog Export | IP_EXPORT_PASS | `hardware/hls/adaptive_pipeline/qgpu_ga_parallel/solution1/impl/ip/` | IP archive: `qgpu_hls_qgpu_ga_parallel_top_1_0.zip`, `component.xml` |
| Vivado Dual-IP Block Design Integration | VIVADO_BD_PASS | `hardware/vivado/project/qgpu_stage13_vivado/` | `qgpu_system_bd` validated; Zynq PS7 + SmartConnect + Dual HLS IPs at `0x40000000` & `0x40010000`; top HDL wrapper generated |
