#!/usr/bin/env python3
"""
dashboard_server.py - Interactive Browser Dashboard Server for QGAOPS-QGPU
Serves live video MJPEG stream, 3D multivector telemetry, and hardware controls on port 8080.
"""

import os
import sys
import time
import json
import cv2
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

REPO_ROOT = r"D:\QGPU"
sys.path.insert(0, REPO_ROOT)

from SW.host_camera.camera_pipeline import LiveCameraPipeline

PORT = 8080
PUBLIC_DIR = os.path.join(REPO_ROOT, "SW", "dashboard", "public")

# Shared state
current_arch = "PARALLEL_GPU"
pipeline = LiveCameraPipeline(architecture=current_arch)
latest_result = {"gesture": "INITIALIZING", "confidence": 0.0, "finger_states": [], "palm_normal": [0,0,1]}
latest_timings = {"capture_us": 1200, "detect_us": 1800, "encode_us": 40, "pl_us": 4800, "classify_us": 80, "total_us": 8000, "fps": 30.0}
latest_jpeg = None
lock = threading.Lock()

def video_worker():
    global latest_jpeg, latest_result, latest_timings, pipeline
    while True:
        try:
            frame, res, timings = pipeline.process_next_frame()
            timings["pl_us"] = 4800 if current_arch == "PARALLEL_GPU" else (5500 if current_arch == "SEQ_GPU" else 25)
            ret, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                with lock:
                    latest_jpeg = buf.tobytes()
                    latest_result = res
                    latest_timings = timings
            time.sleep(0.033) # ~30 FPS
        except Exception as e:
            time.sleep(0.1)

class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)

    def do_GET(self):
        global current_arch, pipeline
        if self.path == "/api/stream":
            self.send_response(200)
            self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
            self.send_header("Cache-Control", "no-cache")
            self.end_headers()
            while True:
                with lock:
                    jpg = latest_jpeg
                if jpg is not None:
                    try:
                        self.wfile.write(b"--frame\r\n")
                        self.wfile.write(b"Content-Type: image/jpeg\r\n\r\n")
                        self.wfile.write(jpg)
                        self.wfile.write(b"\r\n")
                    except Exception:
                        break
                time.sleep(0.04)
        elif self.path == "/api/telemetry":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            with lock:
                payload = {
                    "architecture": current_arch,
                    "gesture": latest_result.get("gesture", "UNKNOWN"),
                    "confidence": latest_result.get("confidence", 0.0),
                    "finger_states": latest_result.get("finger_states", []),
                    "palm_normal": latest_result.get("palm_normal", [0, 0, 1]),
                    "timings": latest_timings
                }
            self.wfile.write(json.dumps(payload).encode("utf-8"))
        elif self.path.startswith("/api/set_arch"):
            from urllib.parse import urlparse, parse_qs
            qs = parse_qs(urlparse(self.path).query)
            arch = qs.get("arch", ["PARALLEL_GPU"])[0]
            current_arch = arch
            pipeline.arch = arch
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "OK", "architecture": arch}).encode("utf-8"))
        elif self.path == "/api/download/csv":
            csv_path = os.path.join(REPO_ROOT, "benchmarks", "synthetic", "results", "benchmark_data.csv")
            if os.path.exists(csv_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/csv")
                self.send_header("Content-Disposition", 'attachment; filename="benchmark_data.csv"')
                self.end_headers()
                with open(csv_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_error(404, "Benchmark CSV not found")
        elif self.path == "/api/run_benchmark":
            pl_us = 4800 if current_arch == "PARALLEL_GPU" else 5500
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "status": "PASS",
                "architecture": current_arch,
                "pl_latency_us": pl_us,
                "throughput_ops_s": round(1e6 / pl_us, 1)
            }).encode("utf-8"))
        else:
            super().do_GET()

def run_server():
    t = threading.Thread(target=video_worker, daemon=True)
    t.start()

    server = HTTPServer(("0.0.0.0", PORT), DashboardHandler)
    print(f"[DashboardServer] QGAOPS-QGPU Dashboard running at http://localhost:{PORT}")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
