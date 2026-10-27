"""
Tests for Performance Tracker, Bandwidth Accounting, and Hardware Metrics Interface.
"""
import os
import time
import pytest

from metrics.hardware_metrics import HardwareMetricsInterface, NOT_AVAILABLE
from metrics.performance_tracker import PerformanceTracker


def test_hardware_metrics_returns_not_available():
    hw = HardwareMetricsInterface()
    assert hw.is_connected is False
    counters = hw.read_counters()
    assert counters.fpga_connected is False
    assert counters.lut == "N/A — FPGA not synthesized"
    assert counters.cycles == NOT_AVAILABLE
    assert counters.power_w == NOT_AVAILABLE


def test_performance_tracker_stages_and_counters():
    tracker = PerformanceTracker(history_seconds=10)

    # Time stages
    tracker.start_stage("camera_acquisition")
    time.sleep(0.002)
    tracker.end_stage("camera_acquisition")

    tracker.start_stage("ga_computation")
    time.sleep(0.001)
    tracker.end_stage("ga_computation")

    # Record operations
    tracker.record_operation("GP")
    tracker.record_operation("WEDGE")
    tracker.record_operation("GP", is_fix16=True)
    assert tracker.counters["GP"] == 2
    assert tracker.counters["WEDGE"] == 1
    assert tracker.counters["FIX16"] == 1
    assert tracker.counters["TOTAL_GA_OPS"] == 3

    # Record data movement
    tracker.record_data_movement(input_bytes=1000000, output_bytes=50000)

    # End frame
    snap = tracker.end_frame(expression="OK", confidence=0.95, backend="PYTHON", precision="FLOAT32")
    assert snap.frame_id == 1
    assert snap.expression == "OK"
    assert snap.confidence == 0.95
    assert snap.memory_model.level == "B5"
    assert snap.memory_model.reuse_ratio_pct > 0.0
    assert snap.memory_model.arithmetic_intensity > 0.0


def test_performance_tracker_export(tmp_path):
    tracker = PerformanceTracker(history_seconds=5)
    for _ in range(5):
        tracker.start_stage("ga_computation")
        time.sleep(0.001)
        tracker.end_stage("ga_computation")
        tracker.record_operation("GP")
        tracker.end_frame(expression="PALM", confidence=0.88)

    export_dir = str(tmp_path / "perf")
    csv_path, json_path = tracker.export_history(export_dir)

    assert os.path.exists(csv_path)
    assert os.path.exists(json_path)
    assert os.path.getsize(csv_path) > 0
    assert os.path.getsize(json_path) > 0
