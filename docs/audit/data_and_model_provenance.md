# Data and Model Provenance Report

Generated: 2026-10-27

## Datasets

### LeapGestRecog
- **Status**: NOT PRESENT in this repository
- **Source**: Kaggle — https://www.kaggle.com/datasets/gti-upm/leapgestrecog
- **License**: CC BY 4.0 (check Kaggle page before redistribution)
- **Size**: ~0.6 GB (10 subjects, 10 gestures, IR images)
- **Relevance**: Primary gesture classification evaluation dataset
- **Action required**: `kaggle datasets download gti-upm/leapgestrecog` or manual download
- **Setup path**: After download, place at a local path and use GUI Dataset tab to verify

### HaGRID
- **Status**: NOT PRESENT
- **Source**: https://github.com/hukenovs/hagrid
- **License**: CC BY-SA 4.0
- **Size**: ~723 GB full; subset ~3.7 GB
- **Relevance**: Alternative/additional gesture dataset
- **Status**: EXCLUDED — too large for this audit scope; download not warranted

### SIFT1M / GIST1M / Deep1M
- **Status**: NOT PRESENT
- **Relevance**: Vector descriptor workloads — NOT hand gesture datasets
- **Decision**: EXCLUDED — no GA-to-descriptor mapping justified in current scope

### Synthetic fixture data
- **Status**: PRESENT — `software/gesture_pipeline/fixtures.json`
- **Content**: 3 hand pose samples (fist, open, point) with 21 3D landmarks each
- **Source**: Hand-crafted deterministic data, not derived from any real dataset
- **Use**: Algorithm correctness testing ONLY — not for accuracy claims

## Model files

### MediaPipe Hand Landmarker
- **Status**: NOT INSTALLED (mediapipe package not in venv)
- **Required for**: Landmark extraction from images
- **Install**: `pip install mediapipe`
- **Model download**: Automatic on first use (mediapipe handles it)

### Static Expression Classifier (pkl)
- **Status**: NOT PRESENT (`models/static_expression_model.pkl` does not exist)
- **Required for**: 13-pose trained classifier in NOT TO USE project
- **Action**: Train with `train.py` after dataset is available

## Generated artifacts (this repository)

| Artifact | Source | Status |
|----------|--------|--------|
| results/raw/stage6_cpu_benchmark.json | benchmark runner | PRESENT (prev. audit) |
| results/raw/bench_*.json (15 files) | benchmark runner | PRESENT (this audit) |
| results/processed/gesture_fixture_result.json | pipeline + fixture | PRESENT |
| docs/audit/*.md, *.csv | this audit | CREATED |

## Reference papers

See `references/paper_manifest.csv` for full list.
Key papers:
- Hildenbrand et al. — GA hardware implementation
- Fuchs & Perwass — GAPP compiler
- Montoya et al. — FPGA motor algebra accelerator
Access: see manifest for DOI and local file status.
All papers remain copyright of their publishers.
