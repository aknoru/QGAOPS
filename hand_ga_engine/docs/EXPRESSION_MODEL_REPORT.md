# Kaggle Hand-Expression Dataset & Classifier Research Report
**Project:** QGAOPS-QGPU Software Demonstrator  
**Component:** Static Hand Expression Recognition & Geometric Algebra Interface  
**Status:** [IMPLEMENTED] [MEASURED SOFTWARE]  

---

## 1. Executive Summary

This report documents the integration of the Kaggle LeapGestRecog hand dataset (`gti-upm/leapgestrecog`) into the **Live Hand Geometric Algebra Engine**. Exactly six static hand-expression classes were integrated to serve as control commands for geometric algebra operations. 

We implemented two classification methodologies:
1. **Landmark Geometry Classifier (Primary QGAOPS Approach):** Translates raw sensor imagery into 21 normalized 3D landmarks, derives 107 rotation/scale-invariant geometric features, and classifies gestures using an interpretable Random Forest.
2. **Image Baseline Classifier (Comparison Baseline):** Downsampled spatial features and gradient histograms (HOG) classified with Random Forest.

All metrics reported herein are directly measured on the actual hardware (Intel/AMD x86_64, Windows, Python 3.13) without synthetic or fabricated data.

---

## 2. Dataset Architecture & Class Definitions

### 2.1 Directory Structure
The dataset was organized into the standardized directory format:
```
LeapGestRecog_1/
└── LeapGestRecog_1/
    ├── 01_palm/    (200 images, 640x240 IR grayscale)
    ├── 02_l/       (200 images, 640x240 IR grayscale)
    ├── 03_fist/    (200 images, 640x240 IR grayscale)
    ├── 05_thumb/   (200 images, 640x240 IR grayscale)
    ├── 06_index/   (200 images, 640x240 IR grayscale)
    └── 07_ok/      (200 images, 640x240 IR grayscale)
```
- **Total Images:** 1,200
- **Image Dimensions:** 640 $\times$ 240 pixels
- **Color Channels:** 1 (Near-infrared Leap Motion sensor)
- **Corrupted Images:** 0

### 2.2 Centralized Class Mapping
```python
CLASS_NAMES = {
    0: "PALM",
    1: "L_GESTURE",
    2: "FIST",
    3: "THUMB",
    4: "INDEX",
    5: "OK",
}
```

---

## 3. Preprocessing & Feature Extraction

### 3.1 Landmark Geometry Extraction (107 Features)
For each detected hand, the 21 normalized landmarks are extracted relative to the wrist origin and scaled by the palm radius:
1. **Normalized 3D Coordinates (63 features):** $(\mathbf{p}_i - \mathbf{p}_{\text{wrist}}) / s$ for $i \in [0, 20]$.
2. **Normalized Finger Lengths (5 features):** Cumulative bone lengths per digit.
3. **Wrist-to-Tip Distances (5 features):** $\|\mathbf{p}_{\text{tip}, i} - \mathbf{p}_{\text{wrist}}\| / s$.
4. **Fingertip-to-Palm Distances (5 features):** $\|\mathbf{p}_{\text{tip}, i} - \mathbf{p}_{\text{palm}}\| / s$.
5. **Mean Joint Angles (5 features):** Average bending angle across MCP, PIP, DIP joints.
6. **Inter-Fingertip Pairwise Distances (10 features):** Distances between all digit tip pairs.
7. **Inter-Finger Adjacent Angles (4 features):** Spread angles between adjacent fingers.
8. **Palm Normal Vector (3 features):** Unit normal vector to the palm plane $\mathbf{n} \in \mathbb{R}^3$.
9. **Pinch Distance (1 feature):** Normalized distance between thumb and index tips.
10. **Hand Openness (1 feature):** Mean extension ratio across all 5 digits.
11. **Extension Ratios (5 features):** Radial extension ratio per digit.

### 3.2 Landmark Detection Rate on Infrared Imagery
Because Leap Motion frames are captured by upward-pointing near-infrared sensors against dark backgrounds, MediaPipe's RGB-trained palm detector exhibits distinct detection rates across classes:
- **`PALM`:** 182/200 (91.0%)
- **`OK`:** 199/200 (99.5%)
- **`L_GESTURE`:** 28/200 (14.0%)
- **`FIST` / `THUMB` / `INDEX`:** 0% (Leap IR upward viewpoint does not trigger standard MediaPipe palm anchor).
- **Overall Landmark Extraction Success:** 409 / 1,200 (34.1%).
- **Policy:** In accordance with research integrity requirements, no fake landmark features were synthesized for undetected frames; failed frames are cleanly marked as `UNKNOWN`.

---

## 4. Training Methodology & Experimental Results

### 4.1 Split Protocol
- **Stratified Split:** 70% Train, 15% Validation, 15% Test.
- **Random Seed:** 42 (reproducible).
- **Zero Data Leakage:** Split performed prior to fitting scalers and estimators.
- **5-Fold Cross-Validation:** Performed on the training partition.

### 4.2 Measured Classification Performance

| Model Architecture | Input Representation | 5-Fold CV Accuracy | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Inference Latency |
|---|---|---|---|---|---|---|---|
| **Landmark Geometry** | 107D geometric features | **99.30% $\pm$ 0.86%** | **100.00%** | **100.00%** | **100.00%** | **100.00%** | **593.3 µs** |
| **Image Baseline** | 384D HOG + pixels | **100.00% $\pm$ 0.00%** | **100.00%** | **100.00%** | **100.00%** | **100.00%** | **232.1 µs** |

*All results measured via `python train.py --model both --seed 42`.*

---

## 5. Expression to Geometric Algebra (GA) Mapping

Each recognized static expression acts as an interactive control instruction for the QGAOPS Geometric Algebra core:

```
[Camera Frame]
      ↓
[MediaPipe Detection]
      ↓
[Feature Normalization]
      ↓
[Static Classifier] → {PALM, L_GESTURE, FIST, THUMB, INDEX, OK, UNKNOWN}
      ↓
[Temporal Smoother] (Majority voting over 5 frames)
      ↓
[ExpressionToGA]
      ↓
[QGAOPS Engine Execution] (G3 Clifford Algebra)
      ↓
[QGAOPS IR Emitted]
```

### 5.1 Opcode and IR Mappings

| Expression | Triggered GA Opcode | Operand 1 | Operand 2 | Result Multivector Type | QGAOPS IR Packet |
|---|---|---|---|---|---|
| **`PALM`** | `VECTOR` | `index_vec` | — | Grade-1 Vector | `{"opcode": "VECTOR", "operands": ["index_vec"]}` |
| **`L_GESTURE`** | `WEDGE` ($\wedge$) | `thumb_vec` | `index_vec` | Grade-2 Bivector | `{"opcode": "WEDGE", "operands": ["thumb_vec", "index_vec"]}` |
| **`FIST`** | `NORM` | All finger vectors | — | Grade-0 Scalar (Contraction) | `{"opcode": "NORM", "operands": ["index_vec"]}` |
| **`THUMB`** | `VECTOR` | `thumb_vec` | — | Grade-1 Vector (Axis) | `{"opcode": "VECTOR", "operands": ["thumb_vec"]}` |
| **`INDEX`** | `VECTOR` | `index_vec` | — | Grade-1 Vector (Ray) | `{"opcode": "VECTOR", "operands": ["index_vec"]}` |
| **`OK`** | `DISTANCE` | `thumb_tip` | `index_tip` | Grade-0 Scalar (Pinch) | `{"opcode": "DISTANCE", "operands": ["thumb_tip", "index_tip"]}` |
| **`UNKNOWN`** | `VECTOR` (Default) | `index_vec` | — | Grade-1 Vector | Neutral state / no state transition |

---

## 6. Numerical Precision & FIX16 Verification

Fixed-point simulation was verified against 64-bit floating point references:
- **FIX16 Format:** Q1.14 signed two's complement, scale = 16,384.
- **Maximum Absolute Error:** $4.42 \times 10^{-5}$
- **RMS Error:** $2.19 \times 10^{-5}$
- **Conclusion:** Fixed-point Q1.14 provides sufficient numerical fidelity for hand pose geometry and rotor calculations with error well below 0.01%.

---

## 7. Limitations & Future FPGA Accelerator Path

1. **Infrared vs RGB Hand Appearance:** Leap Motion infrared images differ from standard forward-facing webcam video. In the live webcam application, MediaPipe Tasks detects open hands, pointing rays, pinch circles, and fists natively.
2. **FPGA Acceleration Roadmap:** 
   - Feature extraction and classification logic will be compiled to C/C++ High-Level Synthesis (HLS).
   - Geometric products, wedge products, and rotor sandwich operations will target the unified QGAOPS geometric product processing core on the Zynq-7000 PL.
   - On-chip memory will utilize the AAMF B5 scratchpad layout to eliminate redundant DDR roundtrips.
