# Repository Inventory
Generated: 2026-10-27 by audit pass

## Root: D:\QGPU

| Path | Type | Notes |
|------|------|-------|
| .gitignore | file | Standard Python/FPGA gitignore |
| .venv/ | dir | Python 3.13.14 venv (dev deps only) |
| LICENSE | file | MIT |
| NOT TO USE/QGPU/ | dir | Reference-only: previous project; do not modify |
| README.md | file | Stage status table, quick-start, repo map |
| pyproject.toml | file | Build + pytest config (updated in audit) |
| references/ | dir | BibTeX, manifest, PDFs |
| results/ | dir | Raw + processed benchmark/fixture outputs |
| scripts/ | dir | Validation helper scripts |
| software/ | dir | All project Python source |
| docs/ | dir | All documentation |

## software/ sub-tree

| Package | Key files | Status |
|---------|-----------|--------|
| software/reference_model/qgaops_reference/ | algebra.py (162 L), fixed_point.py (213 L) | IMPLEMENTED+TESTED |
| software/reference_model/tests/ | test_reference_model.py (9 tests) | 9 PASSED |
| software/benchmarks/ | runner.py, workloads.py | IMPLEMENTED+MEASURED-SOFTWARE |
| software/benchmarks/tests/ | test_benchmarks.py | 3 PASSED |
| software/dashboard/ | app.py (47 L) - stdlib HTTP | IMPLEMENTED; PySide6 GUI added this audit |
| software/dashboard/tests/ | test_dashboard.py | 1 PASSED |
| software/gesture_pipeline/ | pipeline.py (62 L), fixtures.json | IMPLEMENTED (fixture-only) |
| software/hardware_interface/ | contract.py (73 L) | IMPLEMENTED |
| software/gui/ | qgpu_dashboard.py | NEW - added this audit |

## Key Discrepancies

| Issue | Decision |
|-------|----------|
| Precision conflict: NOT TO USE uses Q1.14 FIX16 | Q16.16 is primary per fixed_point_specification.md |
| Basis label e02 in NOT TO USE | Different indexing; NOT interchangeable with Cl(3,0) |
| No PySide6 GUI | Implemented this audit in software/gui/ |
| pytest collected NOT TO USE tests | Fixed: added testpaths/norecursedirs to pyproject.toml |
| Single benchmark file only | Fixed: added 15-file comprehensive benchmark suite |
