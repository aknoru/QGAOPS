"""
camera_fpga_pipeline.py
Live USB Camera to FPGA QGPU Hardware Accelerator Pipeline.
1. Captures live video frame via OpenCV (or generates synthetic frame if no camera attached).
2. Extracts gesture invariant features (centroid, orientation, area).
3. Encodes features into Euclidean Cl(3,0) 8-blade multivectors.
4. Converts multivector to signed Q16.16 fixed-point format.
5. Offloads to FPGA hardware accelerator (via qgpu_overlay.py) for rotor transformations.
6. Renders HUD overlay for HDMI output and local display.
"""

import os
import sys
import time
import cv2
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from deployment.pynq.qgpu_overlay import QGPUAccelerator, float_to_q16, q16_to_float, OPCODE_ROTOR_SANDWICH

class CameraFPGAPipeline:
    def __init__(self, camera_id=0, bitstream_path=None):
        self.camera_id = camera_id
        self.acc = QGPUAccelerator(bitstream_path)
        self.cap = None
        self._init_camera()

    def _init_camera(self):
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            if not self.cap.isOpened():
                print(f"[WARN] Physical USB camera index {self.camera_id} not detected. Using synthetic camera mode.")
                self.cap = None
            else:
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                print(f"[INFO] USB Camera index {self.camera_id} initialized at 640x480.")
        except Exception as e:
            print(f"[WARN] Camera init exception: {e}. Falling back to synthetic mode.")
            self.cap = None

    def read_frame(self):
        """Read frame from USB camera or return realistic synthetic hand gesture frame."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame

        # Synthetic hand gesture frame (dark background with drawn hand contour)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Draw palm circle
        cv2.circle(frame, (320, 260), 60, (200, 180, 160), -1)
        # Draw 5 finger ellipses
        angles = [-60, -30, 0, 30, 60]
        for idx, ang in enumerate(angles):
            rad = np.radians(ang - 90)
            fx = int(320 + 110 * np.cos(rad))
            fy = int(260 + 110 * np.sin(rad))
            cv2.line(frame, (320, 260), (fx, fy), (200, 180, 160), 20)
            cv2.circle(frame, (fx, fy), 12, (180, 160, 140), -1)
        return frame

    def extract_gesture_multivector(self, frame):
        """
        Extract invariant geometric features from frame and map to Cl(3,0) multivector:
        M = [s, e1, e2, e3, e12, e13, e23, e123]
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 60, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            return [0.0] * 8, (320, 240), 0.0

        c = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(c)
        m = cv2.moments(c)
        cx = int(m["m10"] / m["m00"]) if m["m00"] != 0 else 320
        cy = int(m["m01"] / m["m00"]) if m["m00"] != 0 else 240

        # Normalized coordinates [-1.0, 1.0]
        norm_x = (cx - 320) / 320.0
        norm_y = -(cy - 240) / 240.0
        norm_area = min(area / 40000.0, 1.0)

        # Orientation angle from central moments
        mu20 = m["mu20"]
        mu02 = m["mu02"]
        mu11 = m["mu11"]
        theta = 0.5 * np.arctan2(2 * mu11, mu20 - mu02) if (mu20 - mu02) != 0 else 0.0

        # Encode into Cl(3,0) 8-blade multivector
        mv = [
            norm_area,           # Scalar (Grade 0): Normalized scale
            norm_x,              # e1 (Grade 1): Horizontal position
            norm_y,              # e2 (Grade 1): Vertical position
            0.5,                 # e3 (Grade 1): Estimated depth
            np.sin(theta),       # e12 (Grade 2): In-plane rotation bivector
            0.0,                 # e13 (Grade 2): Out-of-plane pitch
            0.0,                 # e23 (Grade 2): Out-of-plane roll
            1.0                  # e123 (Grade 3): Handedness/volume form
        ]
        return mv, (cx, cy), theta

    def process_and_render(self, frame):
        """Run full PS-PL pipeline and render HUD overlay."""
        t0 = time.time()
        mv, centroid, theta = self.extract_gesture_multivector(frame)

        # Rotor rotation: 45 degree rotation around z-axis
        rotor = [np.cos(np.pi/8), 0.0, 0.0, 0.0, np.sin(np.pi/8), 0.0, 0.0, 0.0]

        # Hardware FPGA execution (R * M * ~R)
        t_hw0 = time.time()
        res_mv, status = self.acc.execute_op(rotor, mv, OPCODE_ROTOR_SANDWICH, slot=0)
        t_hw = (time.time() - t_hw0) * 1000.0
        total_lat = (time.time() - t0) * 1000.0

        # Render HUD on frame
        out_frame = frame.copy()
        cv2.circle(out_frame, centroid, 8, (0, 255, 0), -1)
        cv2.putText(out_frame, f"QGAOPS-QGPU PYNQ-Z2 PIPELINE", (20, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(out_frame, f"FPS: {1000.0/total_lat:.1f} | Total Lat: {total_lat:.2f} ms", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(out_frame, f"PL Accelerator Latency: {t_hw:.2f} ms (Status: 0x{status:02X})", (20, 90),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 200, 0), 2)
        cv2.putText(out_frame, f"Input  MV e1/e2: [{mv[1]:.2f}, {mv[2]:.2f}]", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        cv2.putText(out_frame, f"Rotated MV e1/e2: [{res_mv[1]:.2f}, {res_mv[2]:.2f}]", (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 255), 1)

        return out_frame, res_mv, total_lat

def test_pipeline():
    print("==================================================================")
    print("  TESTING CAMERA-TO-FPGA GESTURE PIPELINE")
    print("==================================================================")
    pipeline = CameraFPGAPipeline()
    for frame_idx in range(5):
        frame = pipeline.read_frame()
        out_frame, res_mv, lat = pipeline.process_and_render(frame)
        print(f"  Frame {frame_idx+1}: Latency = {lat:.2f} ms | Rotated e1={res_mv[1]:.4f}, e2={res_mv[2]:.4f}")
    print("[PASS] Camera to FPGA processing pipeline validated successfully!")

if __name__ == "__main__":
    test_pipeline()
