# Dependency and Environment Report

Generated: 2026-10-27

## Python Environment

- Python: 3.13.14 (tags/v3.13.14:fd17997, Jun 10 2026, MSC v.1944 64-bit AMD64)
- Platform: Windows-11-10.0.26300-SP0
- Venv: D:\QGPU\.venv

## Installed packages (this audit pass)

| Package | Version | Group |
|---------|---------|-------|
| pytest | 8.4.2 | dev |
| PySide6 | 6.12.0 | gui (installed this audit) |
| shiboken6 | 6.12.0 | gui (dependency) |
| colorama | 0.4.6 | dev |
| pillow | 13.0.0 | dev |
| pymupdf | 1.28.2 | dev |
| python-pptx | 1.0.2 | dev |
| lxml | 6.1.3 | dev |
| xlsxwriter | 3.3.0 | dev |

## NOT installed (optional groups)

| Package | Group | Required for |
|---------|-------|-------------|
| numpy | train | benchmarks in NOT TO USE project |
| scikit-learn | train | model training |
| matplotlib | train | plots |
| opencv-python | cv | camera input |
| mediapipe | cv | landmark extraction |

## Installation commands

```powershell
# Core dev (already installed):
.\.venv\Scripts\python -m pip install -e ".[dev]"

# GUI (installed this audit):
.\.venv\Scripts\python -m pip install PySide6

# Optional CV:
.\.venv\Scripts\python -m pip install opencv-python mediapipe

# Optional training:
.\.venv\Scripts\python -m pip install numpy scikit-learn matplotlib
```

## Test command

```powershell
.\.venv\Scripts\python -m pytest -v
```

Expected output: 13 passed (as of this audit)

## Launch command for GUI

```powershell
.\.venv\Scripts\python software\gui\qgpu_dashboard.py
```
