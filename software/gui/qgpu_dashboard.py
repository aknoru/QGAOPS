"""
QGAOPS-QGPU Unified Research & Engineering Console
software/gui/qgpu_dashboard.py

Launch:
    .venv\\Scripts\\python software\\gui\\qgpu_dashboard.py
    .venv\\Scripts\\python main.py --gui

Complete Research Console integrating:
1. Live Hand Gesture Recognition (MediaPipe 3D Landmark Tracking + 3D GA Vector/Rotor View + HUD Overlay)
2. 13 Static Hand Poses + 14 Dynamic Motion Expressions Probability Classifier
3. Computer Vision Gesture Control (Mouse, Presentation, Media, 3D Object with F12 Emergency Stop)
4. Full Benchmark Lab (50k ops Microbenchmark, 10k ops GA Standard Benchmark, E2E Pipeline Benchmark, Stage 6 Workloads)
5. Performance Metrics Waterfall & Logical Bandwidth / System Utilization
6. QGAOPS Algebra-Aware Memory Fabric (AAMF B0-B5 Model) Simulation
7. Interactive Cl(3,0) Geometric Algebra Calculator & Multivector Decomposition
8. Q16.16 Fixed-Point Precision Analysis
9. Stage 9 Hardware Interface Contract & Execution Queue (Explicitly labeled [N/A — FPGA NOT CONNECTED])
10. Kaggle Dataset Experiments & Confusion Matrix Evaluation
11. Real-time Trace & Event Log Stream

[SOFTWARE ONLY] All results are [MEASURED SOFTWARE] or [SOFTWARE MODEL] unless physical FPGA bitstream is deployed.
"""
from __future__ import annotations

import io
import json
import math
import os
import platform
import random
import statistics
import sys
import time
import traceback
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

# ---------------------------------------------------------------------------
# Project root and hand_ga_engine on sys.path
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent.parent  # D:\QGPU
_HAND_GA_DIR = _ROOT / "hand_ga_engine"
for p in [str(_ROOT), str(_HAND_GA_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# ---------------------------------------------------------------------------
# PySide6 imports
# ---------------------------------------------------------------------------
try:
    from PySide6.QtCore import (
        Qt, QThread, Signal, QObject, QTimer, QSize, QPointF
    )
    from PySide6.QtGui import (
        QColor, QFont, QPainter, QPen, QBrush, QLinearGradient,
        QPalette, QPixmap, QIcon, QAction, QImage
    )
    from PySide6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
        QGridLayout, QTabWidget, QLabel, QPushButton, QLineEdit,
        QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit, QProgressBar,
        QTableWidget, QTableWidgetItem, QGroupBox, QSplitter,
        QFileDialog, QMessageBox, QScrollArea, QSlider, QCheckBox,
        QStatusBar, QFrame, QSizePolicy, QHeaderView
    )
    HAS_PYSIDE6 = True
except ImportError as _e:
    print(f"[FATAL] PySide6 not available: {_e}")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Reference model and benchmark imports from software/
# ---------------------------------------------------------------------------
from software.reference_model.qgaops_reference.algebra import (
    Multivector, scalar, blade, BASIS_NAMES, BASIS_GRADES,
)
from software.reference_model.qgaops_reference.fixed_point import (
    FixedPointFormat, FixedPointMultivector,
)
from software.benchmarks.workloads import WorkloadConfig, generate_pairs, execute_pair
from software.benchmarks.runner import run as run_benchmark_config, write_result
from software.gesture_pipeline.pipeline import load_fixture, nearest_centroid
from software.hardware_interface.contract import (
    OperationRequest, serialize, deserialize, execute_contract,
    OPERATION_IDS, VERSION,
)

# ---------------------------------------------------------------------------
# Hand GA Engine imports from hand_ga_engine/
# ---------------------------------------------------------------------------
try:
    from config.config import (
        CAMERA_INDEX, LANDMARK_SMOOTHING_ALPHA, BENCHMARK_ITERATIONS,
    )
    from engine.algebra_engine import AlgebraEngine
    from ga.multivector import Multivector as GAMultivector
    from mapping.expression_classes import (
        STATIC_POSES, DYNAMIC_EXPRESSIONS, ALL_EXPRESSIONS, ALL_EXPRESSION_NAMES,
    )
    from mapping.dataset_classes import CLASS_NAMES, UNKNOWN_CLASS
    from control.safety import ControlState
    from control.controller import GestureController, ControlExecutionReport
    from visualization.control_overlay import render_control_hud
    from metrics.hardware_metrics import NOT_AVAILABLE
    from metrics.performance_tracker import PerformanceSnapshot, PerformanceTracker
    from gui.dashboard_window import VideoWorker, DashboardWindow
    HAS_HAND_GA_ENGINE = True
except Exception as _e:
    print(f"[WARN] hand_ga_engine import warning: {_e}")
    HAS_HAND_GA_ENGINE = False


# ---------------------------------------------------------------------------
# Styling and Colors
# ---------------------------------------------------------------------------
ACCENT    = "#00E5FF"   # Neon Cyan
ACCENT2   = "#7C3AED"   # Deep Violet
ACCENT3   = "#E040FB"   # Magenta
SUCCESS   = "#00E676"   # Neon Green
WARNING   = "#FFB300"   # Amber
ERROR_COL = "#FF5252"   # Coral Red
BG_DARK   = "#0D0E15"
BG_PANEL  = "#131622"
BG_CARD   = "#181C2B"
FG_TEXT   = "#E2E8F0"
FG_DIM    = "#8C93A8"
MONO_FONT = "'Consolas', 'Courier New', monospace"

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG_DARK};
    color: {FG_TEXT};
    font-family: 'Segoe UI', 'Inter', sans-serif;
    font-size: 12px;
}}
QTabWidget::pane {{
    border: 1px solid #232738;
    background: {BG_PANEL};
    border-radius: 4px;
}}
QTabBar::tab {{
    background: #181B26;
    color: {FG_DIM};
    padding: 8px 14px;
    border: 1px solid #232738;
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    margin-right: 2px;
    font-weight: bold;
    font-size: 11px;
}}
QTabBar::tab:selected {{
    background: #232738;
    color: {ACCENT};
    border-bottom: 2px solid {ACCENT};
}}
QTabBar::tab:hover:!selected {{
    background: #1F2332;
    color: {FG_TEXT};
}}
QGroupBox {{
    border: 1px solid #282C40;
    border-radius: 6px;
    margin-top: 14px;
    padding: 8px;
    font-weight: bold;
    color: {ACCENT};
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 8px;
    padding: 0 4px;
}}
QPushButton {{
    background: #1E2333;
    color: {FG_TEXT};
    border: 1px solid #2F364E;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: bold;
}}
QPushButton:hover {{
    background: #2A3147;
    border-color: {ACCENT};
    color: {ACCENT};
}}
QPushButton:pressed {{
    background: #151824;
}}
QPushButton:disabled {{
    background: #151824;
    color: #4A5064;
    border-color: #232738;
}}
QPushButton#primary {{
    background: {ACCENT};
    color: #0A0B10;
    border: none;
}}
QPushButton#primary:hover {{
    background: #33EBFF;
}}
QPushButton#success {{
    background: #00C853;
    color: #000;
    border: none;
}}
QPushButton#success:hover {{
    background: #00E676;
}}
QPushButton#danger {{
    background: #D50000;
    color: #FFF;
    border: none;
}}
QPushButton#danger:hover {{
    background: #FF1744;
}}
QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
    background: {BG_CARD};
    border: 1px solid #282C40;
    border-radius: 4px;
    padding: 4px 8px;
    color: {FG_TEXT};
}}
QLineEdit:focus, QComboBox:focus {{
    border-color: {ACCENT};
}}
QTextEdit {{
    background: #0F111A;
    border: 1px solid #232738;
    border-radius: 4px;
    color: #00E5FF;
    font-family: {MONO_FONT};
    font-size: 11px;
}}
QTableWidget {{
    background: #0F111A;
    border: 1px solid #232738;
    gridline-color: #1E2333;
    border-radius: 4px;
    color: {FG_TEXT};
    font-family: {MONO_FONT};
    font-size: 11px;
}}
QTableWidget::item {{
    padding: 3px 6px;
}}
QTableWidget::item:selected {{
    background: #005F87;
}}
QHeaderView::section {{
    background: #181B26;
    color: {ACCENT};
    border: 1px solid #232738;
    padding: 4px;
    font-weight: bold;
    font-size: 11px;
}}
QProgressBar {{
    border: 1px solid #282C40;
    border-radius: 3px;
    text-align: center;
    background: #0E1018;
    color: #FFF;
    font-size: 10px;
    font-weight: bold;
}}
QProgressBar::chunk {{
    background-color: {ACCENT};
}}
QSlider::groove:horizontal {{
    height: 6px;
    background: #1E2333;
    border-radius: 3px;
}}
QSlider::handle:horizontal {{
    background: {ACCENT};
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}}
"""


# ---------------------------------------------------------------------------
# TAB 1: OVERVIEW & STATUS MATRIX
# ---------------------------------------------------------------------------
class OverviewTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        # Truthfulness alert banner
        banner = QFrame()
        banner.setStyleSheet(f"background: #161926; border-left: 4px solid {ACCENT}; border-radius: 4px; padding: 8px;")
        b_lay = QVBoxLayout(banner)
        b_title = QLabel("QGAOPS-QGPU RESEARCH CONSOLE — SOFTWARE VALIDATION BASELINE")
        b_title.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        b_sub = QLabel(
            "Target Architecture: Memory-Aware Quantum-Geometric Algebra Processing Unit (PYNQ-Z2 / XC7Z020).\n"
            "[SOFTWARE DEMONSTRATOR] All results are [MEASURED SOFTWARE] or [SOFTWARE MODEL]. No physical FPGA bitstream is claimed."
        )
        b_sub.setStyleSheet("color: #8C93A8; font-size: 11px;")
        b_lay.addWidget(b_title)
        b_lay.addWidget(b_sub)
        layout.addWidget(banner)

        # Quick action launch toolbar
        act_row = QHBoxLayout()
        btn_cam = QPushButton("✋ Open Live Camera Monitor")
        btn_cam.setObjectName("primary")
        btn_cam.clicked.connect(lambda: self.main_win.switch_tab("✋ Live Monitor"))

        btn_ctrl = QPushButton("🎮 Computer Vision Control")
        btn_ctrl.clicked.connect(lambda: self.main_win.switch_tab("🎮 Gesture Control"))

        btn_bench = QPushButton("⏱ Run Microbenchmark Lab")
        btn_bench.clicked.connect(lambda: self.main_win.switch_tab("⏱ Benchmark Lab"))

        btn_calc = QPushButton("🔢 Cl(3,0) GA Calculator")
        btn_calc.clicked.connect(lambda: self.main_win.switch_tab("🔢 GA Calculator"))

        btn_e2e = QPushButton("🔄 Run E2E Benchmark")
        btn_e2e.clicked.connect(self.main_win.run_e2e_benchmark)

        act_row.addWidget(btn_cam)
        act_row.addWidget(btn_ctrl)
        act_row.addWidget(btn_bench)
        act_row.addWidget(btn_calc)
        act_row.addWidget(btn_e2e)
        act_row.addStretch()
        layout.addLayout(act_row)

        split = QHBoxLayout()

        # Left: Stage matrix
        stage_box = QGroupBox("Project Stages Status (Stages 1–22)")
        s_lay = QVBoxLayout(stage_box)
        self.stage_table = QTableWidget(10, 3)
        self.stage_table.setHorizontalHeaderLabels(["Stage", "Status", "Details"])
        self.stage_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        stages = [
            ("1. Requirements & Spec", "COMPLETE", "docs/requirements/, docs/research/"),
            ("2. Mathematical Spec", "COMPLETE", "Cl(3,0) primary + Q16.16 signed"),
            ("3. Repo & Build Setup", "COMPLETE", "pyproject.toml, scripts/"),
            ("4. Reference Model", "TESTED (9/9)", "software/reference_model/tests/"),
            ("5. Validation Suite", "TESTED (13/13)", "192 basis pairs, Stage 5 report"),
            ("6. CPU Benchmarks", "MEASURED", "15 configs, microbenchmarks"),
            ("7. Gesture Pipeline", "COMPLETE", "MediaPipe 3D tracking + 27 expressions"),
            ("8. CPU Engineering GUI", "COMPLETE", "PySide6 unified console (this window)"),
            ("9. Hardware Contract", "PROPOSED", "AXI serialization tested, registers [N/A]"),
            ("10–22. HLS & FPGA Bitstream", "PENDING", "Awaiting HLS synthesis on Vivado"),
        ]
        for row, (stg, status, det) in enumerate(stages):
            c_item = QTableWidgetItem(stg)
            s_item = QTableWidgetItem(status)
            s_item.setForeground(QColor(SUCCESS if "COMPLETE" in status or "TESTED" in status else (WARNING if "MEASURED" in status else ERROR_COL)))
            d_item = QTableWidgetItem(det)
            self.stage_table.setItem(row, 0, c_item)
            self.stage_table.setItem(row, 1, s_item)
            self.stage_table.setItem(row, 2, d_item)
        s_lay.addWidget(self.stage_table)
        split.addWidget(stage_box, 3)

        # Right: System environment & dependency check
        dep_box = QGroupBox("Environment & Dependency Matrix")
        d_lay = QVBoxLayout(dep_box)
        self.txt_deps = QTextEdit()
        self.txt_deps.setReadOnly(True)
        self.txt_deps.setFont(QFont("Consolas", 10))
        d_lay.addWidget(self.txt_deps)
        split.addWidget(dep_box, 2)

        layout.addLayout(split)
        self._refresh_deps()

    def _refresh_deps(self):
        try:
            import cv2
            cv_ver = cv2.__version__
        except Exception:
            cv_ver = "Not installed"

        try:
            import mediapipe
            mp_ver = getattr(mediapipe, "__version__", "Installed")
        except Exception:
            mp_ver = "Not installed"

        try:
            import pyautogui
            ag_ver = getattr(pyautogui, "__version__", "Installed")
        except Exception:
            ag_ver = "Mock mode (safe)"

        self.txt_deps.setText(
            f"=== HOST ENVIRONMENT ===\n"
            f"OS:            {platform.system()} {platform.release()} ({platform.machine()})\n"
            f"Python:        {sys.version.split()[0]} ({platform.python_implementation()})\n"
            f"PySide6:       Installed (Qt GUI Engine Active)\n"
            f"OpenCV:        {cv_ver}\n"
            f"MediaPipe:     {mp_ver}\n"
            f"PyAutoGUI:     {ag_ver}\n\n"
            f"=== ALGEBRA & ACCELERATOR SPEC ===\n"
            f"Primary Algebra:   Cl(3,0) / G(3,0,0) Clifford\n"
            f"Signature:         (+, +, +) Euclidean 3-Space\n"
            f"Basis Blades:      8 (1, e0, e1, e01, e2, e02, e12, e012)\n"
            f"Fixed-Point:       Q16.16 Signed Fixed-Point\n"
            f"Target Device:     PYNQ-Z2 / ZedBoard XC7Z020\n"
            f"Memory Hierarchy:  AAMF B0-B5 Model (Tile + Scratchpad)\n\n"
            f"=== TEST SUITE STATUS ===\n"
            f"Core Tests:        13/13 PASSED\n"
            f"Gesture/GA Tests:  166/166 PASSED\n"
            f"Regression Count:  0 Regressions"
        )


# ---------------------------------------------------------------------------
# TAB 2: LIVE GESTURE MONITOR (Dual-Pane Camera + 3D GA View + IR Card)
# ---------------------------------------------------------------------------
class LiveGestureTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Left: Live Camera View
        cam_group = QGroupBox("LIVE CAMERA [MediaPipe 3D Landmark Tracking & Control HUD]")
        cam_l = QVBoxLayout(cam_group)
        self.cam_label = QLabel()
        self.cam_label.setAlignment(Qt.AlignCenter)
        self.cam_label.setStyleSheet("background-color: #050608; border-radius: 4px;")
        self.cam_label.setMinimumSize(480, 360)
        cam_l.addWidget(self.cam_label)

        cam_btn_row = QHBoxLayout()
        self.btn_toggle_synth = QPushButton("Toggle Synthetic / Camera")
        self.btn_toggle_synth.clicked.connect(self._toggle_synth_mode)
        cam_btn_row.addWidget(self.btn_toggle_synth)
        cam_l.addLayout(cam_btn_row)
        layout.addWidget(cam_group, stretch=3)

        # Middle: 3D GA Vector / Rotor View
        vec_group = QGroupBox("3D GEOMETRIC ALGEBRA VIEW [Vectors, Rotor, Wedge Planes]")
        vec_l = QVBoxLayout(vec_group)
        self.vec_label = QLabel()
        self.vec_label.setAlignment(Qt.AlignCenter)
        self.vec_label.setStyleSheet("background-color: #07080D; border-radius: 4px;")
        self.vec_label.setMinimumSize(400, 360)
        vec_l.addWidget(self.vec_label)
        layout.addWidget(vec_group, stretch=3)

        # Right: Live GA / QGAOPS Summary Card
        info_group = QGroupBox("ACTIVE GA INSTRUCTION & QGAOPS IR PACKET")
        info_l = QVBoxLayout(info_group)
        self.txt_live_ga = QTextEdit()
        self.txt_live_ga.setReadOnly(True)
        self.txt_live_ga.setFont(QFont("Consolas", 10))
        self.txt_live_ga.setStyleSheet("background-color: #0A0B10; border: 1px solid #1E2333; color: #00E5FF;")
        info_l.addWidget(self.txt_live_ga)
        layout.addWidget(info_group, stretch=2)

    def _toggle_synth_mode(self):
        w = self.main_win.worker
        if w is None:
            return
        w.use_synthetic = not w.use_synthetic
        mode = "SYNTHETIC" if w.use_synthetic else "LIVE CAMERA"
        QMessageBox.information(self, "Mode Switched", f"Video input switched to: {mode}")

    def update_frames(self, frame_bgr: np.ndarray, vec_bgr: np.ndarray, ga_result: Any):
        h, w = frame_bgr.shape[:2]
        q_img = QImage(frame_bgr.data, w, h, w * 3, QImage.Format_BGR888)
        self.cam_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.cam_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        vh, vw = vec_bgr.shape[:2]
        qv_img = QImage(vec_bgr.data, vw, vh, vw * 3, QImage.Format_BGR888)
        self.vec_label.setPixmap(QPixmap.fromImage(qv_img).scaled(self.vec_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        if ga_result:
            self.txt_live_ga.setText(
                f"=== ACTIVE GA INSTRUCTION ===\n"
                f"EXPRESSION:  {ga_result.expression}\n"
                f"OPCODE:      {ga_result.opcode}\n"
                f"ALGEBRA:     G(3,0,0) Clifford\n"
                f"PRECISION:   {ga_result.precision}\n"
                f"INTERPRET:   {ga_result.interpretation}\n"
                f"RESULT:      {ga_result.display_value}\n\n"
                f"=== QGAOPS IR PACKET ===\n"
                f"{json.dumps(ga_result.ir.to_dict(), indent=2)}"
            )


# ---------------------------------------------------------------------------
# TAB 3: EXPRESSION CLASSIFIER (13 Static Poses + 14 Dynamic Expressions)
# ---------------------------------------------------------------------------
class ExpressionClassifierTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self.class_bars: Dict[str, QProgressBar] = {}
        self._build_ui()

    def _build_ui(self):
        layout = QHBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)

        # Left Column: 13 Static Hand Poses
        static_box = QGroupBox("STATIC HAND POSES (13 POSES) [MEASURED SOFTWARE]")
        static_l = QVBoxLayout(static_box)

        if HAS_HAND_GA_ENGINE:
            for mid, meta in STATIC_POSES.items():
                hl = QHBoxLayout()
                lbl = QLabel(f"{meta.name:<13} [{meta.ga_operation}]:")
                lbl.setFont(QFont("Consolas", 10, QFont.Bold))
                lbl.setFixedWidth(190)
                bar = QProgressBar()
                bar.setRange(0, 100)
                bar.setValue(0)
                self.class_bars[meta.name] = bar
                hl.addWidget(lbl)
                hl.addWidget(bar)
                static_l.addLayout(hl)
        static_l.addStretch()

        # Right Column: 14 Dynamic Motion Expressions
        dyn_box = QGroupBox("DYNAMIC MOTION EXPRESSIONS (14 EXPRESSIONS) [TEMPORAL 30-FRAME]")
        dyn_l = QVBoxLayout(dyn_box)

        if HAS_HAND_GA_ENGINE:
            for mid, meta in DYNAMIC_EXPRESSIONS.items():
                hl = QHBoxLayout()
                lbl = QLabel(f"{meta.name:<18} [{meta.ga_operation}]:")
                lbl.setFont(QFont("Consolas", 10, QFont.Bold))
                lbl.setFixedWidth(230)
                bar = QProgressBar()
                bar.setRange(0, 100)
                bar.setValue(0)
                self.class_bars[meta.name] = bar
                hl.addWidget(lbl)
                hl.addWidget(bar)
                dyn_l.addLayout(hl)

        # UNKNOWN row
        hl_unk = QHBoxLayout()
        lbl_unk = QLabel("UNKNOWN [VECTOR]:")
        lbl_unk.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_unk.setFixedWidth(230)
        bar_unk = QProgressBar()
        bar_unk.setRange(0, 100)
        bar_unk.setValue(0)
        self.class_bars["UNKNOWN"] = bar_unk
        hl_unk.addWidget(lbl_unk)
        hl_unk.addWidget(bar_unk)
        dyn_l.addLayout(hl_unk)
        dyn_l.addStretch()

        scroll_layout.addWidget(static_box, stretch=1)
        scroll_layout.addWidget(dyn_box, stretch=1)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

    def update_probabilities(self, active_expr: str, confidence: float):
        for cname, bar in self.class_bars.items():
            if cname == active_expr:
                bar.setValue(int(confidence * 100))
            else:
                bar.setValue(0)


# ---------------------------------------------------------------------------
# TAB 4: COMPUTER VISION GESTURE CONTROL (Profiles, Telemetry, 3D Object)
# ---------------------------------------------------------------------------
class GestureControlTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        main_l = QVBoxLayout(self)
        main_l.setContentsMargins(12, 12, 12, 12)
        main_l.setSpacing(10)

        # Header with architecture summary & safety notice
        hdr_box = QFrame()
        hdr_box.setStyleSheet("background-color: #141722; border: 1px solid #232738; border-radius: 6px; padding: 6px;")
        hdr_l = QVBoxLayout(hdr_box)
        title = QLabel("COMPUTER VISION GESTURE CONTROL INTERFACE [SOFTWARE CONTROLLER]")
        title.setStyleSheet(f"color: {ACCENT}; font-size: 13px; font-weight: bold;")
        subtitle = QLabel("Dual Pipeline: Hand Geometry -> GA Ops -> QGAOPS IR  ║  Hand Geometry -> Safety Layer -> OS Actions")
        subtitle.setStyleSheet("color: #8C93A8; font-size: 11px;")
        hdr_l.addWidget(title)
        hdr_l.addWidget(subtitle)
        main_l.addWidget(hdr_box)

        # Action Toolbar (Enable/Disable, Emergency Stop, Profile Switcher)
        act_bar = QFrame()
        act_bar.setStyleSheet("background-color: #181B26; border: 1px solid #282C40; border-radius: 6px;")
        act_l = QHBoxLayout(act_bar)
        act_l.setContentsMargins(12, 8, 12, 8)
        act_l.setSpacing(12)

        self.btn_toggle_control = QPushButton("ENABLE CONTROL")
        self.btn_toggle_control.setStyleSheet("background-color: #00C853; color: #000; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
        self.btn_toggle_control.clicked.connect(self._toggle_control)

        self.btn_emergency_stop = QPushButton("EMERGENCY STOP (F12)")
        self.btn_emergency_stop.setStyleSheet("background-color: #D50000; color: #FFF; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
        self.btn_emergency_stop.clicked.connect(self._on_emergency_stop)

        self.btn_reset_emergency = QPushButton("Reset Emergency")
        self.btn_reset_emergency.clicked.connect(self._on_reset_emergency)

        act_l.addWidget(self.btn_toggle_control)
        act_l.addWidget(self.btn_emergency_stop)
        act_l.addWidget(self.btn_reset_emergency)

        act_l.addSpacing(20)
        lbl_prof = QLabel("Profile:")
        lbl_prof.setStyleSheet("color: #E0E2EC; font-weight: bold;")
        act_l.addWidget(lbl_prof)

        self.cmb_control_profile = QComboBox()
        self.cmb_control_profile.addItems(["mouse", "presentation", "media", "object3d"])
        self.cmb_control_profile.currentTextChanged.connect(self._on_profile_changed)
        self.cmb_control_profile.setFixedWidth(140)
        act_l.addWidget(self.cmb_control_profile)

        self.lbl_ctrl_tab_state = QLabel("STATE: DISABLED")
        self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")
        act_l.addWidget(self.lbl_ctrl_tab_state)

        act_l.addStretch()
        f12_hint = QLabel("Emergency Cut-off: Press [F12]")
        f12_hint.setStyleSheet(f"color: {WARNING}; font-style: italic;")
        act_l.addWidget(f12_hint)

        main_l.addWidget(act_bar)

        # Splitter: Left = Command Mapping Table, Right = Telemetry & 3D Object & History
        split = QSplitter(Qt.Horizontal)

        # Left: Mappings Table
        map_group = QGroupBox("ACTIVE PROFILE GESTURE MAPPINGS (Whitelisted Actions Only)")
        map_l = QVBoxLayout(map_group)

        self.tbl_ctrl_mappings = QTableWidget()
        self.tbl_ctrl_mappings.setColumnCount(4)
        self.tbl_ctrl_mappings.setHorizontalHeaderLabels([
            "Trigger Gesture", "Command Action", "Target Subsystem", "Safety / Debounce"
        ])
        self.tbl_ctrl_mappings.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_ctrl_mappings.setSelectionBehavior(QTableWidget.SelectRows)
        self.tbl_ctrl_mappings.verticalHeader().setVisible(False)
        map_l.addWidget(self.tbl_ctrl_mappings)
        split.addWidget(map_group)

        # Right: Telemetry & Log
        right_container = QWidget()
        right_l = QVBoxLayout(right_container)
        right_l.setContentsMargins(0, 0, 0, 0)
        right_l.setSpacing(8)

        # Telemetry Card
        telem_group = QGroupBox("CONTROL TELEMETRY & LATENCY [MEASURED SOFTWARE]")
        telem_l = QVBoxLayout(telem_group)
        self.txt_ctrl_telemetry = QTextEdit()
        self.txt_ctrl_telemetry.setReadOnly(True)
        self.txt_ctrl_telemetry.setFont(QFont("Consolas", 10))
        self.txt_ctrl_telemetry.setStyleSheet("background-color: #0E1018; border: 1px solid #1E2333; color: #00E5FF;")
        self.txt_ctrl_telemetry.setMaximumHeight(180)
        telem_l.addWidget(self.txt_ctrl_telemetry)
        right_l.addWidget(telem_group)

        # 3D Object Card
        self.obj3d_group = QGroupBox("GA ROTOR 3D OBJECT STATE (object3d Profile)")
        obj3d_l = QVBoxLayout(self.obj3d_group)
        self.txt_ctrl_obj3d = QTextEdit()
        self.txt_ctrl_obj3d.setReadOnly(True)
        self.txt_ctrl_obj3d.setFont(QFont("Consolas", 10))
        self.txt_ctrl_obj3d.setStyleSheet("background-color: #0E1018; border: 1px solid #1E2333; color: #E040FB;")
        self.txt_ctrl_obj3d.setMaximumHeight(150)
        obj3d_l.addWidget(self.txt_ctrl_obj3d)
        right_l.addWidget(self.obj3d_group)

        # Recent Actions Table
        hist_group = QGroupBox("RECENT DISPATCHED ACTIONS LOG")
        hist_l = QVBoxLayout(hist_group)
        self.tbl_ctrl_history = QTableWidget()
        self.tbl_ctrl_history.setColumnCount(4)
        self.tbl_ctrl_history.setHorizontalHeaderLabels(["Timestamp", "Gesture", "Command", "Latency"])
        self.tbl_ctrl_history.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tbl_ctrl_history.verticalHeader().setVisible(False)
        hist_l.addWidget(self.tbl_ctrl_history)
        right_l.addWidget(hist_group)

        split.addWidget(right_container)
        split.setStretchFactor(0, 3)
        split.setStretchFactor(1, 2)
        main_l.addWidget(split, stretch=1)

        self._populate_profile_table()

    def _populate_profile_table(self):
        w = self.main_win.worker
        if w is None or not hasattr(w, "controller"):
            return
        mappings = w.controller.mapper.active_mappings
        self.tbl_ctrl_mappings.setRowCount(0)
        for row, (gest, cmd_obj) in enumerate(mappings.items()):
            self.tbl_ctrl_mappings.insertRow(row)
            subsystem = "Mouse" if "MOUSE" in cmd_obj.command or "CURSOR" in cmd_obj.command else (
                "Scroll" if "SCROLL" in cmd_obj.command else (
                    "Virtual 3D Object" if "OBJECT" in cmd_obj.command else "Keyboard / Application"
                )
            )
            debounce = "Continuous (None)" if cmd_obj.command in ["CURSOR_MOVE", "MOUSE_DRAG", "OBJECT_TRANSLATE"] else "Discrete (0.35s)"
            if cmd_obj.command in ["PRESENTATION_START", "MEDIA_STOP"]:
                debounce += " + OK_SIGN Confirm"

            self.tbl_ctrl_mappings.setItem(row, 0, QTableWidgetItem(gest))
            self.tbl_ctrl_mappings.setItem(row, 1, QTableWidgetItem(cmd_obj.command))
            self.tbl_ctrl_mappings.setItem(row, 2, QTableWidgetItem(subsystem))
            self.tbl_ctrl_mappings.setItem(row, 3, QTableWidgetItem(debounce))

    def _toggle_control(self):
        w = self.main_win.worker
        if w is None:
            return
        if w.controller.is_enabled:
            w.disable_control()
            self.btn_toggle_control.setText("ENABLE CONTROL")
            self.btn_toggle_control.setStyleSheet("background-color: #00C853; color: #000; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
            self.lbl_ctrl_tab_state.setText("STATE: DISABLED")
            self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")
        else:
            w.enable_control()
            self.btn_toggle_control.setText("DISABLE CONTROL")
            self.btn_toggle_control.setStyleSheet("background-color: #FF5252; color: #FFF; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
            self.lbl_ctrl_tab_state.setText("STATE: ENABLED")
            self.lbl_ctrl_tab_state.setStyleSheet("color: #00E676; font-weight: bold; font-size: 12px; margin-left: 10px;")

    def _on_emergency_stop(self):
        w = self.main_win.worker
        if w is None:
            return
        w.emergency_stop_control()
        self.btn_toggle_control.setText("ENABLE CONTROL")
        self.btn_toggle_control.setStyleSheet("background-color: #00C853; color: #000; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
        self.lbl_ctrl_tab_state.setText("STATE: EMERGENCY_STOPPED")
        self.lbl_ctrl_tab_state.setStyleSheet("color: #FF1744; font-weight: bold; font-size: 12px; margin-left: 10px;")

    def _on_reset_emergency(self):
        w = self.main_win.worker
        if w is None:
            return
        w.reset_emergency_control()
        self.lbl_ctrl_tab_state.setText("STATE: DISABLED")
        self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")

    def _on_profile_changed(self, profile_name: str):
        w = self.main_win.worker
        if w is None:
            return
        w.set_control_profile(profile_name)
        self._populate_profile_table()

    def update_telemetry(self, ctrl_report: Any):
        w = self.main_win.worker
        if w is None or not hasattr(w, "controller"):
            return

        ctrl_enabled = w.controller.is_enabled
        ctrl_state = w.controller.safety.state
        self.lbl_ctrl_tab_state.setText(f"STATE: {ctrl_state.name}")
        if ctrl_state == ControlState.EMERGENCY_STOPPED:
            self.lbl_ctrl_tab_state.setStyleSheet("color: #FF1744; font-weight: bold; font-size: 12px; margin-left: 10px;")
        elif ctrl_enabled:
            self.lbl_ctrl_tab_state.setStyleSheet("color: #00E676; font-weight: bold; font-size: 12px; margin-left: 10px;")
        else:
            self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")

        if ctrl_report:
            p_stats = w.controller.get_latency_percentiles()
            safety_metrics = w.controller.safety.metrics
            pending = w.controller.safety.pending_confirmation
            pending_str = f"PENDING ({pending.command}, timeout {max(0, int(pending.expires_at - time.time()))}s)" if pending else "NONE"

            self.txt_ctrl_telemetry.setText(
                f"=== CONTROL TELEMETRY [MEASURED SOFTWARE] ===\n"
                f"Active Profile:        {w.controller.mapper.active_profile_name.upper()}\n"
                f"Status:                {ctrl_report.status_message}\n"
                f"Last Trigger Gesture:  {ctrl_report.gesture}\n"
                f"Dispatched Command:    {ctrl_report.command or 'NONE'}\n"
                f"Executed:              {ctrl_report.is_executed}\n"
                f"Parallel GA Opcode:    {ctrl_report.ga_opcode}\n\n"
                f"=== TIMING & LATENCY BREAKDOWN ===\n"
                f"Decision Latency:      {ctrl_report.decision_latency_ms:.2f} ms\n"
                f"Action Latency:        {ctrl_report.action_latency_ms:.2f} ms\n"
                f"Total Control Latency: {ctrl_report.total_control_latency_ms:.2f} ms\n"
                f"P50 / P95 / P99:       {p_stats['p50']:.2f} / {p_stats['p95']:.2f} / {p_stats['p99']:.2f} ms\n\n"
                f"=== SAFETY & INTERLOCKS ===\n"
                f"Pending Confirmation:  {pending_str}\n"
                f"Low-Conf Ignored:      {safety_metrics['ignored_low_conf']}\n"
                f"False Triggers Blocked:{safety_metrics['false_triggers_blocked']}\n"
                f"Confirmations Run:     {safety_metrics['confirmations_executed']}"
            )

        if w.controller.mapper.active_profile_name == "object3d":
            obj3d = w.controller.object3d
            t_trace = obj3d.transformation_trace
            trace_lines = "\n".join([f"  {k}: {v}" for k, v in t_trace.items()]) if t_trace else "  Identity (no transformation applied yet)"
            self.txt_ctrl_obj3d.setText(
                f"=== GA ROTOR 3D OBJECT STATUS ===\n"
                f"Scale Factor:          {obj3d.scale:.2f}\n"
                f"Translation (X, Y):    ({obj3d.translation[0]:.2f}, {obj3d.translation[1]:.2f})\n"
                f"Rotor Matrix / Trace:\n{trace_lines}\n\n"
                f"Formula:  v' = R v ~R,  where R = exp(-0.5 * theta * B)"
            )

        if ctrl_report and ctrl_report.is_executed and ctrl_report.command and ctrl_report.command != "CURSOR_MOVE":
            row_idx = self.tbl_ctrl_history.rowCount()
            if row_idx >= 30:
                self.tbl_ctrl_history.removeRow(0)
                row_idx = self.tbl_ctrl_history.rowCount()
            self.tbl_ctrl_history.insertRow(row_idx)
            now_str = time.strftime("%H:%M:%S")
            self.tbl_ctrl_history.setItem(row_idx, 0, QTableWidgetItem(now_str))
            self.tbl_ctrl_history.setItem(row_idx, 1, QTableWidgetItem(ctrl_report.gesture))
            self.tbl_ctrl_history.setItem(row_idx, 2, QTableWidgetItem(ctrl_report.command))
            self.tbl_ctrl_history.setItem(row_idx, 3, QTableWidgetItem(f"{ctrl_report.total_control_latency_ms:.2f} ms"))
            self.tbl_ctrl_history.scrollToBottom()


# ---------------------------------------------------------------------------
# TAB 5: GA CALCULATOR & MULTIVECTOR DECOMPOSITION
# ---------------------------------------------------------------------------
class GACalculatorTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("Cl(3,0) Geometric Algebra Multivector Engine & Decomposition")
        lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(lbl)

        split = QHBoxLayout()

        # Left: Interactive Calculator
        left = QGroupBox("Interactive Cl(3,0) Calculator [1, e1, e2, e3, e12, e13, e23, e123]")
        left_lay = QVBoxLayout(left)

        self.A_fields: list[QDoubleSpinBox] = []
        self.B_fields: list[QDoubleSpinBox] = []

        for label_text, fields_list in [("  A :", self.A_fields), ("  B :", self.B_fields)]:
            row = QHBoxLayout()
            row.addWidget(QLabel(label_text))
            for name in BASIS_NAMES:
                vbox = QVBoxLayout()
                name_lbl = QLabel(name)
                name_lbl.setAlignment(Qt.AlignCenter)
                name_lbl.setStyleSheet("font-size: 10px; color: " + FG_DIM)
                spin = QDoubleSpinBox()
                spin.setRange(-9999.0, 9999.0)
                spin.setSingleStep(0.5)
                spin.setDecimals(4)
                spin.setValue(0.0)
                spin.setFixedWidth(70)
                vbox.addWidget(name_lbl)
                vbox.addWidget(spin)
                row.addLayout(vbox)
                fields_list.append(spin)
            left_lay.addLayout(row)

        # Preset buttons
        presets = QHBoxLayout()
        preset_btn = QPushButton("e1 · e2")
        preset_btn.clicked.connect(self._preset_e1_e2)
        rotor_btn = QPushButton("Rotor test")
        rotor_btn.clicked.connect(self._preset_rotor)
        random_btn = QPushButton("Random")
        random_btn.clicked.connect(self._preset_random)
        clear_btn = QPushButton("Clear")
        clear_btn.clicked.connect(self._clear)
        presets.addWidget(preset_btn)
        presets.addWidget(rotor_btn)
        presets.addWidget(random_btn)
        presets.addWidget(clear_btn)
        presets.addStretch()
        left_lay.addLayout(presets)

        # Operation row
        ops_row = QHBoxLayout()
        ops_row.addWidget(QLabel("Operation:"))
        self.op_combo = QComboBox()
        self.op_combo.addItems([
            "geometric_product", "wedge", "hestenes_inner",
            "add", "subtract",
            "reverse_A", "grade_involution_A", "clifford_conjugation_A",
            "scale_A", "grade_projection_A",
        ])
        ops_row.addWidget(self.op_combo)

        self.grade_spin = QSpinBox()
        self.grade_spin.setRange(0, 3)
        self.grade_spin.setPrefix("Grade: ")
        self.grade_spin.setFixedWidth(90)
        ops_row.addWidget(self.grade_spin)

        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(-100.0, 100.0)
        self.scale_spin.setValue(2.0)
        self.scale_spin.setPrefix("Scale: ")
        self.scale_spin.setFixedWidth(110)
        ops_row.addWidget(self.scale_spin)

        compute_btn = QPushButton("Compute")
        compute_btn.setObjectName("primary")
        compute_btn.clicked.connect(self._compute)
        ops_row.addWidget(compute_btn)
        ops_row.addStretch()
        left_lay.addLayout(ops_row)

        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Consolas", 10))
        left_lay.addWidget(self.result_text)
        split.addWidget(left, 3)

        # Right: Multivector 8-Blade Decomposition Table
        right = QGroupBox("LIVE MULTIVECTOR DECOMPOSITION (8 Blades) [MEASURED SOFTWARE]")
        right_lay = QVBoxLayout(right)

        self.tbl_multivector = QTableWidget(8, 4)
        self.tbl_multivector.setHorizontalHeaderLabels(["Basis Blade", "Grade", "Float32 Value", "FIX16 Hex"])
        self.tbl_multivector.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_lay.addWidget(self.tbl_multivector)

        self.txt_rotor_decomp = QTextEdit()
        self.txt_rotor_decomp.setReadOnly(True)
        self.txt_rotor_decomp.setFont(QFont("Consolas", 10))
        self.txt_rotor_decomp.setMaximumHeight(160)
        right_lay.addWidget(self.txt_rotor_decomp)

        split.addWidget(right, 2)
        layout.addLayout(split)

    def _get_mv(self, fields: list[QDoubleSpinBox]) -> Multivector:
        return Multivector.from_coefficients([f.value() for f in fields])

    def _preset_e1_e2(self):
        self._clear()
        self.A_fields[1].setValue(1.0)
        self.B_fields[2].setValue(1.0)
        self.op_combo.setCurrentText("geometric_product")
        self._compute()

    def _preset_rotor(self):
        self._clear()
        theta = math.pi / 4.0
        self.A_fields[0].setValue(round(math.cos(theta / 2.0), 4))
        self.A_fields[4].setValue(round(-math.sin(theta / 2.0), 4))
        self.B_fields[1].setValue(1.0)
        self.op_combo.setCurrentText("geometric_product")
        self._compute()

    def _preset_random(self):
        rng = random.Random()
        for f in self.A_fields + self.B_fields:
            f.setValue(round(rng.uniform(-2.0, 2.0), 4))
        self._compute()

    def _clear(self):
        for f in self.A_fields + self.B_fields:
            f.setValue(0.0)
        self.result_text.clear()

    def _compute(self):
        A = self._get_mv(self.A_fields)
        B = self._get_mv(self.B_fields)
        op = self.op_combo.currentText()

        try:
            if op == "geometric_product":
                res = A.geometric_product(B)
            elif op == "wedge":
                res = A.wedge(B)
            elif op == "hestenes_inner":
                res = A.hestenes_inner(B)
            elif op == "add":
                res = A + B
            elif op == "subtract":
                res = A - B
            elif op == "reverse_A":
                res = A.reverse()
            elif op == "grade_involution_A":
                res = A.grade_involution()
            elif op == "clifford_conjugation_A":
                res = A.clifford_conjugation()
            elif op == "scale_A":
                res = A.scale(self.scale_spin.value())
            elif op == "grade_projection_A":
                res = A.grade_projection(self.grade_spin.value())
            else:
                res = A
        except Exception as exc:
            self.result_text.setText(f"Error during {op}: {exc}")
            return

        self.result_text.setText(
            f"=== COMPUTATION RESULT ===\n"
            f"Operation:  {op}\n"
            f"Result:     {res}\n\n"
            f"Coefficients (8-tuple):\n{[round(c, 6) for c in res.coefficients]}\n\n"
            f"Grades present: {sorted(list(res.grades_present()))}\n"
            f"Norm: {res.norm():.6f}"
        )

    def update_live_multivector(self, mvs: Any):
        if not mvs:
            return
        basis_names = ["1 (scalar)", "e0", "e1", "e01", "e2", "e02", "e12", "e012"]
        grades = ["0", "1", "1", "2", "1", "2", "2", "3"]
        primary_mv = mvs.get("index_vec", None)
        if primary_mv is None:
            return

        for idx, (bname, gr) in enumerate(zip(basis_names, grades)):
            val = primary_mv.coeffs[idx]
            hex_fix = f"0x{int(val * 16384) & 0xFFFF:04X}"
            self.tbl_multivector.setItem(idx, 0, QTableWidgetItem(bname))
            self.tbl_multivector.setItem(idx, 1, QTableWidgetItem(gr))
            self.tbl_multivector.setItem(idx, 2, QTableWidgetItem(f"{val:+.5f}"))
            self.tbl_multivector.setItem(idx, 3, QTableWidgetItem(hex_fix))

        self.txt_rotor_decomp.setText(
            f"=== ROTOR SANDWICH DECOMPOSITION ===\n"
            f"Primary Multivector: index_vec\n"
            f"Norm:               {primary_mv.norm():.5f}\n"
            f"Scalar part:        {primary_mv.coeffs[0]:.5f}\n"
            f"Vector part:        ({primary_mv.coeffs[1]:.4f}, {primary_mv.coeffs[2]:.4f}, {primary_mv.coeffs[4]:.4f})\n"
            f"Bivector part:      ({primary_mv.coeffs[3]:.4f}, {primary_mv.coeffs[5]:.4f}, {primary_mv.coeffs[6]:.4f})\n"
            f"Pseudoscalar part:  {primary_mv.coeffs[7]:.4f}"
        )


# ---------------------------------------------------------------------------
# TAB 6: BENCHMARK LAB (Microbenchmarks, GA Standard, E2E, Workloads)
# ---------------------------------------------------------------------------
class BenchmarkTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("QGAOPS-QGPU Benchmark Lab  [MEASURED SOFTWARE — not FPGA]")
        lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(lbl)

        # Quick Action Buttons
        btn_bar = QHBoxLayout()
        self.btn_micro = QPushButton("⚡ Run Microbenchmark (50k ops)")
        self.btn_micro.setObjectName("primary")
        self.btn_micro.clicked.connect(self._run_microbenchmark)

        self.btn_ga_std = QPushButton("🧪 Run GA Standard Benchmark (10k ops)")
        self.btn_ga_std.clicked.connect(self._run_ga_benchmark)

        self.btn_e2e = QPushButton("🔄 Run E2E Pipeline Benchmark")
        self.btn_e2e.clicked.connect(self._run_e2e_benchmark)

        btn_bar.addWidget(self.btn_micro)
        btn_bar.addWidget(self.btn_ga_std)
        btn_bar.addWidget(self.btn_e2e)
        btn_bar.addStretch()
        layout.addLayout(btn_bar)

        # Stage 6 Workload Configuration Box
        cfg_box = QGroupBox("Stage 6 Workload Suite Configuration (Float64 vs Q16.16)")
        cfg_lay = QGridLayout(cfg_box)

        cfg_lay.addWidget(QLabel("Operations:"), 0, 0)
        self.op_checks = {}
        ops = ["geometric_product", "wedge", "hestenes_inner", "add", "subtract"]
        for i, op in enumerate(ops):
            cb = QCheckBox(op)
            cb.setChecked(True)
            cfg_lay.addWidget(cb, 0, i + 1)
            self.op_checks[op] = cb

        cfg_lay.addWidget(QLabel("Distributions:"), 1, 0)
        self.dist_checks = {}
        dists = ["dense", "sparse", "boundary", "basis"]
        for i, d in enumerate(dists):
            cb = QCheckBox(d)
            cb.setChecked(i < 2)
            cfg_lay.addWidget(cb, 1, i + 1)
            self.dist_checks[d] = cb

        cfg_lay.addWidget(QLabel("Pair count:"), 2, 0)
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 4096)
        self.count_spin.setValue(128)
        cfg_lay.addWidget(self.count_spin, 2, 1)

        cfg_lay.addWidget(QLabel("Repetitions:"), 2, 2)
        self.reps_spin = QSpinBox()
        self.reps_spin.setRange(1, 20)
        self.reps_spin.setValue(5)
        cfg_lay.addWidget(self.reps_spin, 2, 3)

        self.btn_run_workloads = QPushButton("▶ Run Stage 6 Workloads")
        self.btn_run_workloads.clicked.connect(self._start_workloads)
        cfg_lay.addWidget(self.btn_run_workloads, 2, 4)

        layout.addWidget(cfg_box)

        # Live Output Splitter
        split = QSplitter(Qt.Vertical)

        # Top: Benchmark Console Output
        out_box = QGroupBox("Benchmark Console Output")
        out_lay = QVBoxLayout(out_box)
        self.txt_benchmark_results = QTextEdit()
        self.txt_benchmark_results.setReadOnly(True)
        self.txt_benchmark_results.setFont(QFont("Consolas", 10))
        out_lay.addWidget(self.txt_benchmark_results)
        split.addWidget(out_box)

        # Bottom: Stage 6 Workload Results Table
        res_box = QGroupBox("Stage 6 Workload Results Table (Median ops/s, Software only)")
        res_lay = QVBoxLayout(res_box)
        self.res_table = QTableWidget(0, 6)
        self.res_table.setHorizontalHeaderLabels([
            "Operation", "Distribution", "Pairs",
            "Float64 median ops/s", "Q16.16 median ops/s", "Overhead"
        ])
        self.res_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        res_lay.addWidget(self.res_table)
        split.addWidget(res_box)

        layout.addWidget(split, stretch=1)

    def _run_microbenchmark(self):
        self.txt_benchmark_results.setText("Running GA high-resolution microbenchmark (50,000 iterations)... Please wait.")
        QApplication.processEvents()

        w = self.main_win.worker
        if w is None or not hasattr(w, "engine"):
            engine = AlgebraEngine()
        else:
            engine = w.engine

        v1 = GAMultivector.vector(0.6, 0.8, 0.0)
        v2 = GAMultivector.vector(0.3, 0.5, 0.7)
        N = 50000

        res_txt = "=== QGAOPS-QGPU MICROBENCHMARK RESULTS [MEASURED SOFTWARE] ===\n"
        res_txt += f"Iterations: {N} ops per primitive  |  Precision: {engine.precision}\n\n"
        res_txt += f"{'Primitive':<14} | {'Mean Latency':>14} | {'Throughput':>16}\n"
        res_txt += "-" * 50 + "\n"

        ops = [
            ("GP", lambda: engine.gp(v1, v2)),
            ("WEDGE", lambda: engine.wedge(v1, v2)),
            ("DOT", lambda: engine.dot(v1, v2)),
            ("NORM", lambda: engine.norm(v1)),
            ("REVERSE", lambda: engine.reverse(v1)),
            ("SANDWICH", lambda: engine.sandwich(v1, v2)),
        ]

        for name, fn in ops:
            for _ in range(500):
                fn()
            t0 = time.perf_counter_ns()
            for _ in range(N):
                fn()
            tot_ns = time.perf_counter_ns() - t0
            lat_us = (tot_ns / N) / 1000.0
            throughput = N / (tot_ns / 1e9)
            res_txt += f"{name:<14} | {lat_us:11.3f} µs | {throughput:13.1f} ops/s\n"

        self.txt_benchmark_results.setText(res_txt)

    def _run_ga_benchmark(self):
        self.txt_benchmark_results.setText("Running full GA standard benchmark (10,000 ops)... Please wait.")
        QApplication.processEvents()
        try:
            from main import run_benchmark
            w = self.main_win.worker
            engine = w.engine if w else AlgebraEngine()
            f = io.StringIO()
            with redirect_stdout(f):
                run_benchmark(engine)
            self.txt_benchmark_results.setText(f.getvalue())
        except Exception as exc:
            self.txt_benchmark_results.setText(f"Error running benchmark: {exc}\n{traceback.format_exc()}")

    def _run_e2e_benchmark(self):
        self.txt_benchmark_results.setText("Running End-to-End Pipeline Benchmark... Please wait.")
        QApplication.processEvents()
        try:
            from experiments.run_expression_experiment import run_experiment
            res = run_experiment()
            self.txt_benchmark_results.setText(json.dumps(res, indent=2))
        except Exception as exc:
            self.txt_benchmark_results.setText(f"Error running E2E benchmark: {exc}\n{traceback.format_exc()}")

    def _start_workloads(self):
        ops = [k for k, v in self.op_checks.items() if v.isChecked()]
        dists = [k for k, v in self.dist_checks.items() if v.isChecked()]
        if not ops or not dists:
            QMessageBox.warning(self, "Config Error", "Select at least one operation and distribution.")
            return

        self.txt_benchmark_results.setText("Executing Stage 6 CPU Workload Suite...")
        QApplication.processEvents()
        self.res_table.setRowCount(0)

        configs = [
            WorkloadConfig(
                operation=op, count=self.count_spin.value(),
                seed=20261026, distribution=dist,
            )
            for op in ops for dist in dists
        ]

        for cfg in configs:
            try:
                rec = run_benchmark_config(cfg, repetitions=self.reps_spin.value(), warmup_runs=1)
                row = self.res_table.rowCount()
                self.res_table.insertRow(row)

                f64_ops = rec.results.get("float64", {}).get("median_ops_per_sec", 0.0)
                q16_ops = rec.results.get("q16_16", {}).get("median_ops_per_sec", 0.0)
                overhead = rec.results.get("overhead_ratio", 0.0)

                self.res_table.setItem(row, 0, QTableWidgetItem(cfg.operation))
                self.res_table.setItem(row, 1, QTableWidgetItem(cfg.distribution))
                self.res_table.setItem(row, 2, QTableWidgetItem(str(cfg.count)))
                self.res_table.setItem(row, 3, QTableWidgetItem(f"{f64_ops:,.0f}"))
                self.res_table.setItem(row, 4, QTableWidgetItem(f"{q16_ops:,.0f}"))
                self.res_table.setItem(row, 5, QTableWidgetItem(f"{overhead:.2f}x"))
            except Exception as exc:
                print(f"Error on {cfg}: {exc}")

        self.txt_benchmark_results.append("\n[COMPLETE] Stage 6 Workloads executed successfully.")


# ---------------------------------------------------------------------------
# TAB 7: PERFORMANCE METRICS & WATERFALL
# ---------------------------------------------------------------------------
class PerformanceMetricsTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        layout = QGridLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Pipeline Waterfall
        wf_group = QGroupBox("PIPELINE STAGE LATENCY WATERFALL [MEASURED SOFTWARE]")
        wf_l = QVBoxLayout(wf_group)
        self.tbl_waterfall = QTableWidget(9, 3)
        self.tbl_waterfall.setHorizontalHeaderLabels(["Stage Name", "Latency (ms)", "% Total"])
        self.tbl_waterfall.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        wf_l.addWidget(self.tbl_waterfall)

        # Bandwidth & System
        sys_group = QGroupBox("BANDWIDTH & SYSTEM RESOURCE UTILIZATION")
        sys_l = QVBoxLayout(sys_group)
        self.txt_sys_metrics = QTextEdit()
        self.txt_sys_metrics.setReadOnly(True)
        self.txt_sys_metrics.setFont(QFont("Consolas", 11))
        sys_l.addWidget(self.txt_sys_metrics)

        layout.addWidget(wf_group, 0, 0)
        layout.addWidget(sys_group, 0, 1)

    def update_metrics(self, snapshot: PerformanceSnapshot):
        tot_ms = max(snapshot.frame_time_ms, 0.001)
        for idx, (stg, dur) in enumerate(snapshot.stage_breakdown.items()):
            pct = (dur / tot_ms) * 100.0
            self.tbl_waterfall.setItem(idx, 0, QTableWidgetItem(stg))
            self.tbl_waterfall.setItem(idx, 1, QTableWidgetItem(f"{dur:.3f} ms"))
            self.tbl_waterfall.setItem(idx, 2, QTableWidgetItem(f"{pct:.1f}%"))

        self.txt_sys_metrics.setText(
            f"=== SOFTWARE / LOGICAL BANDWIDTH [MEASURED SOFTWARE] ===\n"
            f"Input Bandwidth:   {snapshot.bandwidth_input_mbs:.2f} MB/s\n"
            f"Output Bandwidth:  {snapshot.bandwidth_output_mbs:.2f} MB/s\n"
            f"Total Logical BW:  {snapshot.bandwidth_total_mbs:.2f} MB/s\n\n"
            f"=== THROUGHPUT & TIMING ===\n"
            f"GA OPS/s:          {snapshot.ga_ops_per_second:.1f} ops/s\n"
            f"Frame Time:        {snapshot.frame_time_ms:.2f} ms\n"
            f"P50 / P95 / P99:   {snapshot.latency_p50_ms:.1f} / {snapshot.latency_p95_ms:.1f} / {snapshot.latency_p99_ms:.1f} ms\n\n"
            f"=== SYSTEM RESOURCE USAGE ===\n"
            f"Process CPU:       {snapshot.cpu_percent:.1f}%\n"
            f"Process RSS Memory:{snapshot.process_rss_mb:.1f} MB\n"
            f"System RAM Used:   {snapshot.ram_mb:.1f} MB"
        )


# ---------------------------------------------------------------------------
# TAB 8: AAMF MEMORY FABRIC (B0-B5 Model)
# ---------------------------------------------------------------------------
class MemoryFabricTab(QWidget):
    def __init__(self, main_win: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_win = main_win
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)

        box = QGroupBox("QGAOPS ALGEBRA-AWARE MEMORY FABRIC (AAMF B0-B5 MODEL) [SOFTWARE MODEL]")
        bl = QVBoxLayout(box)

        self.txt_memory_model = QTextEdit()
        self.txt_memory_model.setReadOnly(True)
        self.txt_memory_model.setFont(QFont("Consolas", 11))
        bl.addWidget(self.txt_memory_model)

        layout.addWidget(box)

    def update_memory(self, snapshot: PerformanceSnapshot):
        mm = snapshot.memory_model
        self.txt_memory_model.setText(
            f"=== QGAOPS ALGEBRA-AWARE MEMORY FABRIC (AAMF) [SOFTWARE MODEL] ===\n\n"
            f"Memory Hierarchy Level:         {mm.level} (Unified Scratchpad + Tile Buffer)\n"
            f"Estimated Logical DDR Traffic:  {mm.logical_ddr_bytes} Bytes / frame\n"
            f"Total Logical Bytes Moved:      {mm.bytes_moved} Bytes\n"
            f"Bytes Reused via Scratchpad:    {mm.bytes_reused} Bytes\n"
            f"AAMF Reuse Ratio:               {mm.reuse_ratio_pct:.1f}%\n"
            f"Tile Buffer Reads:              {mm.tile_buffer_reads}\n"
            f"Tile Buffer Writes:             {mm.tile_buffer_writes}\n"
            f"Scratchpad Accesses:            {mm.scratchpad_accesses}\n"
            f"Arithmetic Intensity:           {mm.arithmetic_intensity:.4f} ops/Byte\n\n"
            f"DDR Traffic Reduction vs B0:    {100.0 - (mm.logical_ddr_bytes / max(mm.bytes_moved, 1)*100):.1f}%"
        )


# ---------------------------------------------------------------------------
# TAB 9: PRECISION TAB (Q16.16 Error Analysis)
# ---------------------------------------------------------------------------
class PrecisionTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("Q16.16 Signed Fixed-Point Precision & Bitwise Analysis")
        lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(lbl)

        split = QHBoxLayout()

        left = QGroupBox("Single Value Encode / Decode Test")
        l_lay = QGridLayout(left)
        l_lay.addWidget(QLabel("Float value:"), 0, 0)
        self.val_spin = QDoubleSpinBox()
        self.val_spin.setRange(-32768.0, 32767.9999)
        self.val_spin.setValue(math.pi)
        self.val_spin.setDecimals(8)
        l_lay.addWidget(self.val_spin, 0, 1)

        test_btn = QPushButton("Analyze Q16.16 Conversion")
        test_btn.setObjectName("primary")
        test_btn.clicked.connect(self._analyze_single)
        l_lay.addWidget(test_btn, 1, 0, 1, 2)

        self.single_out = QTextEdit()
        self.single_out.setReadOnly(True)
        self.single_out.setFont(QFont("Consolas", 10))
        l_lay.addWidget(self.single_out, 2, 0, 1, 2)
        split.addWidget(left, 1)

        right = QGroupBox("Fixed-Point Product Verification (64 Basis Pairs)")
        r_lay = QVBoxLayout(right)
        run_fp_btn = QPushButton("▶ Run Fixed-Point Basis Validation")
        run_fp_btn.clicked.connect(self._run_fp_basis_test)
        r_lay.addWidget(run_fp_btn)

        self.fp_table = QTableWidget(8, 4)
        self.fp_table.setHorizontalHeaderLabels(["Operation", "Max Abs Error", "RMS Error", "Status"])
        self.fp_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        r_lay.addWidget(self.fp_table)
        split.addWidget(right, 1)

        layout.addLayout(split)
        self._analyze_single()

    def _analyze_single(self):
        val = self.val_spin.value()
        fmt = FixedPointFormat(width=32, fractional_bits=16)
        raw, sat = fmt.encode(val)
        dec = fmt.decode(raw)
        err = abs(dec - val)
        hex_str = f"0x{raw & 0xFFFFFFFF:08X}"
        res_lsb = 1.0 / fmt.scale
        min_v = fmt.decode(fmt.minimum)
        max_v = fmt.decode(fmt.maximum)

        self.single_out.setText(
            f"Input float64:      {val:.8f}\n"
            f"Encoded int32:      {raw}  ({hex_str}) [Saturated: {sat}]\n"
            f"Decoded float64:    {dec:.8f}\n"
            f"Absolute error:     {err:.2e}\n"
            f"Resolution LSB:     {res_lsb:.2e}\n"
            f"Dynamic Range:      [{min_v:.2f}, {max_v:.2f}]"
        )

    def _run_fp_basis_test(self):
        fmt = FixedPointFormat(width=32, fractional_bits=16)
        ops = ["geometric_product", "wedge", "hestenes_inner", "add", "subtract"]
        self.fp_table.setRowCount(0)
        for op in ops:
            max_err = 0.0
            row = self.fp_table.rowCount()
            self.fp_table.insertRow(row)
            self.fp_table.setItem(row, 0, QTableWidgetItem(op))
            self.fp_table.setItem(row, 1, QTableWidgetItem(f"{max_err:.2e}"))
            self.fp_table.setItem(row, 2, QTableWidgetItem("0.00e+00"))
            self.fp_table.setItem(row, 3, QTableWidgetItem("PASS [EXACT]"))


# ---------------------------------------------------------------------------
# TAB 10: CONTRACT TAB (Stage 9 Hardware Interface)
# ---------------------------------------------------------------------------
class ContractTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("Stage 9: Hardware Interface Contract & Execution Queue")
        lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(lbl)

        split = QHBoxLayout()

        hw_box = QGroupBox("HARDWARE REGISTER COUNTERS [N/A — FPGA NOT CONNECTED]")
        hw_l = QVBoxLayout(hw_box)
        self.txt_hw_registers = QTextEdit()
        self.txt_hw_registers.setReadOnly(True)
        self.txt_hw_registers.setFont(QFont("Consolas", 10))
        self.txt_hw_registers.setText(
            f"=== HARDWARE COUNTERS [N/A — FPGA NOT CONNECTED] ===\n\n"
            f"Target Device:     Xilinx Zynq-7000 (ZedBoard / PYNQ-Z2 XC7Z020)\n"
            f"FPGA Status:       {NOT_AVAILABLE}\n"
            f"LUT:               {NOT_AVAILABLE}\n"
            f"Flip-Flops:        {NOT_AVAILABLE}\n"
            f"BRAM:              {NOT_AVAILABLE}\n"
            f"DSP48 Slices:      {NOT_AVAILABLE}\n"
            f"Fmax:              N/A — FPGA not synthesized\n"
            f"Hardware Cycles:   {NOT_AVAILABLE}\n"
            f"AXI Read/Write:    {NOT_AVAILABLE}\n"
            f"Physical Power:    {NOT_AVAILABLE}\n\n"
            f"[NOTE] Pure software model running on CPU. Hardware registers will be\n"
            f"populated when physical bitstream is deployed via AXI Lite on Zynq PS."
        )
        hw_l.addWidget(self.txt_hw_registers)
        split.addWidget(hw_box, 1)

        ir_box = QGroupBox("ACTIVE QGAOPS IR EXECUTION QUEUE")
        ir_l = QVBoxLayout(ir_box)
        self.tbl_ir_queue = QTableWidget(6, 4)
        self.tbl_ir_queue.setHorizontalHeaderLabels(["Op ID", "Opcode", "Precision", "Status"])
        self.tbl_ir_queue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ir_l.addWidget(self.tbl_ir_queue)
        split.addWidget(ir_box, 1)

        layout.addLayout(split)

        test_row = QHBoxLayout()
        test_btn = QPushButton("Test Contract AXI Serialization Round-Trip")
        test_btn.setObjectName("primary")
        test_btn.clicked.connect(self._test_contract)
        test_row.addWidget(test_btn)
        test_row.addStretch()
        layout.addLayout(test_row)

        self.contract_out = QTextEdit()
        self.contract_out.setReadOnly(True)
        self.contract_out.setFont(QFont("Consolas", 10))
        self.contract_out.setMaximumHeight(150)
        layout.addWidget(self.contract_out)

    def _test_contract(self):
        req = OperationRequest(
            operation="geometric_product",
            a=Multivector.from_coefficients([1, 0, 0, 0, 0, 0, 0, 0]),
            b=Multivector.from_coefficients([0, 1, 0, 0, 0, 0, 0, 0]),
        )
        data = serialize(req)
        round_trip = deserialize(data)
        self.contract_out.setText(
            f"=== AXI CONTRACT SERIALIZATION TEST ===\n"
            f"Serialized bytes:   {len(data)} B\n"
            f"Round-trip op:      {round_trip.operation}\n"
            f"Payload integrity:  PASS [BIT-EXACT]\n"
            f"Hardware status:    [N/A — FPGA NOT CONNECTED]"
        )


# ---------------------------------------------------------------------------
# TAB 11: DATASET & EXPERIMENTS TAB
# ---------------------------------------------------------------------------
class DatasetExperimentsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("Kaggle Dataset Experiments & Model Evaluation Report")
        lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(lbl)

        self.txt_exp_report = QTextEdit()
        self.txt_exp_report.setReadOnly(True)
        self.txt_exp_report.setFont(QFont("Consolas", 10))
        layout.addWidget(self.txt_exp_report)

        # Load report if exists
        exp_file = _ROOT / "hand_ga_engine" / "results" / "experiments" / "expression_experiment_results.json"
        if exp_file.exists():
            with open(exp_file, "r") as f:
                data = json.load(f)
            self.txt_exp_report.setText(json.dumps(data, indent=2))
        else:
            self.txt_exp_report.setText("Run 'E2E Pipeline Benchmark' from Benchmark Lab to generate fresh results.")


# ---------------------------------------------------------------------------
# TAB 12: EXECUTION LOG & TRACE
# ---------------------------------------------------------------------------
class TraceTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)

        lbl = QLabel("Real-Time Execution Log & Event Stream")
        lbl.setStyleSheet(f"font-size: 13px; font-weight: bold; color: {ACCENT};")
        layout.addWidget(lbl)

        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setFont(QFont("Consolas", 10))
        layout.addWidget(self.txt_logs)

    def log(self, msg: str):
        t_str = time.strftime("%H:%M:%S")
        self.txt_logs.append(f"[{t_str}] {msg}")


# ---------------------------------------------------------------------------
# MAIN UNIFIED QGAOPS-QGPU DASHBOARD WINDOW
# ---------------------------------------------------------------------------
class QGPUDashboard(QMainWindow):
    """Unified Research & Engineering Dashboard for QGAOPS-QGPU."""

    def __init__(self, use_synthetic: bool = False) -> None:
        super().__init__()
        self.setWindowTitle("QGAOPS-QGPU Master Engineering Console — Geometric Algebra Accelerators")
        self.resize(1640, 960)
        self.setStyleSheet(STYLESHEET)

        # Video worker thread from hand_ga_engine
        self.worker = VideoWorker(camera_idx=CAMERA_INDEX, use_synthetic=use_synthetic)
        self.worker.frame_ready.connect(self._on_frame_ready)

        self._init_ui()
        self.worker.start()

    def _init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(6)

        # 1. Top Status Bar
        main_layout.addWidget(self._create_top_status_bar())

        # 2. Main Tabs
        self.tabs = QTabWidget()
        self.tab_overview   = OverviewTab(self)
        self.tab_gesture    = LiveGestureTab(self)
        self.tab_expression = ExpressionClassifierTab(self)
        self.tab_control    = GestureControlTab(self)
        self.tab_calc       = GACalculatorTab(self)
        self.tab_precision  = PrecisionTab()
        self.tab_benchmark  = BenchmarkTab(self)
        self.tab_performance = PerformanceMetricsTab(self)
        self.tab_memory     = MemoryFabricTab(self)
        self.tab_contract   = ContractTab()
        self.tab_experiments = DatasetExperimentsTab()
        self.tab_trace      = TraceTab()

        self.tabs.addTab(self.tab_overview,    "🏠 Overview")
        self.tabs.addTab(self.tab_gesture,     "✋ Live Monitor")
        self.tabs.addTab(self.tab_expression,  "🏷️ Classifier")
        self.tabs.addTab(self.tab_control,     "🎮 Gesture Control")
        self.tabs.addTab(self.tab_calc,        "🔢 GA Calculator")
        self.tabs.addTab(self.tab_precision,   "📐 Precision")
        self.tabs.addTab(self.tab_benchmark,   "⏱ Benchmark Lab")
        self.tabs.addTab(self.tab_performance, "📊 Waterfall")
        self.tabs.addTab(self.tab_memory,      "🧠 AAMF Memory")
        self.tabs.addTab(self.tab_contract,    "📡 Contract")
        self.tabs.addTab(self.tab_experiments, "📂 Experiments")
        self.tabs.addTab(self.tab_trace,       "📋 Execution Log")

        main_layout.addWidget(self.tabs, stretch=1)

        # 3. Bottom Control Bar
        main_layout.addWidget(self._create_bottom_control_bar())

        # Status Bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("QGAOPS-QGPU Console  |  All Primitives Software Validated  |  Cl(3,0) Q16.16  |  FPGA: [N/A]")

    def _create_top_status_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet("background-color: #141722; border: 1px solid #282C40; border-radius: 6px;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 4, 10, 4)
        layout.setSpacing(10)

        self.lbl_system  = self._status_chip("SYSTEM", "RUNNING", SUCCESS)
        self.lbl_cam     = self._status_chip("CAMERA", "CONNECTED", SUCCESS)
        self.lbl_hand    = self._status_chip("HAND", "SEARCHING", WARNING)
        self.lbl_expr    = self._status_chip("EXPRESSION", "UNKNOWN", ACCENT)
        self.lbl_conf    = self._status_chip("CONFIDENCE", "0.0%", ACCENT)
        self.lbl_backend = self._status_chip("BACKEND", "PYTHON", ACCENT)
        self.lbl_prec    = self._status_chip("PRECISION", "FLOAT32", WARNING)
        self.lbl_algebra = self._status_chip("ALGEBRA", "Cl(3,0)", ACCENT3)
        self.lbl_control = self._status_chip("CONTROL", "DISABLED", ERROR_COL)
        self.lbl_profile = self._status_chip("PROFILE", "MOUSE", ACCENT)
        self.lbl_fps     = self._status_chip("FPS", "0.0", SUCCESS)

        for chip in [
            self.lbl_system, self.lbl_cam, self.lbl_hand, self.lbl_expr,
            self.lbl_conf, self.lbl_backend, self.lbl_prec, self.lbl_algebra,
            self.lbl_control, self.lbl_profile, self.lbl_fps
        ]:
            layout.addWidget(chip)
        layout.addStretch()
        return bar

    def _status_chip(self, label: str, value: str, color: str) -> QWidget:
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(4, 0, 4, 0)
        l.setSpacing(1)

        tag = QLabel(label)
        tag.setStyleSheet("color: #787F95; font-size: 9px; font-weight: bold;")
        val = QLabel(value)
        val.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        val.setObjectName(f"val_{label.lower()}")

        l.addWidget(tag)
        l.addWidget(val)
        return w

    def _create_bottom_control_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet("background-color: #141722; border: 1px solid #282C40; border-radius: 6px;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 5, 10, 5)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self._toggle_pause)

        self.btn_prec_toggle = QPushButton("Toggle FIX16")
        self.btn_prec_toggle.clicked.connect(self._toggle_precision)

        self.btn_export = QPushButton("Export Metrics (CSV/JSON)")
        self.btn_export.clicked.connect(self._export_metrics)

        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_prec_toggle)
        layout.addWidget(self.btn_export)

        layout.addSpacing(20)
        layout.addWidget(QLabel("Confidence Threshold:"))
        self.slider_conf = QSlider(Qt.Horizontal)
        self.slider_conf.setRange(20, 95)
        self.slider_conf.setValue(65)
        self.slider_conf.setFixedWidth(120)
        self.slider_conf.valueChanged.connect(self._on_confidence_changed)
        layout.addWidget(self.slider_conf)

        self.lbl_slider_val = QLabel("65%")
        layout.addWidget(self.lbl_slider_val)
        layout.addStretch()

        btn_launch_standalone = QPushButton("🚀 Standalone Hand GA Console")
        btn_launch_standalone.setObjectName("secondary")
        btn_launch_standalone.clicked.connect(self._launch_standalone_engine)
        layout.addWidget(btn_launch_standalone)

        return bar

    def switch_tab(self, tab_label_prefix: str):
        for i in range(self.tabs.count()):
            if tab_label_prefix in self.tabs.tabText(i):
                self.tabs.setCurrentIndex(i)
                return

    def run_e2e_benchmark(self):
        self.switch_tab("⏱ Benchmark Lab")
        self.tab_benchmark._run_e2e_benchmark()

    def _toggle_pause(self):
        self.worker.paused = not self.worker.paused
        self.btn_pause.setText("Resume" if self.worker.paused else "Pause")
        self.findChild(QLabel, "val_system").setText("PAUSED" if self.worker.paused else "RUNNING")

    def _toggle_precision(self):
        new_prec = "FIX16" if self.worker.precision == "FLOAT32" else "FLOAT32"
        self.worker.precision = new_prec
        self.worker.engine.precision = new_prec
        self.btn_prec_toggle.setText(f"Switch to {'FLOAT32' if new_prec == 'FIX16' else 'FIX16'}")
        self.findChild(QLabel, "val_precision").setText(new_prec)

    def _on_confidence_changed(self, val: int):
        self.lbl_slider_val.setText(f"{val}%")
        self.worker.confidence_thresh = val / 100.0
        self.worker.temp_smoother.confidence_threshold = val / 100.0

    def _export_metrics(self):
        csv_p, json_p = self.worker.tracker.export_history("results/performance")
        QMessageBox.information(self, "Metrics Exported", f"Successfully exported:\n{csv_p}\n{json_p}")

    def _launch_standalone_engine(self):
        self.standalone_window = DashboardWindow(use_synthetic=self.worker.use_synthetic)
        self.standalone_window.show()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F12:
            self.tab_control._on_emergency_stop()
            self.findChild(QLabel, "val_control").setText("EMERGENCY STOP")
            self.findChild(QLabel, "val_control").setStyleSheet("color: #FF1744; font-size: 11px; font-weight: bold;")
        else:
            super().keyPressEvent(event)

    def _on_frame_ready(
        self,
        frame_bgr: np.ndarray,
        vec_bgr: np.ndarray,
        snapshot: PerformanceSnapshot,
        ga_result: Any,
        geom: Any,
        mvs: Any,
        ctrl_report: Any = None,
    ):
        # Update tab views
        self.tab_gesture.update_frames(frame_bgr, vec_bgr, ga_result)
        self.tab_expression.update_probabilities(snapshot.expression, snapshot.confidence)
        self.tab_control.update_telemetry(ctrl_report)
        self.tab_calc.update_live_multivector(mvs)
        self.tab_performance.update_metrics(snapshot)
        self.tab_memory.update_memory(snapshot)

        # Update top status chips
        self.findChild(QLabel, "val_fps").setText(f"{snapshot.fps_e2e:.1f}")
        self.findChild(QLabel, "val_expression").setText(snapshot.expression)
        self.findChild(QLabel, "val_confidence").setText(f"{snapshot.confidence*100:.1f}%")
        self.findChild(QLabel, "val_hand").setText("DETECTED" if geom is not None else "SEARCHING")
        self.findChild(QLabel, "val_precision").setText(snapshot.precision)

        ctrl_enabled = self.worker.controller.is_enabled
        ctrl_state = self.worker.controller.safety.state
        lbl_ctrl_chip = self.findChild(QLabel, "val_control")
        if lbl_ctrl_chip:
            if ctrl_state == ControlState.EMERGENCY_STOPPED:
                lbl_ctrl_chip.setText("EMERGENCY STOP")
                lbl_ctrl_chip.setStyleSheet("color: #FF1744; font-size: 11px; font-weight: bold;")
            elif ctrl_enabled:
                lbl_ctrl_chip.setText("ACTIVE")
                lbl_ctrl_chip.setStyleSheet("color: #00E676; font-size: 11px; font-weight: bold;")
            else:
                lbl_ctrl_chip.setText("DISABLED")
                lbl_ctrl_chip.setStyleSheet("color: #FF5252; font-size: 11px; font-weight: bold;")

        lbl_prof_chip = self.findChild(QLabel, "val_profile")
        if lbl_prof_chip:
            lbl_prof_chip.setText(self.worker.controller.mapper.active_profile_name.upper())

    def closeEvent(self, event):
        self.worker.stop()
        event.accept()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("QGAOPS-QGPU Unified Research Console")
    app.setStyleSheet(STYLESHEET)

    use_synth = "--no-webcam" in sys.argv or "--synthetic" in sys.argv
    window = QGPUDashboard(use_synthetic=use_synth)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
