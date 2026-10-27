# Existing Application Audit

Generated: 2026-10-27 — NOT TO USE / QGPU project review

## Application under review

Location: D:\QGPU\NOT TO USE\QGPU\hand_ga_engine\
Main files: main.py (1014 lines), train.py (11229 bytes), walkthrough.md

STATUS: Reference-only. DO NOT MODIFY or merge blindly.

## Algebra comparison

| Attribute | NOT TO USE project | QGAOPS-QGPU main project |
|-----------|-------------------|--------------------------|
| Algebra notation | G(3,0,0) | Cl(3,0) |
| Basis order | 1, e1, e2, e3, e12, e13, e23, e123 | 1, e1, e2, e3, e12, e13, e23, e123 |
| Unusual labels | e02 (appears in mapping code) | None — standard labels only |
| Fixed-point | Q1.14 FIX16 (16-bit, 14 frac bits) | Q16.16 (32-bit, 16 frac bits) |
| Range Q1.14 | [-2, +2) approx | N/A |
| Range Q16.16 | N/A | [-32768, +32767.9999...] |

### e02 label investigation

The label "e02" appears in the mapping/hand_to_ga.py of the NOT TO USE project.
In context it appears to be a basis bivector label where "0" means a zero-indexed
basis vector (e0, e1, e2 instead of e1, e2, e3). This is a DIFFERENT convention
from the Cl(3,0) eight-blade basis used in the main project.

CONCLUSION: e02 from the NOT TO USE project is NOT interchangeable with e12 in
the main project without an explicit coordinate re-labeling. The algebras are
isomorphic but the indexing conventions differ.

## Precision conflict resolution

### NOT TO USE: Q1.14 FIX16
- 16-bit signed: 1 sign + 1 integer + 14 fractional bits
- Range: approx [-2, +2)
- Scale: 2^14 = 16384
- Rounding: implementation-dependent (not documented as ROUND_HALF_EVEN)

### QGAOPS-QGPU: Q16.16
- 32-bit signed: 1 sign + 15 integer + 16 fractional bits
- Range: [-32768, +32767.99998...]
- Scale: 2^16 = 65536
- Rounding: ROUND_HALF_EVEN (documented in fixed_point_specification.md)
- Overflow: saturate + explicit flag

DECISION: Q16.16 is the research project baseline. Q1.14 is a compatibility
mode in the NOT TO USE reference and is explicitly labelled as such.
The precision gap (14 vs 16 fractional bits) means Q1.14 has lower precision
by a factor of 4 (2 bits). For fixed-point FPGA implementation, Q16.16
provides more headroom and precision for the GP coefficient accumulations.

## train.py inspection

Key findings from train.py (NOT TO USE version):
- Takes --dataset argument but contains hard-coded path fallback to LeapGestRecog_1/
- Feature extraction pipeline: HOG baseline + geometric feature extractor
- Uses sklearn RandomForestClassifier and MLPClassifier
- Requires numpy, scikit-learn, opencv-python, mediapipe
- BLOCKER: None of these packages are in the main project venv (dev-only has pytest)

The main project does NOT import from NOT TO USE. Dataset evaluation is BLOCKED
until the dataset is downloaded and optional deps installed.

## main.py inspection

- Full live webcam pipeline requiring cv2, mediapipe, PySide6
- GA engine uses Fix16Multivector with Q1.14
- Well-structured modes: benchmark, microbenchmark, e2e-benchmark, gui, fixed, golden, profile, record, replay, experiment, collect-data
- GUI flag launches PySide6 engineering dashboard (separate module in gui/)
- Computer control features: mouse, presentation, media profiles — uses allowlist

The main project GUI (software/gui/qgpu_dashboard.py) is a new implementation
that reuses the main project's reference model and does NOT depend on the NOT TO USE
application code. This avoids a competing implementation problem.
