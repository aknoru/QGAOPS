"""
LIVE HAND GEOMETRIC ALGEBRA ENGINE
main.py — Entry point

[IMPLEMENTED] Full live webcam mode, benchmark, FIX16, golden-vector generation,
              profiling, record/replay, experiment, data collection modes.

[SOFTWARE DEMONSTRATOR] This is the Python golden model for QGAOPS-QGPU.
[NOT IMPLEMENTED] No FPGA operations are performed.

Run:
    python main.py                   # Live webcam mode
    python main.py --benchmark       # Benchmark mode
    python main.py --fixed           # FIX16 mode
    python main.py --generate-golden # Generate golden vectors
    python main.py --profile         # Profiling mode
    python main.py --record          # Record to recording.json
    python main.py --replay FILE     # Replay from file
    python main.py --experiment      # Deterministic experiment
    python main.py --collect-data    # Gesture data collection
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import sys
import time
from collections import deque
from typing import Any, Dict, List, Optional

import numpy as np

# ---------------------------------------------------------------------------
# Project root on sys.path (handles running from project dir)
# ---------------------------------------------------------------------------
_HERE = pathlib.Path(__file__).parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# ---------------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------------
from config.config import (
    CAMERA_INDEX, CAMERA_WIDTH, CAMERA_HEIGHT, CAMERA_FPS,
    MEDIAPIPE_MAX_HANDS, MEDIAPIPE_MIN_DETECTION_CONF,
    MEDIAPIPE_MIN_TRACKING_CONF, MEDIAPIPE_MODEL_COMPLEXITY,
    LANDMARK_SMOOTHING_ALPHA, VECTOR_3D_UPDATE_EVERY,
    BENCHMARK_ITERATIONS, PROFILE_SAVE_DIR, EXPERIMENT_DIR,
    GOLDEN_DIR, RECORDING_DEFAULT, DEFAULT_BACKEND,
    KEY_QUIT, KEY_GP, KEY_DOT, KEY_WEDGE, KEY_ROTOR, KEY_SANDWICH,
    KEY_FIX16, KEY_BENCHMARK, KEY_VECTORS, KEY_HELP, KEY_NEXT_MODE,
    GESTURE_CONFIDENCE_MIN, GESTURE_STABLE_FRAMES, GESTURE_COOLDOWN_FRAMES,
    TEMPORAL_BUFFER_FRAMES,
)
from engine.algebra_engine import AlgebraEngine
from engine.operation_scheduler import OperationScheduler
from hand_detection import (
    HandDetector, LandmarkSmoother, HandGeometryExtractor, StaticPoseRecognizer
)
from mapping.hand_to_ga import hand_to_multivectors
from expression.dynamic_recognizer import DynamicExpressionRecognizer
from expression.state_machine import ExpressionStateMachine
from expression.expression_to_ga import ExpressionToGA
from ga.multivector import Multivector
from ga.rotor import rotor_from_axis_angle
from fixed_point.fix16 import (
    Fix16Multivector, fix16_geometric_product, fix16_error_analysis
)
from visualization.webcam_view import draw_webcam_overlay, draw_no_hand_message
from visualization.vector_view import VectorView3D
from visualization.dashboard import make_info_panel, assemble_dashboard
from control.controller import GestureController
from visualization.control_overlay import render_control_hud

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Operation modes
MODES = [
    "HAND GEOMETRY",
    "DOT PRODUCT",
    "WEDGE PRODUCT",
    "GEOMETRIC PRODUCT",
    "ROTOR",
    "SANDWICH PRODUCT",
    "FINGER ANGLES",
    "DISTANCE ANALYSIS",
    "FIXED-POINT",
    "PERFORMANCE",
    "QGAOPS PIPELINE",
]


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Live Hand Geometric Algebra Engine — QGAOPS-QGPU Demonstrator"
    )
    p.add_argument("--benchmark",       action="store_true",  help="Run GA benchmark")
    p.add_argument("--microbenchmark",  action="store_true",  help="Run high-resolution GA microbenchmark")
    p.add_argument("--e2e-benchmark",   action="store_true",  help="Run end-to-end pipeline benchmark")
    p.add_argument("--gui",             action="store_true",  help="Launch PySide6 engineering dashboard")
    p.add_argument("--fixed",           action="store_true",  help="Enable FIX16 mode")
    p.add_argument("--generate-golden", action="store_true",  help="Generate golden vectors")
    p.add_argument("--profile",         action="store_true",  help="Profile performance")
    p.add_argument("--record",          action="store_true",  help="Record landmarks to file")
    p.add_argument("--replay",          type=str,  default=None, help="Replay from JSON file")
    p.add_argument("--experiment",      action="store_true",  help="Run deterministic experiment")
    p.add_argument("--collect-data",    action="store_true",  help="Collect gesture data")
    p.add_argument("--expression-benchmark", action="store_true", help="Expression benchmarking")
    p.add_argument("--camera",          type=int,  default=CAMERA_INDEX, help="Camera index")
    p.add_argument("--backend",         type=str,  default=DEFAULT_BACKEND)
    p.add_argument("--no-webcam",       action="store_true",  help="Disable webcam (synthetic mode)")
    p.add_argument(
        "--control",
        type=str,
        choices=["mouse", "presentation", "media", "object3d", "debug"],
        default=None,
        help="Enable computer vision gesture control with specified profile",
    )
    return p.parse_args()


# ---------------------------------------------------------------------------
# Benchmark mode
# ---------------------------------------------------------------------------

def run_benchmark(engine: AlgebraEngine) -> None:
    """Run GA operation benchmark and print results."""
    print("\n=== QGAOPS-QGPU Software Benchmark [IMPLEMENTED] ===")
    print(f"{'Operation':<20} {'N':>8} {'Total (s)':>12} {'Ops/s':>12}")
    print("-" * 56)

    ops = [
        ("GP",       lambda: engine.gp(Multivector.vector(0.6, 0.8, 0.0), Multivector.vector(0.3, 0.5, 0.7))),
        ("WEDGE",    lambda: engine.wedge(Multivector.vector(0.6, 0.8, 0.0), Multivector.vector(0.3, 0.5, 0.7))),
        ("DOT",      lambda: engine.dot(Multivector.vector(0.6, 0.8, 0.0), Multivector.vector(0.3, 0.5, 0.7))),
        ("REVERSE",  lambda: engine.reverse(Multivector.vector(0.6, 0.8, 0.0))),
        ("SANDWICH", lambda: engine.sandwich(
            rotor_from_axis_angle(np.array([0.0, 0.0, 1.0]), 0.5),
            Multivector.vector(1.0, 0.0, 0.0)
        )),
        ("NORM",     lambda: engine.norm(Multivector.vector(0.6, 0.8, 0.0))),
    ]

    results = []
    N = BENCHMARK_ITERATIONS
    for name, fn in ops:
        t0 = time.perf_counter()
        for _ in range(N):
            fn()
        elapsed = time.perf_counter() - t0
        opsec = N / elapsed
        print(f"{name:<20} {N:>8} {elapsed:>12.4f} {opsec:>12.1f}")
        results.append({"operation": name, "n": N, "runtime_s": elapsed, "ops_s": opsec})

    # Save results
    out_dir = pathlib.Path("results/performance")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "hand_ga_benchmark.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[IMPLEMENTED] Results saved to {out_path}")


def run_microbenchmark(engine: AlgebraEngine) -> None:
    """Run high-resolution nanosecond microbenchmark across all GA primitives."""
    from ga.geometric_product import geometric_product
    from ga.rotor import rotor_from_axis_angle

    print("\n=== QGAOPS-QGPU High-Resolution Microbenchmark [MEASURED SOFTWARE] ===")
    print(f"{'Primitive':<18} {'N':>8} {'Mean Latency':>16} {'P95 Latency':>16} {'Throughput':>16}")
    print("-" * 76)

    v1 = Multivector.vector(0.6, 0.8, 0.0)
    v2 = Multivector.vector(0.3, 0.5, 0.7)
    rotor = rotor_from_axis_angle(np.array([0.0, 0.0, 1.0]), 0.5)

    ops = [
        ("GP", lambda: engine.gp(v1, v2)),
        ("WEDGE", lambda: engine.wedge(v1, v2)),
        ("DOT", lambda: engine.dot(v1, v2)),
        ("NORM", lambda: engine.norm(v1)),
        ("REVERSE", lambda: engine.reverse(v1)),
        ("ROTOR_GEN", lambda: rotor_from_axis_angle(np.array([0.0, 0.0, 1.0]), 0.5)),
        ("SANDWICH", lambda: engine.sandwich(rotor, v1)),
    ]

    N = 20000
    results = []
    for name, fn in ops:
        # warmup
        for _ in range(1000):
            fn()
        t_lats = []
        for _ in range(N):
            t0 = time.perf_counter_ns()
            fn()
            t_lats.append((time.perf_counter_ns() - t0) / 1000.0)  # µs
        t_lats.sort()
        mean_us = float(np.mean(t_lats))
        p95_us = float(np.percentile(t_lats, 95))
        throughput = 1e6 / max(mean_us, 1e-6)
        print(f"{name:<18} {N:>8} {mean_us:13.3f} µs {p95_us:13.3f} µs {throughput:13.1f} ops/s")
        results.append({
            "primitive": name,
            "iterations": N,
            "mean_latency_us": round(mean_us, 3),
            "p95_latency_us": round(p95_us, 3),
            "throughput_ops_s": round(throughput, 1),
            "classification": "[MEASURED SOFTWARE]",
        })

    out_path = pathlib.Path("results/performance/microbenchmark_results.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[MEASURED SOFTWARE] Results written to {out_path}")


def run_e2e_benchmark(engine: AlgebraEngine) -> None:
    """Run full end-to-end dataset, classification, GA, and metrics benchmark."""
    from experiments.run_expression_experiment import run_experiment
    run_experiment()


# ---------------------------------------------------------------------------
# FIX16 validation
# ---------------------------------------------------------------------------

def run_fix16_validation() -> None:
    """Validate FIX16 vs FLOAT32 for all GA operations."""
    from ga.geometric_product import geometric_product
    from fixed_point.fix16 import Fix16Multivector, fix16_geometric_product, fix16_error_analysis

    print("\n=== FIX16 Validation [IMPLEMENTED] ===")
    test_vectors = [
        (Multivector.vector(0.6, 0.8, 0.0), Multivector.vector(0.3, 0.5, 0.7)),
        (Multivector.vector(1.0, 0.0, 0.0), Multivector.vector(0.0, 1.0, 0.0)),
        (Multivector.vector(0.577, 0.577, 0.577), Multivector.vector(-0.577, 0.577, -0.577)),
    ]

    print(f"{'Test':<6} {'max|err|':>12} {'mean|err|':>12} {'RMS':>12}")
    print("-" * 46)

    for i, (a, b) in enumerate(test_vectors):
        fp_result  = geometric_product(a, b)
        fa = Fix16Multivector.from_multivector(a)
        fb = Fix16Multivector.from_multivector(b)
        fix_result = fix16_geometric_product(fa, fb)
        max_e, mean_e, rms_e = fix16_error_analysis(fp_result, fix_result)
        print(f"{i+1:<6} {max_e:>12.2e} {mean_e:>12.2e} {rms_e:>12.2e}")

    print("\n[IMPLEMENTED] FIX16 validation complete.")


# ---------------------------------------------------------------------------
# Golden vector generation
# ---------------------------------------------------------------------------

def run_generate_golden() -> None:
    """Generate deterministic golden vectors for RTL verification."""
    from ga.geometric_product import geometric_product, outer_product, inner_product
    from ga.rotor import rotor_from_axis_angle, sandwich_product
    from fixed_point.fix16 import Fix16Multivector, fix16_geometric_product, fix16_error_analysis

    golden_dir = pathlib.Path(GOLDEN_DIR)
    golden_dir.mkdir(parents=True, exist_ok=True)

    vectors = [
        ("v_x", Multivector.vector(1.0, 0.0, 0.0)),
        ("v_y", Multivector.vector(0.0, 1.0, 0.0)),
        ("v_z", Multivector.vector(0.0, 0.0, 1.0)),
        ("v_xy", Multivector.vector(0.6, 0.8, 0.0)),
        ("v_xyz", Multivector.vector(0.577, 0.577, 0.577)),
        ("v_neg", Multivector.vector(-0.5, 0.3, -0.8)),
    ]

    golden_records = []
    for i, (na, a) in enumerate(vectors):
        for j, (nb, b) in enumerate(vectors):
            if j <= i:
                continue
            # Float32 GP
            gp = geometric_product(a, b)
            wp = outer_product(a, b)
            ip = inner_product(a, b)

            # FIX16 GP
            fa = Fix16Multivector.from_multivector(a)
            fb = Fix16Multivector.from_multivector(b)
            fix_gp = fix16_geometric_product(fa, fb)
            max_e, mean_e, rms_e = fix16_error_analysis(gp, fix_gp)

            rec = {
                "id": len(golden_records),
                "input_a": {"label": na, "coeffs": a.to_list()},
                "input_b": {"label": nb, "coeffs": b.to_list()},
                "operations": {
                    "GP_FLOAT32":  gp.to_list(),
                    "WEDGE_FLOAT32": wp.to_list(),
                    "INNER_FLOAT32": ip.to_list(),
                    "GP_FIX16":    fix_gp.to_multivector().to_list(),
                },
                "fix16_error": {
                    "max_abs": max_e,
                    "mean_abs": mean_e,
                    "rms": rms_e,
                },
                "note": "[MEASURED] Deterministic golden vector for RTL verification.",
            }
            golden_records.append(rec)

    # Rotor golden vectors
    axes = [
        ("axis_z", np.array([0.0, 0.0, 1.0])),
        ("axis_x", np.array([1.0, 0.0, 0.0])),
        ("axis_diag", np.array([0.577, 0.577, 0.577])),
    ]
    angles = [0.0, np.pi/6, np.pi/4, np.pi/2, np.pi]
    v_test = Multivector.vector(1.0, 0.0, 0.0)
    rotor_records = []
    for aname, axis in axes:
        for angle in angles:
            R = rotor_from_axis_angle(axis, angle)
            v_rot = sandwich_product(R, v_test)
            rotor_records.append({
                "axis": aname,
                "axis_values": axis.tolist(),
                "angle_rad": float(angle),
                "angle_deg": float(np.degrees(angle)),
                "rotor_coeffs": R.to_list(),
                "input_vector": v_test.to_list(),
                "rotated_vector": v_rot.to_list(),
                "note": "[MEASURED] Rotor sandwich product golden vector.",
            })

    # Hand landmark golden vectors (synthetic)
    hand_records = _generate_hand_landmark_golden()

    out = {
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "algebra": "G(3,0,0)",
        "precision_float": "FLOAT32",
        "precision_fixed": "Q1.14 FIX16",
        "ga_product_vectors": golden_records,
        "rotor_vectors": rotor_records,
        "hand_landmark_vectors": hand_records,
        "notes": (
            "[IMPLEMENTED] Deterministic golden vectors for RTL verification. "
            "All values computed by QGAOPS-QGPU software golden model."
        ),
    }

    out_path = golden_dir / "hand_ga_golden.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    n = len(golden_records) + len(rotor_records) + len(hand_records)
    print(f"\n[IMPLEMENTED] Generated {n} golden vectors → {out_path}")


def _generate_hand_landmark_golden() -> List[Dict]:
    """Generate synthetic hand landmark → GA golden vectors."""
    from mapping.hand_to_ga import hand_to_multivectors
    from hand_detection.landmarks import HandGeometryExtractor

    # Synthetic flat open hand (normalized [0,1] MediaPipe-like coords)
    lm = np.array([
        [0.5, 0.7, 0.0],  # 0 wrist
        [0.45,0.62,0.0],[0.40,0.55,0.0],[0.37,0.50,0.0],[0.34,0.45,0.0],  # thumb
        [0.50,0.58,0.0],[0.50,0.50,0.0],[0.50,0.44,0.0],[0.50,0.38,0.0],  # index
        [0.54,0.58,0.0],[0.54,0.49,0.0],[0.54,0.43,0.0],[0.54,0.37,0.0],  # middle
        [0.58,0.59,0.0],[0.58,0.50,0.0],[0.58,0.44,0.0],[0.58,0.39,0.0],  # ring
        [0.62,0.61,0.0],[0.62,0.54,0.0],[0.62,0.49,0.0],[0.62,0.44,0.0],  # pinky
    ], dtype=np.float32)

    extractor = HandGeometryExtractor()
    geom = extractor.extract(lm, lm, confidence=1.0, handedness="Right")
    mvs  = hand_to_multivectors(geom)

    from ga.geometric_product import geometric_product, outer_product
    v_idx = mvs["index_vec"]
    v_mid = mvs["middle_vec"]

    gp  = geometric_product(v_idx, v_mid)
    wp  = outer_product(v_idx, v_mid)

    records = [{
        "id": 0,
        "description": "Synthetic open right hand",
        "landmarks": lm.tolist(),
        "finger_vectors": {k: mvs[k].to_list() for k in ["index_vec","middle_vec","ring_vec","pinky_vec","thumb_vec"]},
        "operations": {
            "index_x_middle_GP":    gp.to_list(),
            "index_x_middle_WEDGE": wp.to_list(),
        },
        "note": "[IMPLEMENTED] Synthetic hand landmark golden vector.",
    }]

    return records


# ---------------------------------------------------------------------------
# Profiling
# ---------------------------------------------------------------------------

def run_profile(engine: AlgebraEngine, n_frames: int = 500) -> None:
    """Profile per-stage latency."""
    import statistics

    detector  = HandDetector(MEDIAPIPE_MAX_HANDS, MEDIAPIPE_MIN_DETECTION_CONF, MEDIAPIPE_MIN_TRACKING_CONF)
    smoother  = LandmarkSmoother(LANDMARK_SMOOTHING_ALPHA)
    extractor = HandGeometryExtractor()

    a = Multivector.vector(0.6, 0.8, 0.0)
    b = Multivector.vector(0.3, 0.5, 0.7)

    timings = {"detection": [], "smoothing": [], "geometry": [], "ga": []}

    # Fake frame (no real camera)
    frame = np.zeros((480, 640, 3), dtype=np.uint8)

    for _ in range(n_frames):
        t0 = time.perf_counter()
        _ = detector.detect(frame)
        timings["detection"].append(time.perf_counter() - t0)

        lm = np.random.rand(21, 3).astype(np.float32) * 0.8 + 0.1
        t1 = time.perf_counter()
        smooth = smoother.update(lm)
        timings["smoothing"].append(time.perf_counter() - t1)

        t2 = time.perf_counter()
        geom = extractor.extract(lm, smooth)
        timings["geometry"].append(time.perf_counter() - t2)

        t3 = time.perf_counter()
        engine.gp(a, b)
        timings["ga"].append(time.perf_counter() - t3)

    print("\n=== Profile Results [IMPLEMENTED] ===")
    print(f"{'Stage':<20} {'Mean (ms)':>12} {'P50 (ms)':>12} {'P95 (ms)':>12} {'P99 (ms)':>12}")
    print("-" * 68)

    all_data = {}
    for name, vals in timings.items():
        ms = [v * 1000 for v in vals]
        m   = statistics.mean(ms)
        p50 = sorted(ms)[int(0.50 * len(ms))]
        p95 = sorted(ms)[int(0.95 * len(ms))]
        p99 = sorted(ms)[int(0.99 * len(ms))]
        print(f"{name:<20} {m:>12.3f} {p50:>12.3f} {p95:>12.3f} {p99:>12.3f}")
        all_data[name] = {"mean_ms": m, "p50_ms": p50, "p95_ms": p95, "p99_ms": p99}

    out_dir = pathlib.Path(PROFILE_SAVE_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "profile_results.json"
    with open(out_path, "w") as f:
        json.dump(all_data, f, indent=2)
    print(f"\n[IMPLEMENTED] Profile saved to {out_path}")


# ---------------------------------------------------------------------------
# Record mode
# ---------------------------------------------------------------------------

def run_record(camera_index: int, output_path: str = RECORDING_DEFAULT) -> None:
    """Record hand landmarks to a JSON file."""
    try:
        import cv2
    except ImportError:
        print("[ERROR] OpenCV not available.")
        return

    detector  = HandDetector(MEDIAPIPE_MAX_HANDS, MEDIAPIPE_MIN_DETECTION_CONF, MEDIAPIPE_MIN_TRACKING_CONF)
    smoother  = LandmarkSmoother(LANDMARK_SMOOTHING_ALPHA)
    extractor = HandGeometryExtractor()
    pose_rec  = StaticPoseRecognizer()

    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open camera {camera_index}.")
        return

    frames = []
    print(f"[RECORD] Recording... press Q to stop. Saving to {output_path}")
    frame_idx = 0
    t_start = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        ts = time.time() - t_start
        hands = detector.detect(frame)

        if hands:
            lm_raw = hands[0].to_array()
            lm_smooth = smoother.update(lm_raw)
            geom = extractor.extract(lm_raw, lm_smooth, hands[0].confidence, hands[0].handedness, frame_idx)
            gr   = pose_rec.recognize(geom)

            frames.append({
                "frame": frame_idx,
                "timestamp": ts,
                "handedness": hands[0].handedness,
                "confidence": hands[0].confidence,
                "landmarks": lm_raw.tolist(),
                "pose": gr.pose,
                "pose_confidence": gr.confidence,
            })

        # Display
        annotated = detector.draw_landmarks(frame, hands)
        cv2.putText(annotated, f"RECORDING | Frame {frame_idx} | Q to stop",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 80, 255), 2)
        cv2.imshow("Record", annotated)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_idx += 1

    cap.release()
    cv2.destroyAllWindows()

    recording = {"frames": frames, "total_frames": frame_idx, "duration_s": time.time() - t_start}
    with open(output_path, "w") as f:
        json.dump(recording, f, indent=2)
    print(f"[RECORD] Saved {len(frames)} frames with hands → {output_path}")


# ---------------------------------------------------------------------------
# Replay mode
# ---------------------------------------------------------------------------

def run_replay(replay_path: str, engine: AlgebraEngine) -> None:
    """Replay recorded landmarks and recompute GA results."""
    extractor  = HandGeometryExtractor()
    smoother   = LandmarkSmoother(LANDMARK_SMOOTHING_ALPHA)
    pose_rec   = StaticPoseRecognizer()
    expr_to_ga = ExpressionToGA(engine)

    with open(replay_path) as f:
        recording = json.load(f)

    frames = recording.get("frames", [])
    print(f"[REPLAY] {len(frames)} frames from {replay_path}")

    results = []
    for rec in frames:
        lm_raw = np.array(rec["landmarks"], dtype=np.float32)
        lm_sm  = smoother.update(lm_raw)
        geom   = extractor.extract(lm_raw, lm_sm, rec["confidence"], rec["handedness"], rec["frame"])
        mvs    = hand_to_multivectors(geom)
        gr     = pose_rec.recognize(geom)
        ga_res = expr_to_ga.map(gr.pose, geom, mvs)

        results.append({
            "frame": rec["frame"],
            "timestamp": rec["timestamp"],
            "pose": gr.pose,
            "pose_confidence": gr.confidence,
            "ga_opcode": ga_res.opcode if ga_res else None,
            "ga_result": str(ga_res.result) if ga_res else None,
        })

    out_dir = pathlib.Path(EXPERIMENT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "replay_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"[REPLAY] Done. Results → {out_path}")


# ---------------------------------------------------------------------------
# Experiment mode
# ---------------------------------------------------------------------------

def run_experiment(engine: AlgebraEngine) -> None:
    """Run deterministic experiment over synthetic trajectories."""
    smoother   = LandmarkSmoother(LANDMARK_SMOOTHING_ALPHA)
    extractor  = HandGeometryExtractor()
    pose_rec   = StaticPoseRecognizer()
    expr_to_ga = ExpressionToGA(engine)
    scheduler  = OperationScheduler(backend="python", precision="FLOAT32")

    np.random.seed(42)
    N_FRAMES = 200
    latencies = []
    all_ir = []

    for i in range(N_FRAMES):
        lm = (np.random.rand(21, 3) * 0.6 + 0.2).astype(np.float32)
        t0 = time.perf_counter()
        lm_sm = smoother.update(lm)
        geom  = extractor.extract(lm, lm_sm, 0.9, "Right", i)
        mvs   = hand_to_multivectors(geom)
        gr    = pose_rec.recognize(geom)
        ga_r  = expr_to_ga.map(gr.pose, geom, mvs)
        latencies.append((time.perf_counter() - t0) * 1000)
        if ga_r:
            all_ir.append(ga_r.ir)

    schedule = scheduler.schedule(all_ir)

    results = {
        "n_frames": N_FRAMES,
        "mean_latency_ms": float(np.mean(latencies)),
        "p95_latency_ms":  float(sorted(latencies)[int(0.95 * N_FRAMES)]),
        "p99_latency_ms":  float(sorted(latencies)[int(0.99 * N_FRAMES)]),
        "throughput_fps":  float(1000.0 / (np.mean(latencies) + 1e-9)),
        "schedule_summary": {
            "total_ops":  schedule.total_ops,
            "peak_live":  schedule.peak_live,
            "memory_b0":  schedule.b0_materialize,
            "memory_b4":  schedule.b4_lifetime_reuse,
            "memory_b5":  schedule.b5_fusion,
            "fused":      schedule.fusion_opportunities,
        },
        "note": "[IMPLEMENTED] [SOFTWARE MODEL] Deterministic experiment results.",
    }

    out_dir = pathlib.Path(EXPERIMENT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "experiment_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print("\n=== Experiment Results [IMPLEMENTED] ===")
    print(f"  Frames:          {N_FRAMES}")
    print(f"  Mean latency:    {results['mean_latency_ms']:.2f} ms")
    print(f"  P95 latency:     {results['p95_latency_ms']:.2f} ms")
    print(f"  Throughput:      {results['throughput_fps']:.1f} fps")
    print(f"  Memory B0:       {results['schedule_summary']['memory_b0']} B  [SW MODEL]")
    print(f"  Fusion ops:      {results['schedule_summary']['fused']}")
    print(f"  Results saved:   {out_path}")


# ---------------------------------------------------------------------------
# Main live webcam loop
# ---------------------------------------------------------------------------

def run_live(
    args: argparse.Namespace,
    engine: AlgebraEngine,
) -> None:
    """Main real-time webcam loop.

    [IMPLEMENTED]
    """
    try:
        import cv2
    except ImportError:
        print("[ERROR] OpenCV (cv2) is required for live mode. Install: pip install opencv-python")
        return

    # Sub-systems
    detector   = HandDetector(
        MEDIAPIPE_MAX_HANDS,
        MEDIAPIPE_MIN_DETECTION_CONF,
        MEDIAPIPE_MIN_TRACKING_CONF,
        MEDIAPIPE_MODEL_COMPLEXITY,
    )
    smoother   = [LandmarkSmoother(LANDMARK_SMOOTHING_ALPHA) for _ in range(2)]
    extractor  = HandGeometryExtractor()
    pose_rec   = StaticPoseRecognizer()
    dyn_rec    = DynamicExpressionRecognizer(TEMPORAL_BUFFER_FRAMES)
    state_mach = ExpressionStateMachine(GESTURE_STABLE_FRAMES, GESTURE_COOLDOWN_FRAMES)
    expr_to_ga = ExpressionToGA(engine, precision=engine.precision)
    vector_view = VectorView3D(480, 480)
    scheduler   = OperationScheduler(precision=engine.precision)

    # Load trained 13-pose classifier if available
    classifier = None
    model_path = "models/static_expression_model.pkl"
    if os.path.exists(model_path):
        try:
            from models.static_expression_classifier import StaticExpressionClassifier
            classifier = StaticExpressionClassifier.load(model_path)
            print(f"[MODEL] Loaded trained 13-pose classifier from {model_path}")
        except Exception as e:
            logger.warning(f"Could not load {model_path}: {e}")

    # Open webcam (or synthetic)
    cap = None
    if not args.no_webcam:
        cap = cv2.VideoCapture(args.camera)
        if not cap.isOpened():
            logger.warning(f"Camera {args.camera} not available. Switching to synthetic mode.")
            cap = None

    # State
    mode_idx       = 0
    use_fix16      = args.fixed
    show_vectors   = True
    frame_idx      = 0
    fps_buf: deque = deque(maxlen=30)
    vec_cache: Optional[np.ndarray] = None
    last_geom      = None
    last_mvs       = None
    last_ga_result = None
    last_ir        = None
    last_pose      = "UNKNOWN"
    last_expression = ""
    last_confidence = 0.0
    recording_frames: List[Dict] = []
    expression_log:   List[Dict] = []
    schedule_cache     = None

    cv2.namedWindow("QGAOPS Hand GA Engine", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("QGAOPS Hand GA Engine", 1600, 720)

    print("\n[LIVE] Starting QGAOPS Hand GA Engine")
    print("  Keyboard: Q=Quit  M=Mode  F=FIX16  G=GP  D=Dot  W=Wedge")
    print("            R=Rotor  S=Sandwich  V=Vectors  H=Help  B=Benchmark")
    if not detector.is_available:
        print("  [WARN] MediaPipe not available — no hand detection.")

    # Phase 5: Gesture Control Layer
    controller = None
    if getattr(args, "control", None):
        prof = "mouse" if args.control == "debug" else args.control
        controller = GestureController(profile_name=prof)
        controller.enable()
        print(f"\n[CONTROL] Computer Vision Gesture Control ENABLED (Profile: {prof.upper()})")
        print("          Press [F12] or [Esc] for Emergency Stop Cut-off")

    t_last = time.perf_counter()

    while True:
        # --- Acquire frame ---
        t_frame_start = time.perf_counter()
        if cap is not None:
            ret, frame = cap.read()
            if not ret:
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
        else:
            # Synthetic: grey noise frame
            frame = np.full((480, 640, 3), 30, dtype=np.uint8)
            cv2.putText(frame, "SYNTHETIC MODE (no webcam)", (40, 240),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (120, 120, 200), 2)

        frame = cv2.flip(frame, 1)  # mirror

        # --- Hand detection ---
        hands = detector.detect(frame)
        annotated = detector.draw_landmarks(frame, hands)

        geom_list = []
        mvs_list  = []
        for i, h in enumerate(hands[:2]):
            lm_raw  = h.to_array()
            lm_sm   = smoother[i].update(lm_raw)
            geom    = extractor.extract(lm_raw, lm_sm, h.confidence, h.handedness, frame_idx)
            mvs_d   = hand_to_multivectors(geom)
            geom_list.append(geom)
            mvs_list.append(mvs_d)

        # Use first hand for GA operations
        if geom_list:
            last_geom = geom_list[0]
            last_mvs  = mvs_list[0]
            dyn_rec.push(last_geom, time.time())

        # --- Gesture recognition ---
        hand_present = len(geom_list) > 0
        if hand_present and last_geom is not None:
            gr = pose_rec.recognize(last_geom)
            if classifier is not None:
                from scripts.extract_features import extract_geometric_features
                geo_feat = extract_geometric_features(last_geom, last_geom.landmarks_raw)
                ml_expr, ml_conf = classifier.predict_single(geo_feat)
                if ml_conf >= 0.65 and gr.confidence >= 0.60 and ml_expr == gr.pose:
                    static_pose = ml_expr
                    static_conf = min(1.0, 0.5 * (ml_conf + gr.confidence) + 0.1)
                elif ml_conf >= 0.70:
                    static_pose = ml_expr
                    static_conf = ml_conf
                elif gr.confidence >= 0.65:
                    static_pose = gr.pose
                    static_conf = gr.confidence
                elif ml_expr != "UNKNOWN" and ml_conf > 0.5:
                    static_pose = ml_expr
                    static_conf = ml_conf
                else:
                    static_pose = gr.pose
                    static_conf = max(gr.confidence, ml_conf)
            else:
                static_pose = gr.pose
                static_conf = gr.confidence
        else:
            static_pose = "UNKNOWN"
            static_conf = 0.0

        # --- Dynamic expression ---
        dyn_result = dyn_rec.recognize()
        # Dynamic priority when motion is present
        if dyn_result.confidence >= 0.70 and dyn_result.expression != "UNKNOWN_DYNAMIC":
            expression = dyn_result.expression
            confidence = dyn_result.confidence
        else:
            expression = static_pose
            confidence = static_conf

        state_event = state_mach.update(hand_present, expression, confidence)
        last_pose       = static_pose
        last_expression = expression
        last_confidence = confidence

        # --- GA computation ---
        if hand_present and last_geom is not None and last_mvs is not None:
            ga_r = expr_to_ga.map(expression, last_geom, last_mvs)
            if ga_r is not None:
                last_ga_result = ga_r.result
                last_ir        = ga_r.ir

        # --- Gesture Control Layer ---
        ctrl_report = None
        if controller is not None:
            ctrl_report = controller.process_frame(
                gesture=expression if hand_present else "UNKNOWN",
                confidence=confidence,
                geom=last_geom,
                detection_latency_ms=0.0,
            )
            if controller.mapper.active_profile_name == "object3d":
                vec_cache = controller.object3d.render(480, 480)

        # --- Record ---
        if args.record and hand_present and last_geom is not None:
            recording_frames.append({
                "frame": frame_idx,
                "timestamp": time.time(),
                "landmarks": last_geom.landmarks_raw.tolist(),
                "pose": last_pose,
                "expression": last_expression,
            })

        # --- 3D vector panel ---
        if show_vectors and frame_idx % VECTOR_3D_UPDATE_EVERY == 0:
            if controller is not None and controller.mapper.active_profile_name == "object3d":
                pass
            else:
                highlight = ["index_vec", "middle_vec"] if last_mvs else []
                wedge_pair = ("index_vec", "middle_vec") if expression == "TWO_FINGER" else None
                vec_cache = vector_view.render(last_geom, last_mvs, highlight, wedge_pair)

        # --- Info panel ---
        fix16_err = getattr(engine, "_last_fix16_error", (0.0, 0.0, 0.0))
        info_panel = make_info_panel(
            480, 720,
            geom=last_geom,
            mvs=last_mvs,
            pose=last_pose,
            expression=last_expression,
            confidence=last_confidence,
            ga_result=last_ga_result,
            last_ir=last_ir,
            ir_trace=engine.ir_trace[-5:] if engine.ir_trace else [],
            ops_per_s=engine.operations_per_second(),
            fix16_error=fix16_err,
            use_fix16=use_fix16,
            backend=engine.backend_name,
            frame_ms=(time.perf_counter() - t_frame_start) * 1000,
            mode_name=MODES[mode_idx],
        )

        # --- Webcam overlay ---
        fps = len(fps_buf) / (sum(fps_buf) + 1e-6) if fps_buf else 0.0
        annotated = draw_webcam_overlay(
            annotated,
            gesture=last_pose,
            expression=last_expression,
            confidence=last_confidence,
            handedness=geom_list[0].handedness if geom_list else "Unknown",
            fps=fps,
            tracking_conf=geom_list[0].confidence if geom_list else 0.0,
            mode_name=MODES[mode_idx],
            use_fix16=use_fix16,
            backend=engine.backend_name,
        )
        if not hand_present:
            annotated = draw_no_hand_message(annotated)

        # Render Computer Vision Control HUD Overlay
        if controller is not None:
            annotated = render_control_hud(
                annotated,
                report=ctrl_report,
                pose=last_pose,
                expression=last_expression,
                confidence=last_confidence,
                hand_detected=hand_present,
                is_control_enabled=controller.is_enabled,
                active_profile=controller.mapper.active_profile_name,
            )

        # --- Assemble dashboard ---
        dashboard = assemble_dashboard(annotated, vec_cache, info_panel, 720)
        cv2.imshow("QGAOPS Hand GA Engine", dashboard)

        # --- FPS ---
        t_now = time.perf_counter()
        fps_buf.append(t_now - t_last)
        t_last = t_now

        # --- Key handling ---
        key = cv2.waitKey(1) & 0xFF
        if key == KEY_QUIT or key == 27:
            break
        elif key in [0, 190, 0x7B]:  # F12 key on various keyboard layouts
            if controller is not None:
                controller.emergency_stop()
                print("\n[SAFETY] EMERGENCY STOP TRIGGERED VIA KEYBOARD (F12)!")
        elif key == KEY_NEXT_MODE:
            mode_idx = (mode_idx + 1) % len(MODES)
        elif key == KEY_FIX16:
            use_fix16 = not use_fix16
            engine.precision = "FIX16" if use_fix16 else "FLOAT32"
            expr_to_ga._precision = engine.precision
            print(f"[KEY] FIX16 mode: {use_fix16}")
        elif key == KEY_BENCHMARK:
            run_benchmark(engine)
        elif key == KEY_VECTORS:
            show_vectors = not show_vectors
            vec_cache = None
        elif key == KEY_HELP:
            print("\n[HELP] Keyboard shortcuts:")
            print("  Q = Quit | M = Next mode | F = Toggle FIX16")
            print("  G = Geometric product | D = Dot product | W = Wedge product")
            print("  R = Rotor | S = Sandwich | V = Toggle 3D view | B = Benchmark")
        elif key == KEY_GP:
            mode_idx = 3  # GEOMETRIC PRODUCT
        elif key == KEY_DOT:
            mode_idx = 1  # DOT PRODUCT
        elif key == KEY_WEDGE:
            mode_idx = 2  # WEDGE PRODUCT
        elif key == KEY_ROTOR:
            mode_idx = 4  # ROTOR
        elif key == KEY_SANDWICH:
            mode_idx = 5  # SANDWICH

        frame_idx += 1

    # Cleanup
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()
    vector_view.close()
    detector.close()

    # Save recording if active
    if args.record and recording_frames:
        recording = {"frames": recording_frames, "total": len(recording_frames)}
        with open(RECORDING_DEFAULT, "w") as f:
            json.dump(recording, f, indent=2)
        print(f"[RECORD] Saved {len(recording_frames)} frames → {RECORDING_DEFAULT}")

    print("\n[QGAOPS] Session ended.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    args = parse_args()

    engine = AlgebraEngine(
        backend=args.backend,
        precision="FIX16" if args.fixed else "FLOAT32",
        trace=True,
    )

    print("=" * 60)
    print("  LIVE HAND GEOMETRIC ALGEBRA ENGINE")
    print("  [SOFTWARE DEMONSTRATOR] QGAOPS-QGPU Golden Model")
    print("=" * 60)
    print(f"  Engine:    {engine}")
    print(f"  Backend:   {engine.backend_name} [IMPLEMENTED]")
    print(f"  Precision: {engine.precision}")
    print(f"  FPGA:      [PROPOSED] [NOT IMPLEMENTED]")
    print()

    if args.gui:
        from gui.dashboard_window import launch_gui
        launch_gui(use_synthetic=args.no_webcam)
    elif args.benchmark:
        run_benchmark(engine)
    elif args.microbenchmark:
        run_microbenchmark(engine)
    elif args.e2e_benchmark:
        run_e2e_benchmark(engine)
    elif args.fixed:
        run_fix16_validation()
        run_live(args, engine)
    elif args.generate_golden:
        run_generate_golden()
    elif args.profile:
        run_profile(engine)
    elif args.replay:
        run_replay(args.replay, engine)
    elif args.experiment:
        run_experiment(engine)
    else:
        run_live(args, engine)


if __name__ == "__main__":
    main()
