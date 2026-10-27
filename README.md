# QGAOPS-QGPU

QGAOPS-QGPU is a research repository for an algebra-aware, memory-centric
geometric-algebra accelerator targeting the PYNQ-Z2 (Xilinx Zynq-7000
XC7Z020). This README reflects the state after the October 2026 audit pass.

> **VERIFICATION DISCIPLINE** — Software results are explicitly marked [MEASURED-SOFTWARE].
> HLS C-simulation results are marked [CSIM-VERIFIED]. No physical FPGA board connection
> is claimed until deployed.

## Status (Stages 1–13 Verification)

| Stage | Status | Evidence |
|-------|--------|----------|
| 1. Requirements and literature | `SOFTWARE_VERIFIED` | [docs/requirements.md](file:///d:/QGPU/docs/requirements.md), [docs/literature_review.md](file:///d:/QGPU/docs/literature_review.md), [docs/references.bib](file:///d:/QGPU/docs/references.bib) |
| 2. Mathematical specification | `SOFTWARE_VERIFIED` — Cl(3,0) Q16.16 | [docs/mathematics/cl30_specification.md](file:///d:/QGPU/docs/mathematics/cl30_specification.md), 66-bit accumulator derivation |
| 3. Repository and build setup | `SOFTWARE_VERIFIED` | [pyproject.toml](file:///d:/QGPU/pyproject.toml), 193/193 tests passing |
| 4. Independent reference model | `SOFTWARE_VERIFIED` — 12 ops | [software/reference_model/](file:///d:/QGPU/software/reference_model) |
| 5. Mathematical validation | `SOFTWARE_VERIFIED` — 66-bit bounds | [accumulator_width_analysis.md](file:///d:/QGPU/docs/verification/accumulator_width_analysis.md) |
| 6. CPU benchmarks | `MEASURED-SOFTWARE` | [results/performance/hand_ga_benchmark.json](file:///d:/QGPU/results/performance/hand_ga_benchmark.json) |
| 7. Multi-dataset & GA mapping | `SOFTWARE_VERIFIED` | [leap_gesture_evaluation.json](file:///d:/QGPU/results/experiments/leap_gesture_evaluation.json) (98.39% acc), Deep1M/SIFT1M/GIST1M adapters |
| 8. CPU GUI dashboard | `SOFTWARE_VERIFIED` | [software/gui/qgpu_dashboard.py](file:///d:/QGPU/software/gui/qgpu_dashboard.py) (12 tabs, verified offscreen/live) |
| 9. Hardware interface contract | `SOFTWARE_VERIFIED` — 76-byte DMA packet | [contract.py](file:///d:/QGPU/software/hardware_interface/contract.py), [hardware_interface_specification.md](file:///d:/QGPU/docs/architecture/hardware_interface_specification.md) |
| 10. Synthesizable HLS GA engine | `HLS_CSIM_VERIFIED` | [hardware/hls/ga_engine/src/](file:///d:/QGPU/hardware/hls/ga_engine/src) (Variants A & B) |
| 11. Independent C/C++ testbench | `HLS_CSIM_VERIFIED` — 271/271 pass | [results/hls/csim/csim_evidence.log](file:///d:/QGPU/results/hls/csim/csim_evidence.log) |
| 12. HLS Synthesis, Co-Sim & IP | `BLOCKED (Host Toolchain Missing)` | [hardware/hls/ga_engine/scripts/](file:///d:/QGPU/hardware/hls/ga_engine/scripts) (Tcl scripts ready; Vitis HLS not on host) |
| 13. Controlled Arch Comparison | `HLS_CSIM_VERIFIED` | [docs/architecture/architecture_comparison_report.md](file:///d:/QGPU/docs/architecture/architecture_comparison_report.md) |

## Quick start

```powershell
# Install core dev dependencies
.\.venv\Scripts\python -m pip install -e ".[dev]"

# Run tests (179 total: 13 core + 166 hand GA engine — all pass 100%)
.\.venv\Scripts\python -m pytest software hand_ga_engine\tests -v

# Launch full PySide6 Unified Research & Engineering Console
.\.venv\Scripts\python software\gui\qgpu_dashboard.py
# or
.\.venv\Scripts\python main.py --gui

# Run synthetic mode (no camera needed)
.\.venv\Scripts\python main.py --gui --no-webcam

# Run high-resolution 50,000-op microbenchmarks
.\.venv\Scripts\python main.py --microbenchmark

# Run standard GA benchmarks (10,000 ops)
.\.venv\Scripts\python main.py --benchmark

# Run end-to-end pipeline benchmark
.\.venv\Scripts\python main.py --e2e-benchmark

# Run Stage 6 CPU workload benchmarks
.\.venv\Scripts\python -m software.benchmarks

# Launch computer vision gesture control directly
.\.venv\Scripts\python main.py --control mouse
.\.venv\Scripts\python main.py --control presentation
.\.venv\Scripts\python main.py --control object3d
```

### Dependencies

```powershell
# GUI & CV & Scientific packages (installed in .venv)
.\.venv\Scripts\python -m pip install PySide6 opencv-python mediapipe numpy scikit-learn matplotlib pyyaml scipy pyautogui
```

## GUI Features (12 functional tabs)

1. **Overview** — Stage status matrix (Stages 1–22), dependency checks, hardware truthfulness banner
2. **Live Monitor** — Dual-pane MediaPipe 3D Landmark Tracking camera feed + 3D GA Vector/Rotor View + HUD overlay + Active GA/IR card
3. **Classifier** — 13 Static Hand Poses + 14 Dynamic Motion Expressions real-time probability progress bars
4. **Gesture Control** — Computer Vision control suite (Mouse, Presentation, Media, Object3D profiles, F12 emergency stop, sub-ms telemetry, recent actions log)
5. **GA Calculator** — Interactive Cl(3,0) multivector computation, 8-blade coefficient decomposition table, rotor/sandwich product decomposition
6. **Precision** — Q16.16 signed fixed-point error analysis, single-value bitwise encoder/decoder, 64-pair basis validation
7. **Benchmark Lab** — One-click 50k ops microbenchmark, 10k ops standard benchmark, E2E pipeline benchmark, Stage 6 workload runner
8. **Waterfall** — Pipeline stage latency waterfall table (ms and % total), logical bandwidth, throughput, system CPU/RAM usage
9. **AAMF Memory** — QGAOPS Algebra-Aware Memory Fabric simulation (Scratchpad + Tile Buffer B0-B5 model, DDR traffic reduction)
10. **Contract** — Stage 9 hardware contract serialization tester, hardware register counters `[N/A — FPGA NOT CONNECTED]`, IR queue
11. **Experiments** — Kaggle LeapGestRecog dataset audit, test evaluation, classification report, confusion matrix
12. **Execution Log** — Searchable timestamped real-time log stream

## Benchmark summary (CPU software — seed=20261026, 32 pairs)

| Operation | Float64 (ops/s) | Q16.16 (ops/s) | Notes |
|-----------|-----------------|-----------------|-------|
| geometric_product | ~13,000 | ~7,000 | dense distribution |
| wedge | ~33,000 | ~17,000 | sparse distribution |
| hestenes_inner | ~29,000 | ~15,000 | dense |
| add/subtract | ~290,000 | ~90,000 | element-wise only |

_[MEASURED-SOFTWARE] Not FPGA. Timing boundary: operation batch only, conversion excluded._

## Repository map

- `docs/audit/` — **NEW**: complete audit reports and gap analysis
- `docs/requirements/` — requirements, traceability, acceptance gates
- `docs/mathematics/` — Cl(3,0), operation conventions, Q16.16 semantics
- `docs/research/` — literature review, comparison, gap, citation audit
- `docs/architecture/` — proposed system and implementation variants
- `docs/planning/` — risks, decisions, illustrative timeline
- `docs/verification/` — validation and acceptance plan
- `references/` — BibTeX, provenance manifest, PDF policy
- `software/reference_model/` — independent Cl(3,0) floating-point + Q16.16 model
- `software/benchmarks/` — CPU benchmark runner and workloads
- `software/gesture_pipeline/` — fixture-based gesture pipeline
- `software/hardware_interface/` — Stage 9 serialization contract
- `software/gui/` — PySide6 12-tab engineering console (`qgpu_dashboard.py`)
- `hand_ga_engine/` — Live Hand GA Engine, MediaPipe tracking, gesture control & 27 expressions
- `golden/` — Golden test vectors for hardware verification (CGA, spatial GA, fixed point, quantum GA)
- `hardware/` — Stage 10+ HLS accelerator IP (`qgpu_accel.cpp`), Vivado block designs, testbenches, drivers
- `results/` — benchmark reports, performance metrics, and experiment evaluations

## Mathematical contract

Algebra: **Cl(3,0)** — Euclidean 3D Clifford algebra  
Basis: `[1, e1, e2, e3, e12, e13, e23, e123]`  
Basis masks: `[0, 1, 2, 4, 3, 5, 6, 7]`  
Fixed-point: **Q16.16** signed 32-bit (primary research contract)  
Rounding: ROUND_HALF_EVEN | Overflow: saturate + explicit flag

## Precision Specification (Q16.16 Primary)

The primary mathematical contract uses **Q16.16** (signed 32-bit with 16 fractional bits, range $[-32768, +32767.9999]$).
A Q1.14 fixed-point mode is also provided in `hand_ga_engine/fixed_point/` for comparison with edge FPGA micro-datapaths.

## License and attribution

Project-authored documentation and code: MIT licensed.  
Third-party papers: copyright of respective publishers/authors.  
See `LICENSE` and `references/README.md`.
