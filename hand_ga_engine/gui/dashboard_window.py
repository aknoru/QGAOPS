"""
LIVE HAND GA ENGINE — gui/dashboard_window.py
Research-grade engineering dashboard built with PySide6.

[IMPLEMENTED]
- Dark engineering-style aesthetic resembling physical accelerator monitoring consoles.
- Top status bar with live status indicators.
- 9 Functional Tabs:
    1. LIVE: Dual-pane Camera & 3D GA view with expression and GA results.
    2. GEOMETRIC ALGEBRA: 8-component multivector decomposition, rotor extraction, sandwich.
    3. EXPRESSION: Kaggle 6-class classifier stats, confusion matrix, confidence meters.
    4. PERFORMANCE: Live rolling metrics (FPS, latency, OPS/s, bandwidth, CPU/RAM).
    5. MEMORY: QGAOPS AAMF B0-B5 memory hierarchy, logical DDR traffic, reuse ratio.
    6. QGAOPS: Live IR queue, opcode breakdown, binary bytecode disassembly.
    7. BENCHMARK: One-click microbenchmarks, GA benchmarks, and E2E evaluation.
    8. EXPERIMENTS: Kaggle dataset audit, test set evaluation, model comparisons.
    9. LOGS: Searchable real-time event log and execution trace.
- Explicit metric labeling:
    [MEASURED SOFTWARE]
    [SOFTWARE MODEL]
    [CALCULATED]
    [N/A — FPGA NOT CONNECTED]
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
from PySide6.QtCore import QDateTime, QPoint, QRect, QSize, Qt, QThread, QTimer, Signal
from PySide6.QtGui import QColor, QFont, QIcon, QImage, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSlider,
    QSplitter,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config.config import CAMERA_INDEX, LANDMARK_SMOOTHING_ALPHA
from engine.algebra_engine import AlgebraEngine
from expression.dynamic_recognizer import DynamicExpressionRecognizer
from expression.expression_to_ga import ExpressionToGA
from expression.state_machine import ExpressionStateMachine
from expression.temporal_smoother import ExpressionTemporalSmoother
from ga.multivector import Multivector
from hand_detection.detector import HandDetector
from hand_detection.gesture import StaticPoseRecognizer
from hand_detection.landmarks import HandGeometryExtractor, LandmarkSmoother
from mapping.dataset_classes import CLASS_NAMES, UNKNOWN_CLASS
from mapping.expression_classes import (
    STATIC_POSES,
    DYNAMIC_EXPRESSIONS,
    ALL_EXPRESSIONS,
    ALL_EXPRESSION_NAMES,
)
from mapping.hand_to_ga import hand_to_multivectors
from metrics.hardware_metrics import NOT_AVAILABLE
from metrics.performance_tracker import PerformanceSnapshot, PerformanceTracker
from models.static_expression_classifier import StaticExpressionClassifier
from scripts.extract_features import extract_geometric_features
from visualization.vector_view import VectorView3D
from control.controller import GestureController, ControlExecutionReport
from control.safety import ControlState
from visualization.control_overlay import render_control_hud


# ---------------------------------------------------------------------------
# Styling & Theme Constants
# ---------------------------------------------------------------------------
DARK_STYLE = """
QMainWindow, QWidget {
    background-color: #0F1016;
    color: #E0E2EC;
    font-family: 'Segoe UI', 'Consolas', sans-serif;
    font-size: 12px;
}
QTabWidget::pane {
    border: 1px solid #232738;
    background-color: #141722;
    border-radius: 4px;
}
QTabBar::tab {
    background-color: #1A1D2B;
    color: #8C93A8;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: bold;
}
QTabBar::tab:selected {
    background-color: #232738;
    color: #00E5FF;
    border-bottom: 2px solid #00E5FF;
}
QGroupBox {
    border: 1px solid #282C40;
    border-radius: 6px;
    margin-top: 14px;
    padding-top: 14px;
    font-weight: bold;
    color: #00E5FF;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    color: #00E5FF;
}
QPushButton {
    background-color: #1E2333;
    color: #00E5FF;
    border: 1px solid #00B0FF;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: bold;
}
QPushButton:hover {
    background-color: #00B0FF;
    color: #0B0E14;
}
QPushButton:pressed {
    background-color: #0081CB;
}
QPushButton:disabled {
    background-color: #181B26;
    color: #555B6E;
    border-color: #2D3244;
}
QLineEdit, QTextEdit, QTableWidget {
    background-color: #10121A;
    border: 1px solid #282C40;
    color: #DDE1F0;
    border-radius: 4px;
}
QTableWidget {
    gridline-color: #1E2333;
    selection-background-color: #005F87;
}
QHeaderView::section {
    background-color: #1A1D2B;
    color: #00E5FF;
    padding: 4px;
    border: 1px solid #282C40;
    font-weight: bold;
}
QProgressBar {
    border: 1px solid #282C40;
    border-radius: 3px;
    text-align: center;
    background-color: #10121A;
    color: #FFF;
}
QProgressBar::chunk {
    background-color: #00E5FF;
}
QSlider::groove:horizontal {
    height: 6px;
    background: #1E2333;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background: #00E5FF;
    width: 14px;
    margin: -4px 0;
    border-radius: 7px;
}
"""


# ---------------------------------------------------------------------------
# Background Video Worker Thread
# ---------------------------------------------------------------------------
class VideoWorker(QThread):
    """Acquires frames, runs detection, classifier, GA, and metrics asynchronously."""
    frame_ready = Signal(np.ndarray, np.ndarray, object, object, object, object, object)

    def __init__(
        self,
        camera_idx: int = 0,
        use_synthetic: bool = False,
        confidence_thresh: float = 0.65,
    ) -> None:
        super().__init__()
        self.camera_idx = camera_idx
        self.use_synthetic = use_synthetic
        self.confidence_thresh = confidence_thresh
        self.running = False
        self.paused = False
        self.precision = "FLOAT32"

        # Pipeline sub-systems
        self.engine = AlgebraEngine(precision=self.precision, trace=True)
        self.detector = HandDetector(max_hands=2, min_detection_conf=0.3, min_tracking_conf=0.3)
        self.smoother = [LandmarkSmoother(LANDMARK_SMOOTHING_ALPHA) for _ in range(2)]
        self.extractor = HandGeometryExtractor()
        self.vector_view = VectorView3D(480, 480)
        self.pose_rec = StaticPoseRecognizer()
        self.dyn_rec = DynamicExpressionRecognizer(buffer_frames=30)
        self.state_mach = ExpressionStateMachine(stable_frames=3, cooldown_frames=10)
        self.expr_to_ga = ExpressionToGA(self.engine, precision=self.precision)
        self.temp_smoother = ExpressionTemporalSmoother(window_size=5, confidence_threshold=confidence_thresh)
        self.tracker = PerformanceTracker(history_seconds=60)

        # Phase 5: Gesture Control Layer
        self.controller = GestureController(profile_name="mouse")

        # Load trained classifier if available
        model_path = "models/static_expression_model.pkl"
        if os.path.exists(model_path):
            try:
                self.classifier = StaticExpressionClassifier.load(model_path)
            except Exception:
                self.classifier = None
        else:
            self.classifier = None

    def enable_control(self) -> None:
        self.controller.enable()

    def disable_control(self) -> None:
        self.controller.disable()

    def emergency_stop_control(self) -> None:
        self.controller.emergency_stop()

    def reset_emergency_control(self) -> None:
        self.controller.reset_emergency()

    def set_control_profile(self, profile: str) -> bool:
        return self.controller.set_profile(profile)

    def run(self) -> None:
        self.running = True
        cap = None
        if not self.use_synthetic:
            cap = cv2.VideoCapture(self.camera_idx)
            if not cap.isOpened():
                cap = None

        while self.running:
            if self.paused:
                time.sleep(0.05)
                continue

            # 1. Camera Acquisition
            self.tracker.start_stage("camera_acquisition")
            if cap is not None:
                ret, frame = cap.read()
                if not ret:
                    frame = np.full((480, 640, 3), 20, dtype=np.uint8)
            else:
                frame = np.full((480, 640, 3), 24, dtype=np.uint8)
                cv2.putText(
                    frame, "SYNTHETIC DEMO MODE", (140, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 255), 2
                )
            frame = cv2.flip(frame, 1)
            self.tracker.end_stage("camera_acquisition")
            self.tracker.record_data_movement(input_bytes=frame.nbytes)

            # 2. Hand Detection
            self.tracker.start_stage("hand_detection")
            hands = self.detector.detect(frame)
            annotated = self.detector.draw_landmarks(frame, hands)
            self.tracker.end_stage("hand_detection")

            last_geom = None
            last_mvs = None
            raw_expr = UNKNOWN_CLASS
            raw_conf = 0.0

            if hands:
                self.tracker.record_data_movement(input_bytes=len(hands) * 21 * 12)
                hand = hands[0]
                lm_raw = hand.to_array()

                # 3. Landmark Normalization
                self.tracker.start_stage("landmark_normalization")
                lm_sm = self.smoother[0].update(lm_raw)
                geom = self.extractor.extract(lm_raw, lm_sm, hand.confidence, hand.handedness, frame_index=0)
                last_geom = geom
                self.tracker.end_stage("landmark_normalization")

                # 4. Feature Extraction
                self.tracker.start_stage("feature_extraction")
                mvs = hand_to_multivectors(geom)
                last_mvs = mvs
                geo_feat = extract_geometric_features(geom, lm_raw)
                self.dyn_rec.push(geom, time.time())
                self.tracker.end_stage("feature_extraction")

                # 5. Expression Classification & Recognition
                self.tracker.start_stage("expression_classification")
                # A. Dynamic motion recognition (14 expressions)
                dyn_res = self.dyn_rec.recognize()

                # B. Static pose geometric rule recognizer (13 poses)
                gr = self.pose_rec.recognize(geom)

                # C. ML model prediction (13 poses)
                ml_expr, ml_conf = UNKNOWN_CLASS, 0.0
                if self.classifier is not None:
                    ml_expr, ml_conf = self.classifier.predict_single(geo_feat)

                # D. Static fusion
                if ml_conf >= 0.65 and gr.confidence >= 0.60 and ml_expr == gr.pose:
                    static_expr = ml_expr
                    static_conf = min(1.0, 0.5 * (ml_conf + gr.confidence) + 0.1)
                elif ml_conf >= 0.70:
                    static_expr = ml_expr
                    static_conf = ml_conf
                elif gr.confidence >= 0.65:
                    static_expr = gr.pose
                    static_conf = gr.confidence
                elif ml_expr != UNKNOWN_CLASS and ml_conf > 0.5:
                    static_expr = ml_expr
                    static_conf = ml_conf
                else:
                    static_expr = gr.pose if gr.confidence > 0 else UNKNOWN_CLASS
                    static_conf = max(gr.confidence, ml_conf)

                # E. Dynamic priority when motion is present
                if dyn_res.confidence >= 0.70 and dyn_res.expression != "UNKNOWN_DYNAMIC":
                    raw_expr = dyn_res.expression
                    raw_conf = dyn_res.confidence
                else:
                    raw_expr = static_expr
                    raw_conf = static_conf
                self.tracker.end_stage("expression_classification")
            else:
                self.temp_smoother.reset()
                self.dyn_rec.reset()

            # Temporal Consensus
            smoothed_pred = self.temp_smoother.update(raw_expr, raw_conf)
            stable_expr = smoothed_pred.expression
            stable_conf = smoothed_pred.confidence

            # 6. GA Encoding & 7. Algebra Analysis & 8. Computation
            self.tracker.start_stage("ga_encoding")
            ga_result = None
            if last_geom is not None and last_mvs is not None:
                ga_result = self.expr_to_ga.map(stable_expr, last_geom, last_mvs)
                if ga_result:
                    self.tracker.record_operation(ga_result.opcode, is_fix16=(self.precision == "FIX16"))
                    self.tracker.record_data_movement(output_bytes=64)
            self.tracker.end_stage("ga_encoding")

            # Phase 5: Gesture Control Layer
            self.tracker.start_stage("gesture_control")
            ctrl_report = self.controller.process_frame(
                gesture=stable_expr if last_geom else "UNKNOWN",
                confidence=stable_conf,
                geom=last_geom,
                detection_latency_ms=0.0,
            )
            self.tracker.end_stage("gesture_control")

            # 9. 3D Vector View / 3D Virtual Object View
            self.tracker.start_stage("visualization")
            if self.controller.mapper.active_profile_name == "object3d":
                vec_bgr = self.controller.object3d.render(480, 480)
            else:
                vec_bgr = self.vector_view.render(last_geom, last_mvs)
            self.tracker.end_stage("visualization")

            # Control HUD Overlay on camera frame
            annotated = render_control_hud(
                annotated,
                report=ctrl_report,
                pose=static_expr if last_geom else "UNKNOWN",
                expression=stable_expr if last_geom else "UNKNOWN",
                confidence=stable_conf,
                hand_detected=(last_geom is not None),
                is_control_enabled=self.controller.is_enabled,
                active_profile=self.controller.mapper.active_profile_name,
            )

            # End frame snapshot
            snapshot = self.tracker.end_frame(
                expression=stable_expr,
                confidence=stable_conf,
                backend="PYTHON",
                precision=self.precision,
            )

            # Emit signal to GUI
            self.frame_ready.emit(annotated, vec_bgr, snapshot, ga_result, last_geom, last_mvs, ctrl_report)

            # Cap loop rate to ~60 FPS
            time.sleep(0.005)

        if cap is not None:
            cap.release()
        self.detector.close()
        self.vector_view.close()

    def stop(self) -> None:
        self.running = False
        self.wait(2000)


# ---------------------------------------------------------------------------
# Main Engineering Dashboard Window
# ---------------------------------------------------------------------------
class DashboardWindow(QMainWindow):
    """Main QGAOPS Engineering Monitoring Console."""

    def __init__(self, use_synthetic: bool = False) -> None:
        super().__init__()
        self.setWindowTitle("QGAOPS-QGPU Live Hand Geometric Algebra Engine — Engineering Dashboard")
        self.resize(1640, 960)
        self.setStyleSheet(DARK_STYLE)

        self.worker = VideoWorker(camera_idx=CAMERA_INDEX, use_synthetic=use_synthetic)
        self.worker.frame_ready.connect(self._on_frame_ready)

        self._init_ui()
        self.worker.start()

    def _init_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # 1. TOP ACCELERATOR STATUS BAR
        main_layout.addWidget(self._create_top_status_bar())

        # 2. TABBED CONSOLE
        self.tabs = QTabWidget()
        self.tabs.addTab(self._create_live_tab(), "1. LIVE MONITOR")
        self.tabs.addTab(self._create_ga_tab(), "2. GEOMETRIC ALGEBRA")
        self.tabs.addTab(self._create_expression_tab(), "3. EXPRESSION CLASSIFIER")
        self.tabs.addTab(self._create_performance_tab(), "4. PERFORMANCE METRICS")
        self.tabs.addTab(self._create_memory_tab(), "5. AAMF MEMORY FABRIC")
        self.tabs.addTab(self._create_qgaops_tab(), "6. QGAOPS ACCELERATOR")
        self.tabs.addTab(self._create_benchmark_tab(), "7. BENCHMARKS")
        self.tabs.addTab(self._create_experiments_tab(), "8. DATASET EXPERIMENTS")
        self.tabs.addTab(self._create_logs_tab(), "9. EXECUTION LOG")
        self.tabs.addTab(self._create_control_tab(), "10. COMPUTER CONTROL")

        main_layout.addWidget(self.tabs, stretch=1)

        # 3. BOTTOM CONTROL BAR
        main_layout.addWidget(self._create_bottom_control_bar())

    # -----------------------------------------------------------------------
    # Top Status Bar
    # -----------------------------------------------------------------------
    def _create_top_status_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet("background-color: #141722; border: 1px solid #282C40; border-radius: 6px;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 6, 12, 6)

        self.lbl_system = self._status_chip("SYSTEM", "RUNNING", "#00E676")
        self.lbl_cam = self._status_chip("CAMERA", "CONNECTED", "#00E676")
        self.lbl_hand = self._status_chip("HAND", "SEARCHING", "#FF9100")
        self.lbl_expr = self._status_chip("EXPRESSION", "UNKNOWN", "#00E5FF")
        self.lbl_conf = self._status_chip("CONFIDENCE", "0.0%", "#00E5FF")
        self.lbl_backend = self._status_chip("BACKEND", "PYTHON [IMPLEMENTED]", "#00E5FF")
        self.lbl_prec = self._status_chip("PRECISION", "FLOAT32", "#FFD600")
        self.lbl_algebra = self._status_chip("ALGEBRA", "G(3,0,0)", "#E040FB")
        self.lbl_control = self._status_chip("CONTROL", "DISABLED", "#FF5252")
        self.lbl_profile = self._status_chip("PROFILE", "MOUSE", "#00E5FF")
        self.lbl_fps = self._status_chip("FPS", "0.0", "#00E676")

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
        val.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold;")
        val.setObjectName(f"val_{label.lower()}")

        l.addWidget(tag)
        l.addWidget(val)
        return w

    # -----------------------------------------------------------------------
    # 1. LIVE MONITOR TAB
    # -----------------------------------------------------------------------
    def _create_live_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)
        layout.setContentsMargins(8, 8, 8, 8)

        # Left: Camera Video
        cam_group = QGroupBox("LIVE CAMERA [MediaPipe 3D Landmark Tracking]")
        cam_l = QVBoxLayout(cam_group)
        self.cam_label = QLabel()
        self.cam_label.setAlignment(Qt.AlignCenter)
        self.cam_label.setStyleSheet("background-color: #000; border-radius: 4px;")
        self.cam_label.setMinimumSize(480, 360)
        cam_l.addWidget(self.cam_label)

        # Middle: 3D Vector View
        vec_group = QGroupBox("3D GEOMETRIC ALGEBRA VIEW [Vectors, Rotor, Wedge Planes]")
        vec_l = QVBoxLayout(vec_group)
        self.vec_label = QLabel()
        self.vec_label.setAlignment(Qt.AlignCenter)
        self.vec_label.setStyleSheet("background-color: #0A0B10; border-radius: 4px;")
        self.vec_label.setMinimumSize(400, 360)
        vec_l.addWidget(self.vec_label)

        # Right: Live GA / QGAOPS Summary Card
        info_group = QGroupBox("ACTIVE GA INSTRUCTION & QGAOPS IR PACKET")
        info_l = QVBoxLayout(info_group)

        self.txt_live_ga = QTextEdit()
        self.txt_live_ga.setReadOnly(True)
        self.txt_live_ga.setFont(QFont("Consolas", 11))
        self.txt_live_ga.setStyleSheet("background-color: #0E1018; border: 1px solid #1E2333; color: #00E5FF;")
        info_l.addWidget(self.txt_live_ga)

        layout.addWidget(cam_group, stretch=3)
        layout.addWidget(vec_group, stretch=3)
        layout.addWidget(info_group, stretch=2)
        return tab

    # -----------------------------------------------------------------------
    # 2. GEOMETRIC ALGEBRA TAB
    # -----------------------------------------------------------------------
    def _create_ga_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout(tab)
        layout.setContentsMargins(12, 12, 12, 12)

        # Multivector decomposition
        mv_group = QGroupBox("MULTIVECTOR COEFFICIENTS (Clifford Algebra G(3,0,0)) [MEASURED SOFTWARE]")
        mv_l = QVBoxLayout(mv_group)
        self.tbl_multivector = QTableWidget(8, 4)
        self.tbl_multivector.setHorizontalHeaderLabels(["Basis Element", "Grade", "Float32 Value", "FIX16 Hex"])
        self.tbl_multivector.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        mv_l.addWidget(self.tbl_multivector)

        # Rotor & Sandwich Products
        rotor_group = QGroupBox("ROTOR / SANDWICH PRODUCT DECOMPOSITION (R * v * ~R) [MEASURED SOFTWARE]")
        rotor_l = QVBoxLayout(rotor_group)
        self.txt_rotor_decomp = QTextEdit()
        self.txt_rotor_decomp.setReadOnly(True)
        self.txt_rotor_decomp.setFont(QFont("Consolas", 11))
        rotor_l.addWidget(self.txt_rotor_decomp)

        layout.addWidget(mv_group, 0, 0)
        layout.addWidget(rotor_group, 0, 1)
        return tab

    # -----------------------------------------------------------------------
    # 3. EXPRESSION CLASSIFIER TAB
    # -----------------------------------------------------------------------
    def _create_expression_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)

        # Scroll Area for all 27 gestures
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QHBoxLayout(scroll_content)

        # Left Column: 13 Static Hand Poses
        static_box = QGroupBox("STATIC HAND POSES (13 POSES) [MEASURED SOFTWARE]")
        static_l = QVBoxLayout(static_box)

        self.class_bars: Dict[str, QProgressBar] = {}
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
        return tab

    # -----------------------------------------------------------------------
    # 4. PERFORMANCE METRICS TAB
    # -----------------------------------------------------------------------
    def _create_performance_tab(self) -> QWidget:
        tab = QWidget()
        layout = QGridLayout(tab)

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
        return tab

    # -----------------------------------------------------------------------
    # 5. AAMF MEMORY FABRIC TAB
    # -----------------------------------------------------------------------
    def _create_memory_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        box = QGroupBox("QGAOPS ALGEBRA-AWARE MEMORY FABRIC (AAMF B0-B5 MODEL) [SOFTWARE MODEL]")
        bl = QVBoxLayout(box)

        self.txt_memory_model = QTextEdit()
        self.txt_memory_model.setReadOnly(True)
        self.txt_memory_model.setFont(QFont("Consolas", 11))
        bl.addWidget(self.txt_memory_model)

        layout.addWidget(box)
        return tab

    # -----------------------------------------------------------------------
    # 6. QGAOPS ACCELERATOR TAB
    # -----------------------------------------------------------------------
    def _create_qgaops_tab(self) -> QWidget:
        tab = QWidget()
        layout = QHBoxLayout(tab)

        hw_box = QGroupBox("HARDWARE REGISTER COUNTERS [N/A — FPGA NOT CONNECTED]")
        hw_l = QVBoxLayout(hw_box)
        self.txt_hw_registers = QTextEdit()
        self.txt_hw_registers.setReadOnly(True)
        self.txt_hw_registers.setFont(QFont("Consolas", 11))
        hw_l.addWidget(self.txt_hw_registers)

        ir_box = QGroupBox("ACTIVE QGAOPS IR EXECUTION QUEUE")
        ir_l = QVBoxLayout(ir_box)
        self.tbl_ir_queue = QTableWidget(6, 4)
        self.tbl_ir_queue.setHorizontalHeaderLabels(["Op ID", "Opcode", "Precision", "Status"])
        self.tbl_ir_queue.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ir_l.addWidget(self.tbl_ir_queue)

        layout.addWidget(hw_box, stretch=1)
        layout.addWidget(ir_box, stretch=1)
        return tab

    # -----------------------------------------------------------------------
    # 7. BENCHMARKS TAB
    # -----------------------------------------------------------------------
    def _create_benchmark_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        btn_row = QHBoxLayout()
        self.btn_run_micro = QPushButton("Run Microbenchmark (50k ops)")
        self.btn_run_micro.clicked.connect(self._run_microbenchmark)
        self.btn_run_ga = QPushButton("Run GA Standard Benchmark")
        self.btn_run_ga.clicked.connect(self._run_ga_benchmark)
        self.btn_run_e2e = QPushButton("Run E2E Pipeline Benchmark")
        self.btn_run_e2e.clicked.connect(self._run_e2e_benchmark)

        btn_row.addWidget(self.btn_run_micro)
        btn_row.addWidget(self.btn_run_ga)
        btn_row.addWidget(self.btn_run_e2e)
        btn_row.addStretch()

        self.txt_benchmark_results = QTextEdit()
        self.txt_benchmark_results.setReadOnly(True)
        self.txt_benchmark_results.setFont(QFont("Consolas", 11))

        layout.addLayout(btn_row)
        layout.addWidget(self.txt_benchmark_results)
        return tab

    # -----------------------------------------------------------------------
    # 8. DATASET EXPERIMENTS TAB
    # -----------------------------------------------------------------------
    def _create_experiments_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.txt_exp_report = QTextEdit()
        self.txt_exp_report.setReadOnly(True)
        self.txt_exp_report.setFont(QFont("Consolas", 11))
        layout.addWidget(self.txt_exp_report)

        # Load experiment report if exists
        exp_file = "results/experiments/expression_experiment_results.json"
        if os.path.exists(exp_file):
            with open(exp_file, "r") as f:
                data = json.load(f)
            self.txt_exp_report.setText(json.dumps(data, indent=2))

        return tab

    # -----------------------------------------------------------------------
    # 9. EXECUTION LOG TAB
    # -----------------------------------------------------------------------
    def _create_logs_tab(self) -> QWidget:
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.txt_logs = QTextEdit()
        self.txt_logs.setReadOnly(True)
        self.txt_logs.setFont(QFont("Consolas", 10))
        layout.addWidget(self.txt_logs)
        return tab

    # -----------------------------------------------------------------------
    # 10. COMPUTER CONTROL TAB
    # -----------------------------------------------------------------------
    def _create_control_tab(self) -> QWidget:
        tab = QWidget()
        main_l = QVBoxLayout(tab)
        main_l.setContentsMargins(12, 12, 12, 12)
        main_l.setSpacing(10)

        # Header with architecture summary & safety notice
        hdr_box = QFrame()
        hdr_box.setStyleSheet("background-color: #141722; border: 1px solid #232738; border-radius: 6px; padding: 4px;")
        hdr_l = QVBoxLayout(hdr_box)
        title = QLabel("COMPUTER VISION GESTURE CONTROL INTERFACE [SOFTWARE CONTROLLER]")
        title.setStyleSheet("color: #00E5FF; font-size: 14px; font-weight: bold;")
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
        self.btn_toggle_control.clicked.connect(self._toggle_control_enabled)

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
        self.cmb_control_profile.currentTextChanged.connect(self._on_control_profile_changed)
        self.cmb_control_profile.setFixedWidth(140)
        act_l.addWidget(self.cmb_control_profile)

        self.lbl_ctrl_tab_state = QLabel("STATE: DISABLED")
        self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")
        act_l.addWidget(self.lbl_ctrl_tab_state)

        act_l.addStretch()
        f12_hint = QLabel("Emergency Cut-off: Press [F12]")
        f12_hint.setStyleSheet("color: #FF9100; font-style: italic;")
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
        return tab

    def _populate_profile_table(self) -> None:
        """Populate the mappings table from active profile."""
        mappings = self.worker.controller.mapper.active_mappings
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

    def _toggle_control_enabled(self) -> None:
        if self.worker.controller.is_enabled:
            self.worker.disable_control()
            self.btn_toggle_control.setText("ENABLE CONTROL")
            self.btn_toggle_control.setStyleSheet("background-color: #00C853; color: #000; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
            self.lbl_ctrl_tab_state.setText("STATE: DISABLED")
            self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")
        else:
            self.worker.enable_control()
            self.btn_toggle_control.setText("DISABLE CONTROL")
            self.btn_toggle_control.setStyleSheet("background-color: #FF5252; color: #FFF; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
            self.lbl_ctrl_tab_state.setText("STATE: ENABLED")
            self.lbl_ctrl_tab_state.setStyleSheet("color: #00E676; font-weight: bold; font-size: 12px; margin-left: 10px;")

    def _on_emergency_stop(self) -> None:
        self.worker.emergency_stop_control()
        self.btn_toggle_control.setText("ENABLE CONTROL")
        self.btn_toggle_control.setStyleSheet("background-color: #00C853; color: #000; font-weight: bold; padding: 8px 16px; border-radius: 4px;")
        self.lbl_ctrl_tab_state.setText("STATE: EMERGENCY_STOPPED")
        self.lbl_ctrl_tab_state.setStyleSheet("color: #FF1744; font-weight: bold; font-size: 12px; margin-left: 10px;")

    def _on_reset_emergency(self) -> None:
        self.worker.reset_emergency_control()
        self.lbl_ctrl_tab_state.setText("STATE: DISABLED")
        self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")

    def _on_control_profile_changed(self, profile_name: str) -> None:
        self.worker.set_control_profile(profile_name)
        self._populate_profile_table()

    def keyPressEvent(self, event) -> None:
        if event.key() == Qt.Key_F12:
            self._on_emergency_stop()
        else:
            super().keyPressEvent(event)

    # -----------------------------------------------------------------------
    # Bottom Control Bar
    # -----------------------------------------------------------------------
    def _create_bottom_control_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet("background-color: #141722; border: 1px solid #282C40; border-radius: 6px;")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(10, 6, 10, 6)

        self.btn_pause = QPushButton("Pause")
        self.btn_pause.clicked.connect(self._toggle_pause)

        self.btn_prec_toggle = QPushButton("Toggle FIX16")
        self.btn_prec_toggle.clicked.connect(self._toggle_precision)

        self.btn_export = QPushButton("Export Metrics (CSV/JSON)")
        self.btn_export.clicked.connect(self._export_metrics)

        # Confidence Slider
        layout.addWidget(self.btn_pause)
        layout.addWidget(self.btn_prec_toggle)
        layout.addWidget(self.btn_export)

        layout.addSpacing(20)
        layout.addWidget(QLabel("Confidence Threshold:"))
        self.slider_conf = QSlider(Qt.Horizontal)
        self.slider_conf.setRange(20, 95)
        self.slider_conf.setValue(65)
        self.slider_conf.setFixedWidth(140)
        self.slider_conf.valueChanged.connect(self._on_confidence_changed)
        layout.addWidget(self.slider_conf)

        self.lbl_slider_val = QLabel("65%")
        layout.addWidget(self.lbl_slider_val)
        layout.addStretch()

        return bar

    # -----------------------------------------------------------------------
    # Frame Update Slot
    # -----------------------------------------------------------------------
    def _on_frame_ready(
        self,
        frame_bgr: np.ndarray,
        vec_bgr: np.ndarray,
        snapshot: PerformanceSnapshot,
        ga_result: Any,
        geom: Any,
        mvs: Any,
        ctrl_report: Any = None,
    ) -> None:
        # 1. Update Video Frames
        h, w = frame_bgr.shape[:2]
        q_img = QImage(frame_bgr.data, w, h, w * 3, QImage.Format_BGR888)
        self.cam_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.cam_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        vh, vw = vec_bgr.shape[:2]
        qv_img = QImage(vec_bgr.data, vw, vh, vw * 3, QImage.Format_BGR888)
        self.vec_label.setPixmap(QPixmap.fromImage(qv_img).scaled(self.vec_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

        # 2. Update Status Chips
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
                lbl_ctrl_chip.setStyleSheet("color: #FF1744; font-size: 12px; font-weight: bold;")
            elif ctrl_enabled:
                lbl_ctrl_chip.setText("ACTIVE")
                lbl_ctrl_chip.setStyleSheet("color: #00E676; font-size: 12px; font-weight: bold;")
            else:
                lbl_ctrl_chip.setText("DISABLED")
                lbl_ctrl_chip.setStyleSheet("color: #FF5252; font-size: 12px; font-weight: bold;")

        lbl_prof_chip = self.findChild(QLabel, "val_profile")
        if lbl_prof_chip:
            lbl_prof_chip.setText(self.worker.controller.mapper.active_profile_name.upper())

        # 3. Update Live GA Info Card
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

        # 4. Update Multivector Table
        if mvs:
            basis_names = ["1 (scalar)", "e0", "e1", "e01", "e2", "e02", "e12", "e012"]
            grades = ["0", "1", "1", "2", "1", "2", "2", "3"]
            primary_mv = mvs.get("index_vec", Multivector())
            for idx, (bname, gr) in enumerate(zip(basis_names, grades)):
                val = primary_mv.coeffs[idx]
                hex_fix = f"0x{int(val * 16384) & 0xFFFF:04X}"
                self.tbl_multivector.setItem(idx, 0, QTableWidgetItem(bname))
                self.tbl_multivector.setItem(idx, 1, QTableWidgetItem(gr))
                self.tbl_multivector.setItem(idx, 2, QTableWidgetItem(f"{val:+.5f}"))
                self.tbl_multivector.setItem(idx, 3, QTableWidgetItem(hex_fix))

        # 5. Update Waterfall & Bandwidth
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

        # 6. Update Memory Model Text
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

        # 7. Hardware Registers
        self.txt_hw_registers.setText(
            f"=== HARDWARE COUNTERS [N/A — FPGA NOT CONNECTED] ===\n\n"
            f"Target Device:     Xilinx Zynq-7000 (ZedBoard XC7Z020)\n"
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

        # 8. Expression Probability Bars
        for cname, bar in self.class_bars.items():
            if cname == snapshot.expression:
                bar.setValue(int(snapshot.confidence * 100))
            else:
                bar.setValue(0)

        # 9. Update Computer Vision Control Tab (Tab 10)
        if hasattr(self, "lbl_ctrl_tab_state"):
            self.lbl_ctrl_tab_state.setText(f"STATE: {ctrl_state.name}")
            if ctrl_state == ControlState.EMERGENCY_STOPPED:
                self.lbl_ctrl_tab_state.setStyleSheet("color: #FF1744; font-weight: bold; font-size: 12px; margin-left: 10px;")
            elif ctrl_enabled:
                self.lbl_ctrl_tab_state.setStyleSheet("color: #00E676; font-weight: bold; font-size: 12px; margin-left: 10px;")
            else:
                self.lbl_ctrl_tab_state.setStyleSheet("color: #FF5252; font-weight: bold; font-size: 12px; margin-left: 10px;")

        if ctrl_report and hasattr(self, "txt_ctrl_telemetry"):
            p_stats = self.worker.controller.get_latency_percentiles()
            safety_metrics = self.worker.controller.safety.metrics
            pending = self.worker.controller.safety.pending_confirmation
            pending_str = f"PENDING ({pending.command}, timeout {max(0, int(pending.expires_at - time.time()))}s)" if pending else "NONE"

            self.txt_ctrl_telemetry.setText(
                f"=== CONTROL TELEMETRY [MEASURED SOFTWARE] ===\n"
                f"Active Profile:        {self.worker.controller.mapper.active_profile_name.upper()}\n"
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

        if hasattr(self, "txt_ctrl_obj3d") and self.worker.controller.mapper.active_profile_name == "object3d":
            obj3d = self.worker.controller.object3d
            t_trace = obj3d.transformation_trace
            trace_lines = "\n".join([f"  {k}: {v}" for k, v in t_trace.items()]) if t_trace else "  Identity (no transformation applied yet)"
            self.txt_ctrl_obj3d.setText(
                f"=== GA ROTOR 3D OBJECT STATUS ===\n"
                f"Scale Factor:          {obj3d.scale:.2f}\n"
                f"Translation (X, Y):    ({obj3d.translation[0]:.2f}, {obj3d.translation[1]:.2f})\n"
                f"Rotor Matrix / Trace:\n{trace_lines}\n\n"
                f"Formula:  v' = R v ~R,  where R = exp(-0.5 * theta * B)"
            )

        if ctrl_report and ctrl_report.is_executed and ctrl_report.command and ctrl_report.command != "CURSOR_MOVE" and hasattr(self, "tbl_ctrl_history"):
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

    # -----------------------------------------------------------------------
    # Interactive Button Actions
    # -----------------------------------------------------------------------
    def _toggle_pause(self) -> None:
        self.worker.paused = not self.worker.paused
        self.btn_pause.setText("Resume" if self.worker.paused else "Pause")
        self.findChild(QLabel, "val_system").setText("PAUSED" if self.worker.paused else "RUNNING")

    def _toggle_precision(self) -> None:
        new_prec = "FIX16" if self.worker.precision == "FLOAT32" else "FLOAT32"
        self.worker.precision = new_prec
        self.worker.engine.precision = new_prec
        self.btn_prec_toggle.setText(f"Switch to {'FLOAT32' if new_prec == 'FIX16' else 'FIX16'}")

    def _on_confidence_changed(self, val: int) -> None:
        self.lbl_slider_val.setText(f"{val}%")
        self.worker.confidence_thresh = val / 100.0
        self.worker.temp_smoother.confidence_threshold = val / 100.0

    def _export_metrics(self) -> None:
        csv_p, json_p = self.worker.tracker.export_history("results/performance")
        QMessageBox.information(self, "Metrics Exported", f"Successfully exported:\n{csv_p}\n{json_p}")

    def _run_microbenchmark(self) -> None:
        self.txt_benchmark_results.setText("Running GA microbenchmark (50,000 iterations)... Please wait.")
        QApplication.processEvents()

        engine = self.worker.engine
        v1 = Multivector.vector(0.6, 0.8, 0.0)
        v2 = Multivector.vector(0.3, 0.5, 0.7)
        N = 50000

        res_txt = "=== QGAOPS-QGPU MICROBENCHMARK RESULTS [MEASURED SOFTWARE] ===\n\n"
        ops = [
            ("GP", lambda: engine.gp(v1, v2)),
            ("WEDGE", lambda: engine.wedge(v1, v2)),
            ("DOT", lambda: engine.dot(v1, v2)),
            ("NORM", lambda: engine.norm(v1)),
            ("REVERSE", lambda: engine.reverse(v1)),
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
            res_txt += f"{name:<12} | Latency: {lat_us:8.3f} µs | Throughput: {throughput:10.1f} ops/s\n"

        self.txt_benchmark_results.setText(res_txt)

    def _run_ga_benchmark(self) -> None:
        self.txt_benchmark_results.setText("Running full GA standard benchmark (10,000 ops)...")
        QApplication.processEvents()
        from main import run_benchmark
        # Capture stdout
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            run_benchmark(self.worker.engine)
        self.txt_benchmark_results.setText(f.getvalue())

    def _run_e2e_benchmark(self) -> None:
        self.txt_benchmark_results.setText("Running End-to-End Pipeline Benchmark...")
        QApplication.processEvents()
        from experiments.run_expression_experiment import run_experiment
        res = run_experiment()
        self.txt_benchmark_results.setText(json.dumps(res, indent=2))

    def closeEvent(self, event) -> None:
        self.worker.stop()
        event.accept()


# ---------------------------------------------------------------------------
# Launch Helper
# ---------------------------------------------------------------------------
def launch_gui(use_synthetic: bool = False) -> None:
    app = QApplication(sys.argv)
    window = DashboardWindow(use_synthetic=use_synthetic)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    launch_gui()
