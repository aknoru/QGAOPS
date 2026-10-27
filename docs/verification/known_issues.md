# Known Issues & Resolution Log

| Severity | Affected files | Reproduction | Root cause | Fix / acceptance test | Status |
|---|---|---|---|---|---|
| High | `hls_compat.h` | Run sequential `csynth_design` before the fix | Vitis rejects a ternary expression with inferred `ap_int<67>`/`ap_int<68>` arms | Replaced ternary with explicit assignments; synthesis verified to completion on both variants. | RESOLVED |
| High | `tb_qgpu_ga_engine.cpp` | Run dedicated Vitis C-sim / co-sim | Testbench linked sub-kernels instead of top functions `qgpu_ga_sequential_top` and `qgpu_ga_parallel_top` | Updated calls to target dedicated top functions directly; C-sim, GCC audit, and XSIM C/RTL co-sim all pass 100%. | RESOLVED |
| High | `hardware/hls/ga_engine/prj` | Inspect workspace | Obsolete Vitis IDE project attempting monolithic combined synthesis; locked by background daemon | Process tree terminated and entire obsolete `prj` folder deleted. | RESOLVED |
| High | `sequential/qgpu_ga_sequential` | Inspect synthesis & co-sim | Sequential synthesis lacked AXI-Lite control directives and co-sim | Added `s_axilite` directives to `directives.tcl` and `run_hls_synthesis.tcl`; completed synthesis, XSIM co-sim (Pass, 285 vectors), and IP export. | RESOLVED |
| High | `adaptive_pipeline/qgpu_ga_parallel` | Inspect synthesis & co-sim | Parallel synthesis unrolling 64 terms needed independent completion | Completed synthesis (110.71 MHz, 32 DSPs, 12867 FFs, 13627 LUTs), XSIM co-sim (Pass, 285 vectors), and IP export. | RESOLVED |
| High | `hardware/vivado/scripts/` | Vivado BD creation | No dual-IP block design integrating both distinct exported IPs | Created `stage13_vivado_integration.tcl` integrating PS7, SmartConnect, clocking, resets, and both IPs (`0x40000000`, `0x40010000`); validated and generated wrapper. | RESOLVED |
| Medium | Python pytest suite | Run `pytest` | Suspected venv accessibility issue | Verified Python 3.13.14 runs `pytest` cleanly: all 197 unit tests passed in 43.69s. | RESOLVED |
