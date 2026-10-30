#!/usr/bin/env python3
"""
camera_pipeline.py - Live Video & Gesture Recognition Pipeline
Processes frames from webcam or synthetic source, extracts landmarks,
encodes Cl(3,0) features, and classifies gestures with real-time HUD.
"""

import time
import cv2
import numpy as np

from SW.host_camera.landmark_detector import HandLandmarkDetector
from SW.host_camera.feature_encoder import normalize_landmarks, encode_hand_multivectors
from SW.gesture.ga_classifier import GAGestureClassifier
from SW.host_camera.hardware_bridge import QGPUHardwareBridge

class LiveCameraPipeline:
    def __init__(self, camera_index=0, architecture="PARALLEL_GPU"):
        self.cam_idx = camera_index
        self.cap = None
        self.detector = HandLandmarkDetector()
        self.bridge = QGPUHardwareBridge(architecture=architecture)
        self.classifier = GAGestureClassifier(self.bridge)
        self.arch = architecture
        self.running = False
        self.frame_count = 0

        # Try to open webcam
        try:
            self.cap = cv2.VideoCapture(self.cam_idx)
            if not self.cap.isOpened():
                print(f"[CameraPipeline] Webcam {self.cam_idx} unavailable. Using synthetic fallback.")
                self.cap = None
        except Exception as e:
            print(f"[CameraPipeline] Error opening camera: {e}. Using synthetic fallback.")
            self.cap = None

    def read_frame(self):
        """Reads frame from webcam or generates synthetic test frame."""
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame

        # Generate synthetic fallback frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Gradient background
        for y in range(480):
            frame[y, :] = (int(25 + y*0.05), int(20 + y*0.08), int(35 + y*0.1))
        cv2.putText(frame, "SYNTHETIC HAND STREAM (FALLBACK)", (30, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 255), 2)
        return frame

    def process_next_frame(self):
        """Processes single frame through full end-to-end pipeline."""
        t_start = time.perf_counter_ns()
        self.frame_count += 1

        # 1. Capture
        t0 = time.perf_counter_ns()
        frame = self.read_frame()
        t_capture_us = (time.perf_counter_ns() - t0) / 1000.0

        # 2. Landmark Detection
        t0 = time.perf_counter_ns()
        landmarks = self.detector.process_frame(frame)
        if landmarks is None:
            # Synthetic gesture toggle every 60 frames
            gesture_cycle = ["OPEN_PALM", "FIST", "PEACE_V", "POINTING"]
            cur_synth = gesture_cycle[(self.frame_count // 60) % len(gesture_cycle)]
            landmarks = self.detector.generate_synthetic_hand(cur_synth)
        t_detect_us = (time.perf_counter_ns() - t0) / 1000.0

        # 3. Geometric Algebra Feature Encoding
        t0 = time.perf_counter_ns()
        norm_pts = normalize_landmarks(landmarks)
        ga_features = encode_hand_multivectors(norm_pts)
        t_encode_us = (time.perf_counter_ns() - t0) / 1000.0

        # 4. Gesture Classification via GA
        t0 = time.perf_counter_ns()
        result = self.classifier.classify(ga_features)
        t_classify_us = (time.perf_counter_ns() - t0) / 1000.0

        t_total_us = (time.perf_counter_ns() - t_start) / 1000.0

        # Annotate Frame with HUD
        annotated = frame.copy()
        h, w = annotated.shape[:2]

        # Draw landmarks
        for i, pt in enumerate(landmarks):
            px, py = int(pt.x * w), int(pt.y * h)
            cv2.circle(annotated, (px, py), 4, (0, 255, 128), -1)

        # Overlay Telemetry HUD
        cv2.rectangle(annotated, (15, 15), (320, 160), (20, 20, 20), -1)
        cv2.rectangle(annotated, (15, 15), (320, 160), (0, 220, 255), 1)

        cv2.putText(annotated, f"GESTURE: {result['gesture']} ({result['confidence']*100:.0f}%)",
                    (25, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0), 2)
        cv2.putText(annotated, f"ARCH: {self.arch} (100MHz)", (25, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
        cv2.putText(annotated, f"Capture:  {t_capture_us:.1f} us", (25, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
        cv2.putText(annotated, f"Detect:   {t_detect_us:.1f} us", (25, 105),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
        cv2.putText(annotated, f"GA Enc:   {t_encode_us:.1f} us", (25, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
        cv2.putText(annotated, f"GA Class: {t_classify_us:.1f} us", (25, 135),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1)
        cv2.putText(annotated, f"End-to-End: {t_total_us:.1f} us ({1e6/t_total_us:.1f} FPS)",
                    (25, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 220, 255), 1)

        timing_data = {
            "capture_us": t_capture_us,
            "detect_us": t_detect_us,
            "encode_us": t_encode_us,
            "classify_us": t_classify_us,
            "total_us": t_total_us,
            "fps": 1e6 / t_total_us if t_total_us > 0 else 0
        }

        return annotated, result, timing_data

    def release(self):
        if self.cap is not None:
            self.cap.release()
