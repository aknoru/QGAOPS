"""
QGAOPS-QGPU: Unified Entry Point
main.py

[SOFTWARE DEMONSTRATOR] Research Golden Model & GUI for QGAOPS-QGPU.

Modes:
    python main.py                   # Live webcam tracking demo
    python main.py --no-webcam       # Synthetic demo mode (no camera needed)
    python main.py --gui             # Launch full PySide6 Unified Engineering Dashboard
    python main.py --standalone-gui  # Launch standalone Hand GA Engine Console
    python main.py --benchmark       # Run GA operations benchmark
    python main.py --microbenchmark  # Run high-resolution 50,000-op microbenchmark
    python main.py --e2e-benchmark   # Run end-to-end pipeline benchmark
    python main.py --fixed           # Run FIX16 / Q16.16 mode
    python main.py --generate-golden # Generate RTL golden test vectors
    python main.py --profile         # Profile per-stage latency
    python main.py --record          # Record landmarks to JSON
    python main.py --replay FILE     # Replay landmarks from JSON file
    python main.py --experiment      # Run deterministic experiment
    python main.py --control mouse   # Computer vision gesture control (mouse)
    python main.py --control presentation # Presentation slideshow control
    python main.py --control object3d     # GA rotor 3D virtual object manipulation
"""
from __future__ import annotations

import argparse
import os
import pathlib
import sys

_HERE = pathlib.Path(__file__).resolve().parent
_HAND_GA_DIR = _HERE / "hand_ga_engine"

for p in [str(_HERE), str(_HAND_GA_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="QGAOPS-QGPU Master Demonstrator & Benchmark Suite"
    )
    p.add_argument("--gui",             action="store_true", help="Launch PySide6 unified engineering dashboard")
    p.add_argument("--standalone-gui",  action="store_true", help="Launch standalone Hand GA Engine dashboard")
    p.add_argument("--benchmark",       action="store_true", help="Run standard GA benchmark (10k ops)")
    p.add_argument("--microbenchmark",  action="store_true", help="Run high-resolution GA microbenchmark (50k ops)")
    p.add_argument("--e2e-benchmark",   action="store_true", help="Run end-to-end pipeline benchmark")
    p.add_argument("--fixed",           action="store_true", help="Enable FIX16 / Q16.16 mode")
    p.add_argument("--generate-golden", action="store_true", help="Generate golden vectors for hardware verification")
    p.add_argument("--profile",         action="store_true", help="Profile pipeline performance waterfall")
    p.add_argument("--record",          action="store_true", help="Record hand landmarks to file")
    p.add_argument("--replay",          type=str, default=None, help="Replay hand landmarks from JSON file")
    p.add_argument("--experiment",      action="store_true", help="Run deterministic experiment on Kaggle dataset")
    p.add_argument("--no-webcam",       action="store_true", help="Disable webcam (use synthetic demo mode)")
    p.add_argument(
        "--control",
        type=str,
        choices=["mouse", "presentation", "media", "object3d", "debug"],
        default=None,
        help="Enable computer vision gesture control with specified profile",
    )
    p.add_argument("--camera",          type=int, default=0, help="Webcam device index")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    if args.gui:
        from software.gui.qgpu_dashboard import main as gui_main
        gui_main()
        return

    if args.standalone_gui:
        from hand_ga_engine.gui.dashboard_window import launch_gui
        launch_gui(use_synthetic=args.no_webcam)
        return

    # Forward CLI commands directly to hand_ga_engine runner
    import hand_ga_engine.main as hga_main
    sys.argv = [sys.argv[0]] + sys.argv[1:]
    hga_main.main()


if __name__ == "__main__":
    main()
