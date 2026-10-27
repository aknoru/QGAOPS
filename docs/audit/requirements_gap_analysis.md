# Requirements Gap Analysis

Generated: 2026-10-27 — QGAOPS-QGPU Audit Pass

## Summary

| Category | Total | Implemented | Tested | Partial | Blocked | Pending |
|----------|-------|-------------|--------|---------|---------|---------|
| Requirements | 20 | 8 | 4 | 4 | 1 | 3 |

## Critical Gaps Found and Resolved This Audit

### GAP-1: pytest collected NOT TO USE tests (FIXED)
- **Before**: Running `pytest` from repo root caused 12 import errors from NOT TO USE reference project
- **Fix**: Added `testpaths = ["software"]` and `norecursedirs` to `pyproject.toml`
- **After**: `13 passed in 0.23s` clean

### GAP-2: No PySide6 GUI (FIXED)
- **Before**: `software/dashboard/app.py` was a stdlib HTTP server only (47 lines)
- **Fix**: Created `software/gui/qgpu_dashboard.py` — full 10-tab PySide6 application
- **Tabs**: Overview, GA Calculator, Precision, Benchmark Lab, Dataset/Training, Evaluation, Live Gesture, Contract, Trace, System
- **After**: Imports verified clean; all algebra backed by reference model

### GAP-3: Benchmark suite too narrow (FIXED)
- **Before**: One JSON file with 32 ops, 5 repetitions, geometric_product only
- **Fix**: Generated 15-config benchmark covering all 5 operations × 3 distributions × 128 pairs
- **After**: `results/raw/bench_*.json` — 15 files

### GAP-4: Precision conflict not explicitly resolved in code (DOCUMENTED)
- **Before**: NOT TO USE uses Q1.14 FIX16; main project uses Q16.16 — no explicit boundary document
- **Fix**: `docs/mathematics/fixed_point_specification.md` already states Q16.16 as primary
- **Documented**: `docs/audit/existing_application_audit.md` records both formats and their boundary
- **Decision**: Q16.16 is primary; Q1.14 is reference-only in NOT TO USE directory

### GAP-5: Benchmark runner lacked __main__ module (NOT A BLOCKER)
- The runner is importable and usable as a library; no standalone CLI needed per spec
- GUI Benchmark Lab provides the interactive runner interface

## Remaining Gaps

### GAP-R1: No MediaPipe/OpenCV installed — camera support blocked
- **Impact**: Live gesture tab shows synthetic mode only
- **Required**: `pip install opencv-python mediapipe`
- **Status**: BLOCKED — optional dep; synthetic mode is the documented fallback

### GAP-R2: Dataset not present — dataset evaluation blocked
- **Impact**: Dataset/Training tab shows path-check only
- **Required**: Download LeapGestRecog or HaGRID dataset
- **Status**: BLOCKED — dataset not bundled; setup instructions provided in GUI

### GAP-R3: Numerical validation matrix not computed offline
- **Impact**: Stage 5 validation report has no numerical matrix
- **Resolution**: GUI Evaluation tab computes it on demand (20 operation×distribution configs, 64 pairs each)
- **Status**: PARTIAL — computable via GUI or programmatically

### GAP-R4: Stage 9 golden vectors not pre-generated as files
- **Impact**: Contract tab generates them on demand
- **Resolution**: GUI Contract tab can generate 64 GP basis-pair golden vectors
- **Status**: PROPOSED — generation path implemented, file created on demand

## Items Confirmed Correct (no change needed)

- Cl(3,0) algebra: 8 blades, correct basis masks and sign rules
- Q16.16 encode/decode rounding (ROUND_HALF_EVEN)
- Saturation with explicit overflow flag
- Bilinearity, associativity of geometric product
- Hestenes inner product convention (left grade <= right grade)
- Wedge product (no shared basis vectors)
- Reverse, grade involution, Clifford conjugation
- Hardware contract serialization round-trip
- Benchmark measurement boundary (operation batch only)
