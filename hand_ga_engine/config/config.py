"""
LIVE HAND GEOMETRIC ALGEBRA ENGINE
config/config.py — Central Configuration

[IMPLEMENTED] All parameters are software-configurable.
[PROPOSED]    FPGA backend parameters are stubs only.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple


# ---------------------------------------------------------------------------
# Camera
# ---------------------------------------------------------------------------

CAMERA_INDEX: int = 0
CAMERA_WIDTH:  int = 1280
CAMERA_HEIGHT: int = 720
CAMERA_FPS:    int = 30

# ---------------------------------------------------------------------------
# Hand detection
# ---------------------------------------------------------------------------

MEDIAPIPE_MAX_HANDS:           int   = 2
MEDIAPIPE_MIN_DETECTION_CONF:  float = 0.5
MEDIAPIPE_MIN_TRACKING_CONF:   float = 0.5
MEDIAPIPE_MODEL_COMPLEXITY:    int   = 1

# Temporal smoothing (exponential moving average). Alpha=1.0 → no smoothing.
LANDMARK_SMOOTHING_ALPHA: float = 0.5

# ---------------------------------------------------------------------------
# Gesture / Expression recognition
# ---------------------------------------------------------------------------

PINCH_THRESHOLD:       float = 0.05   # normalized distance for pinch
OPEN_THRESHOLD:        float = 0.15   # min fingertip-to-wrist for open
FIST_THRESHOLD:        float = 0.08   # max fingertip-to-palm for fist
CURL_THRESHOLD:        float = 0.06   # joint curl threshold

GESTURE_CONFIDENCE_MIN: float = 0.60  # below this → UNKNOWN
GESTURE_STABLE_FRAMES:  int   = 5     # frames required before confirming
GESTURE_COOLDOWN_FRAMES: int  = 15    # frames after release

# Dynamic expression
TEMPORAL_BUFFER_FRAMES: int  = 30
SWIPE_VEL_THRESHOLD:    float = 0.015  # normalized units / frame
ROTATION_THRESHOLD:     float = 0.10   # radians / frame

# ---------------------------------------------------------------------------
# GA Engine
# ---------------------------------------------------------------------------

DEFAULT_ALGEBRA:    str = "G3"
DEFAULT_SIGNATURE:  Tuple[int,int,int] = (1, 1, 1)   # G(3,0,0)
DEFAULT_PRECISION:  str = "FLOAT32"

# ---------------------------------------------------------------------------
# FIX16 — Q1.14
# ---------------------------------------------------------------------------

FIX16_FRAC_BITS: int = 14
FIX16_MAX:       int = (1 << 15) - 1   # 32767
FIX16_MIN:       int = -(1 << 15)      # -32768
FIX16_SCALE:     float = float(1 << FIX16_FRAC_BITS)  # 16384.0

# ---------------------------------------------------------------------------
# Visualization
# ---------------------------------------------------------------------------

WINDOW_WIDTH:  int = 1600
WINDOW_HEIGHT: int = 800
WEBCAM_PANEL_W: int = 640
VECTOR_PANEL_W: int = 480
INFO_PANEL_W:   int = 480

VECTOR_3D_UPDATE_EVERY: int = 3  # update 3D plot every N frames

# Color palette (BGR for OpenCV)
COLOR_HAND_SKELETON:  Tuple[int,int,int] = (0, 220, 120)
COLOR_VECTOR_PRIMARY: Tuple[int,int,int] = (0, 200, 255)
COLOR_VECTOR_SECONDARY: Tuple[int,int,int] = (255, 120, 0)
COLOR_WEDGE_PLANE:    Tuple[int,int,int] = (180, 0, 255)
COLOR_TEXT:           Tuple[int,int,int] = (230, 230, 230)
COLOR_HIGHLIGHT:      Tuple[int,int,int] = (0, 255, 200)
COLOR_BG:             Tuple[int,int,int] = (18, 18, 24)

FONT_SCALE_LARGE: float = 0.7
FONT_SCALE_SMALL: float = 0.5

# ---------------------------------------------------------------------------
# Profiling / Benchmark
# ---------------------------------------------------------------------------

BENCHMARK_ITERATIONS: int = 10_000
PROFILE_SAVE_DIR:  str = "results/profile"
EXPERIMENT_DIR:    str = "results/experiments"
EXPRESSION_DIR:    str = "results/expressions"
GOLDEN_DIR:        str = "golden"

# ---------------------------------------------------------------------------
# Recording / Replay
# ---------------------------------------------------------------------------

RECORDING_DEFAULT: str = "recording.json"

# ---------------------------------------------------------------------------
# Backend
# ---------------------------------------------------------------------------

DEFAULT_BACKEND: str = "python"  # "python" | "fpga" (fpga is stub)

# ---------------------------------------------------------------------------
# Keyboard shortcuts
# ---------------------------------------------------------------------------

KEY_QUIT:       int = ord('q')
KEY_GP:         int = ord('g')
KEY_DOT:        int = ord('d')
KEY_WEDGE:      int = ord('w')
KEY_ROTOR:      int = ord('r')
KEY_SANDWICH:   int = ord('s')
KEY_FIX16:      int = ord('f')
KEY_BENCHMARK:  int = ord('b')
KEY_VECTORS:    int = ord('v')
KEY_HELP:       int = ord('h')
KEY_NEXT_MODE:  int = ord('m')
KEY_COLLECT:    int = ord('c')
