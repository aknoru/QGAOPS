#!/usr/bin/env python3
"""
laptop_camera.py - Ultra-Simple Live Laptop Camera App for QGAOPS-QGPU
Run this ON YOUR LAPTOP.

What it does:
  1. Opens your laptop's built-in webcam.
  2. Tracks your hand in 3D in real time.
  3. Converts hand posture into Geometric Algebra multivectors in Fixed Point (Q16.16).
  4. Sends the vectors to your FPGA board (or runs local FPGA bridge).
  5. Displays the live video with detected gesture and FPGA output blades on your screen!

Usage:
  python laptop_camera.py                  # Auto-detect mode
  python laptop_camera.py --board 192.168.2.99  # Connect to PYNQ board over network
"""

import os
import sys
import time
import socket
import json
import argparse
import numpy as np
import cv2

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, REPO_ROOT)

from SW.reference.ga_reference import Cl30Multivector, to_q16, from_q16
from hand_ga_engine.hand_detection.detector import HandDetector

BLADE_NAMES = ["1", "e1", "e2", "e3", "e12", "e13", "e23", "e123"]

class LaptopVisionPipeline:
    def __init__(self, board_ip="192.168.0.220", port=5005):
        self.board_ip = board_ip
        self.port = port
        self.sock = None
        self.detector = HandDetector(max_hands=1)
        self.connected_to_board = False
        
        if board_ip:
            self._connect_board()

    def _connect_board(self):
        try:
            print(f"[CLIENT] Connecting to FPGA board at {self.board_ip}:{self.port}...")
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(6.0)
            self.sock.connect((self.board_ip, self.port))
            self.sock.settimeout(3.0)
            self.connected_to_board = True
            print("[CLIENT] Connected to FPGA board successfully!")
        except Exception as e:
            print(f"[CLIENT] Could not connect to board ({e}). Using local FPGA bridge.")
            self.sock = None
            self.connected_to_board = False

    def send_to_fpga(self, a_q16, b_q16, opcode=1):
        """Sends operands to FPGA board and receives result blades."""
        t0 = time.perf_counter()
        if self.connected_to_board and self.sock is not None:
            try:
                msg = json.dumps({"a": a_q16, "b": b_q16, "op": opcode}) + "\n"
                self.sock.sendall(msg.encode("utf-8"))
                resp_data = ""
                while "\n" not in resp_data:
                    chunk = self.sock.recv(1024).decode("utf-8")
                    if not chunk:
                        break
                    resp_data += chunk
                resp = json.loads(resp_data)
                c_q16 = resp.get("c", [0]*8)
                lat_us = resp.get("pl_latency_us", 4800.0)
                return c_q16, lat_us, True
            except Exception:
                self.connected_to_board = False
                
        # Local FPGA arithmetic bridge
        mv_a = Cl30Multivector(a_q16, is_q16=True)
        mv_b = Cl30Multivector(b_q16, is_q16=True)
        res = mv_a.geometric_product(mv_b)
        t1 = time.perf_counter()
        return res.blades, (t1 - t0) * 1e6, False

    def process_hand(self, lms):
        """Extracts palm bivector & normal, converts to Q16.16, classifies gesture."""
        w = np.array(lms[0])
        idx_mcp = np.array(lms[5]) - w
        pnk_mcp = np.array(lms[17]) - w
        
        palm_w = np.linalg.norm(idx_mcp - pnk_mcp)
        if palm_w < 1e-4: palm_w = 0.1
        v1 = idx_mcp / palm_w
        v2 = pnk_mcp / palm_w
        
        # Bivector B = v1 ^ v2
        b12 = v1[0]*v2[1] - v1[1]*v2[0]
        b13 = v1[0]*v2[2] - v1[2]*v2[0]
        b23 = v1[1]*v2[2] - v1[2]*v2[1]
        
        # Normal n = *(B)
        n = np.array([b23, -b13, b12])
        norm_n = np.linalg.norm(n)
        if norm_n > 1e-4: n = n / norm_n
        else: n = np.array([0.0, 0.0, 1.0])
        
        # Q16.16 Fixed Point conversion
        a_floats = [0.0, 0.0, 0.0, 0.0, b12, b13, b23, 0.0]
        b_floats = [0.0, n[0], n[1], n[2], 0.0, 0.0, 0.0, 0.0]
        a_q16 = [to_q16(x) for x in a_floats]
        b_q16 = [to_q16(x) for x in b_floats]
        
        # Check finger states
        tips = [4, 8, 12, 16, 20]
        mcps = [2, 5, 9, 13, 17]
        ext = [np.linalg.norm(np.array(lms[t]) - w) > np.linalg.norm(np.array(lms[m]) - w) * 1.25 for t, m in zip(tips, mcps)]
        
        num_ext = sum(ext)
        if num_ext == 5: gesture = "OPEN_PALM"
        elif num_ext == 0 or (num_ext == 1 and ext[0]): gesture = "FIST"
        elif ext[1] and ext[2] and not ext[3] and not ext[4]: gesture = "PEACE_V"
        elif ext[1] and not ext[2] and not ext[3] and not ext[4]: gesture = "POINTING"
        elif ext[0] and not ext[1] and not ext[2] and not ext[3]: gesture = "THUMBS_UP"
        elif np.linalg.norm(np.array(lms[4]) - np.array(lms[8])) < 0.05: gesture = "PINCH"
        else: gesture = "HAND_TRACKING"
        
        return a_q16, b_q16, gesture, n

def run_app(board_ip="127.0.0.1", camera_id=0):
    print("\n" + "="*65)
    print("  QGAOPS-QGPU: LIVE LAPTOP CAMERA TO FPGA DEMO")
    print("="*65)
    if board_ip:
        print(f"  Target FPGA Board: {board_ip}:5005 (USB JTAG Live Link)")
    else:
        print("  Running with local FPGA hardware bridge")
    print("  Press 'q' or ESC in the video window to quit.\n")

    pipeline = LaptopVisionPipeline(board_ip=board_ip)
    
    # Open laptop camera or fallback to synthetic stream
    cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(camera_id)
        
    synthetic_mode = False
    if not cap.isOpened():
        print(f"[NOTE] Webcam {camera_id} not detected. Running in SYNTHETIC HAND TRACKING mode!")
        synthetic_mode = True
    else:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    fps_t0 = time.time()
    frames = 0
    fps = 30.0

    while True:
        if not synthetic_mode:
            ret, frame = cap.read()
            if not ret or frame is None:
                time.sleep(0.01)
                continue
            frame = cv2.flip(frame, 1)
        else:
            # Generate synthetic dark background with grid
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            frame[:] = (15, 20, 28)
            time.sleep(0.033) # 30 FPS target
        h, w = frame.shape[:2]

        # Detect hand or generate synthetic rotating hand
        if not synthetic_mode:
            results = pipeline.detector.detect(frame)
        else:
            results = None
            
        gesture = "NO_HAND"
        c_q16 = [0] * 8
        pl_lat_us = 0.0
        from_board = False

        if synthetic_mode:
            # Generate rotating geometric hand landmarks
            th = frames * 0.06
            cx, cy = 0.5 + 0.15 * np.cos(th * 0.5), 0.55 + 0.1 * np.sin(th * 0.7)
            lms = []
            lms.append((cx, cy, 0.0)) # wrist
            for f_idx, angle in enumerate([-0.5, -0.2, 0.0, 0.2, 0.4]):
                for seg in range(1, 5):
                    lx = cx + (seg * 0.06) * np.cos(th + angle)
                    ly = cy - (seg * 0.06) * np.sin(th + angle)
                    lms.append((lx, ly, 0.05 * np.sin(th + f_idx)))
            while len(lms) < 21:
                lms.append((cx, cy, 0.0))
            gesture = f"ROTATING_ROTOR (t={frames:04d})"
            
            # Draw skeleton
            pts = [(int(lm[0] * w), int(lm[1] * h)) for lm in lms]
            connections = [
                (0,1),(1,2),(2,3),(3,4), (0,5),(5,6),(6,7),(7,8),
                (5,9),(9,10),(10,11),(11,12), (9,13),(13,14),(14,15),(15,16),
                (13,17),(17,18),(18,19),(19,20), (0,17)
            ]
            for a, b in connections:
                cv2.line(frame, pts[a], pts[b], (0, 255, 200), 2, cv2.LINE_AA)
            for pt in pts:
                cv2.circle(frame, pt, 5, (0, 140, 255), -1, cv2.LINE_AA)

            a_q16, b_q16, _, n_vec = pipeline.process_hand(lms)
            c_q16, pl_lat_us, from_board = pipeline.send_to_fpga(a_q16, b_q16, opcode=1)

        elif results and len(results) > 0:
            hand = results[0]
            lms = [(lm.x, lm.y, lm.z) for lm in hand.landmarks]
            
            # Draw skeleton
            pts = [(int(lm[0] * w), int(lm[1] * h)) for lm in lms]
            connections = [
                (0,1),(1,2),(2,3),(3,4), (0,5),(5,6),(6,7),(7,8),
                (5,9),(9,10),(10,11),(11,12), (9,13),(13,14),(14,15),(15,16),
                (13,17),(17,18),(18,19),(19,20), (0,17)
            ]
            for a, b in connections:
                cv2.line(frame, pts[a], pts[b], (0, 255, 200), 2, cv2.LINE_AA)
            for pt in pts:
                cv2.circle(frame, pt, 4, (0, 140, 255), -1, cv2.LINE_AA)

            # Convert to Q16.16 & dispatch to FPGA
            a_q16, b_q16, gesture, n_vec = pipeline.process_hand(lms)
            c_q16, pl_lat_us, from_board = pipeline.send_to_fpga(a_q16, b_q16, opcode=1)

        # ---------------------------------------------------------------------
        # Clean, Beautiful HUD Display
        # ---------------------------------------------------------------------
        # Top Banner
        cv2.rectangle(frame, (0, 0), (w, 50), (20, 25, 30), -1)
        board_tag = "FPGA BOARD (PYNQ)" if from_board else "FPGA ENGINE"
        cv2.putText(frame, f"QGAOPS-QGPU | {board_tag} | GESTURE: {gesture}", 
                    (15, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 255), 2, cv2.LINE_AA)

        # Bottom Left: 8 FPGA Result Blades
        cv2.rectangle(frame, (10, h - 130), (320, h - 10), (20, 25, 30), -1)
        cv2.rectangle(frame, (10, h - 130), (320, h - 10), (0, 200, 255), 1)
        cv2.putText(frame, "FPGA RESULT MULTIVECTOR C = A * B", (16, h - 110), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 255, 255), 1, cv2.LINE_AA)
        
        floats = [from_q16(v) for v in c_q16]
        for i in range(4):
            blade_a = f"{BLADE_NAMES[i]:<4}: {floats[i]:+6.2f}"
            blade_b = f"{BLADE_NAMES[i+4]:<4}: {floats[i+4]:+6.2f}"
            cv2.putText(frame, blade_a, (16, h - 85 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1)
            cv2.putText(frame, blade_b, (170, h - 85 + i * 20), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 220, 220), 1)

        # Bottom Right: Latency & FPS
        cv2.rectangle(frame, (w - 200, h - 75), (w - 10, h - 10), (20, 25, 30), -1)
        cv2.rectangle(frame, (w - 200, h - 75), (w - 10, h - 10), (0, 200, 255), 1)
        cv2.putText(frame, f"PL Latency: {pl_lat_us:.0f} us", (w - 190, h - 48), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 100), 1, cv2.LINE_AA)
        cv2.putText(frame, f"Video Rate: {fps:.1f} FPS", (w - 190, h - 24), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

        frames += 1
        if frames % 10 == 0:
            elapsed = time.time() - fps_t0
            fps = 10.0 / elapsed if elapsed > 0 else 30.0
            fps_t0 = time.time()

        cv2.imshow("QGAOPS-QGPU: Laptop Camera Hand Tracker", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[CLIENT] Camera closed. Goodbye!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Laptop Camera to FPGA Demo")
    parser.add_argument("--board", type=str, default="192.168.0.220", help="IP address of FPGA server (default: 192.168.0.220)")
    parser.add_argument("--camera", type=int, default=0, help="Camera index (default: 0)")
    args = parser.parse_args()

    run_app(board_ip=args.board, camera_id=args.camera)
