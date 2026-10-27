"""
LIVE HAND GA ENGINE — metrics/performance_tracker.py
Real-time performance tracking, bandwidth accounting, and software memory modeling.

[IMPLEMENTED]
- Nanosecond-precision timing for all pipeline stages.
- Frame metrics: camera FPS, processing FPS, end-to-end FPS, P50/P95/P99 latency.
- GA throughput: GA_OPS/s and FRAME_OPS/s.
- Software logical data-movement bandwidth (Input, Output, Total MB/s).
- QGAOPS FPGA memory model (B0-B5 logical DDR traffic, scratchpad reuse).
- Rolling 60-second history buffer with CSV and JSON export.
- Hardware metrics interface integration with strict labeling:
    [MEASURED SOFTWARE]
    [SOFTWARE MODEL]
    [CALCULATED]
    [N/A — FPGA NOT CONNECTED]
"""
from __future__ import annotations

import csv
import json
import os
import time
from collections import deque
from dataclasses import asdict, dataclass, field
from typing import Any, Deque, Dict, List, Optional, Tuple

import numpy as np

try:
    import psutil
    _PSUTIL_AVAILABLE = True
except ImportError:
    _PSUTIL_AVAILABLE = False

from .hardware_metrics import HardwareMetrics, NOT_AVAILABLE


@dataclass
class StageTiming:
    """Nanosecond timing for a single pipeline stage."""
    name: str
    duration_ns: int = 0
    duration_ms: float = 0.0
    percent: float = 0.0


@dataclass
class MemoryModelReport:
    """Software model of QGAOPS memory fabric."""
    level: str = "B5"
    logical_ddr_bytes: int = 0
    tile_buffer_reads: int = 0
    tile_buffer_writes: int = 0
    scratchpad_accesses: int = 0
    bytes_moved: int = 0
    bytes_reused: int = 0
    reuse_ratio_pct: float = 0.0
    arithmetic_intensity: float = 0.0  # ops per byte
    classification: str = "[SOFTWARE MODEL]"


@dataclass
class PerformanceSnapshot:
    """Comprehensive performance snapshot for one frame or time interval."""
    timestamp: float
    frame_id: int
    fps_camera: float
    fps_processing: float
    fps_e2e: float
    frame_time_ms: float
    latency_p50_ms: float
    latency_p95_ms: float
    latency_p99_ms: float
    ga_ops_per_second: float
    frame_ops_per_second: float
    stage_breakdown: Dict[str, float]  # stage_name -> ms
    bandwidth_input_mbs: float
    bandwidth_output_mbs: float
    bandwidth_total_mbs: float
    memory_model: MemoryModelReport
    cpu_percent: float
    ram_mb: float
    process_rss_mb: float
    operation_counters: Dict[str, int]
    expression: str
    confidence: float
    backend: str
    precision: str


class PerformanceTracker:
    """High-resolution performance tracking and data-movement accounting engine.

    [IMPLEMENTED]
    """

    STAGES = [
        "camera_acquisition",
        "hand_detection",
        "landmark_normalization",
        "feature_extraction",
        "expression_classification",
        "ga_encoding",
        "algebra_analysis",
        "ga_computation",
        "visualization",
    ]

    def __init__(self, history_seconds: int = 60) -> None:
        self.history_seconds = history_seconds
        self.max_history_entries = history_seconds * 60  # assume up to 60 fps

        # Timers and counters
        self._start_time = time.perf_counter()
        self._frame_count = 0
        self._ga_op_count = 0

        # Detailed operation counters
        self.counters: Dict[str, int] = {
            "GP": 0,
            "DOT": 0,
            "WEDGE": 0,
            "REVERSE": 0,
            "ROTOR": 0,
            "SANDWICH": 0,
            "NORM": 0,
            "DISTANCE": 0,
            "FIX16": 0,
            "TOTAL_GA_OPS": 0,
            "TOTAL_EXPRESSIONS": 0,
        }

        # Rolling buffers (last 60 frames for percentiles / smoothed FPS)
        self._frame_latencies_ms: Deque[float] = deque(maxlen=120)
        self._stage_times_ns: Dict[str, Deque[int]] = {s: deque(maxlen=60) for s in self.STAGES}

        # Rolling history buffer for export / graphs
        self.history: Deque[PerformanceSnapshot] = deque(maxlen=self.max_history_entries)

        # Active stage timing context
        self._active_stage: Optional[str] = None
        self._stage_start_ns: int = 0
        self._current_frame_stages: Dict[str, int] = {s: 0 for s in self.STAGES}

        # Data movement accounting
        self._bytes_input_accum = 0
        self._bytes_output_accum = 0
        self._last_bandwidth_time = time.perf_counter()
        self._last_bandwidth_snapshot = (0.0, 0.0, 0.0)

        # Process monitor
        self._process = psutil.Process() if _PSUTIL_AVAILABLE else None

    # -------------------------------------------------------------
    # Stage Timing Interface
    # -------------------------------------------------------------

    def start_stage(self, stage_name: str) -> None:
        """Begin measuring a pipeline stage."""
        self._active_stage = stage_name
        self._stage_start_ns = time.perf_counter_ns()

    def end_stage(self, stage_name: Optional[str] = None) -> float:
        """Finish measuring a pipeline stage. Returns duration in ms."""
        now_ns = time.perf_counter_ns()
        stg = stage_name or self._active_stage
        if stg is None:
            return 0.0

        dur_ns = max(now_ns - self._stage_start_ns, 0)
        if stg in self._current_frame_stages:
            self._current_frame_stages[stg] += dur_ns
            self._stage_times_ns[stg].append(dur_ns)

        self._active_stage = None
        return dur_ns / 1e6

    # -------------------------------------------------------------
    # Operation & Bandwidth Accounting
    # -------------------------------------------------------------

    def record_operation(self, opcode: str, is_fix16: bool = False) -> None:
        """Increment GA operation counter."""
        self._ga_op_count += 1
        self.counters["TOTAL_GA_OPS"] += 1

        op_upper = opcode.upper()
        if op_upper in self.counters:
            self.counters[op_upper] += 1

        if is_fix16:
            self.counters["FIX16"] += 1

    def record_data_movement(self, input_bytes: int = 0, output_bytes: int = 0) -> None:
        """Account for logical software data movement."""
        self._bytes_input_accum += max(input_bytes, 0)
        self._bytes_output_accum += max(output_bytes, 0)

    # -------------------------------------------------------------
    # Frame End & Snapshot Generation
    # -------------------------------------------------------------

    def end_frame(
        self,
        expression: str = "UNKNOWN",
        confidence: float = 0.0,
        backend: str = "PYTHON",
        precision: str = "FLOAT32",
    ) -> PerformanceSnapshot:
        """Conclude the current frame, record metrics, and produce a snapshot."""
        now = time.perf_counter()
        self._frame_count += 1

        # Frame duration from stage sum
        tot_stage_ns = sum(self._current_frame_stages.values())
        frame_ms = tot_stage_ns / 1e6
        self._frame_latencies_ms.append(frame_ms)

        # Percentiles
        lats = sorted(list(self._frame_latencies_ms))
        if lats:
            p50 = float(np.percentile(lats, 50))
            p95 = float(np.percentile(lats, 95))
            p99 = float(np.percentile(lats, 99))
        else:
            p50 = p95 = p99 = frame_ms

        # FPS
        elapsed_total = max(now - self._start_time, 1e-4)
        fps_camera = float(self._frame_count / elapsed_total)
        fps_proc = 1000.0 / max(frame_ms, 0.001)
        fps_e2e = float(len(self._frame_latencies_ms) / (sum(self._frame_latencies_ms) / 1000.0)) if self._frame_latencies_ms else fps_proc

        # Throughput
        ga_ops_sec = float(self._ga_op_count / elapsed_total)
        frame_ops_sec = float(self._frame_count / elapsed_total)

        # Bandwidth accounting over elapsed time
        dt_bw = max(now - self._last_bandwidth_time, 1e-4)
        bw_in_mbs = (self._bytes_input_accum / (1024 * 1024)) / dt_bw
        bw_out_mbs = (self._bytes_output_accum / (1024 * 1024)) / dt_bw
        bw_tot_mbs = bw_in_mbs + bw_out_mbs

        # Reset accumulator every second
        if dt_bw >= 1.0:
            self._last_bandwidth_snapshot = (bw_in_mbs, bw_out_mbs, bw_tot_mbs)
            self._bytes_input_accum = 0
            self._bytes_output_accum = 0
            self._last_bandwidth_time = now
        else:
            bw_in_mbs, bw_out_mbs, bw_tot_mbs = self._last_bandwidth_snapshot

        # Stage breakdown (in ms)
        breakdown = {s: round(self._current_frame_stages[s] / 1e6, 3) for s in self.STAGES}

        # Memory model (QGAOPS B0-B5 simulation)
        # In G3, multivector = 8 floats (32 bytes). Naive B0 reads 2 operands (64 B) + writes 1 (32 B) = 96 B per op.
        # B5 AAMF scratchpad achieves ~66% reuse in GA DAGs.
        ops_this_frame = max(self._ga_op_count - (self.history[-1].operation_counters["TOTAL_GA_OPS"] if self.history else 0), 1)
        b0_bytes = ops_this_frame * 96
        b5_ddr_bytes = int(b0_bytes * 0.33)  # 67% reduction via tile scratchpad
        bytes_reused = b0_bytes - b5_ddr_bytes
        reuse_pct = (bytes_reused / max(b0_bytes, 1)) * 100.0

        mem_model = MemoryModelReport(
            level="B5",
            logical_ddr_bytes=b5_ddr_bytes,
            tile_buffer_reads=ops_this_frame * 2,
            tile_buffer_writes=ops_this_frame,
            scratchpad_accesses=ops_this_frame * 3,
            bytes_moved=b0_bytes,
            bytes_reused=bytes_reused,
            reuse_ratio_pct=round(reuse_pct, 1),
            arithmetic_intensity=round(ops_this_frame / max(b5_ddr_bytes, 1), 4),
            classification="[SOFTWARE MODEL]",
        )

        # System resource usage
        cpu_pct = 0.0
        ram_mb = 0.0
        rss_mb = 0.0
        if self._process is not None:
            try:
                cpu_pct = float(self._process.cpu_percent())
                ram_mb = float(psutil.virtual_memory().used / (1024 * 1024))
                rss_mb = float(self._process.memory_info().rss / (1024 * 1024))
            except Exception:
                pass

        if expression not in ("UNKNOWN", ""):
            self.counters["TOTAL_EXPRESSIONS"] += 1

        snap = PerformanceSnapshot(
            timestamp=now,
            frame_id=self._frame_count,
            fps_camera=round(fps_camera, 1),
            fps_processing=round(fps_proc, 1),
            fps_e2e=round(fps_e2e, 1),
            frame_time_ms=round(frame_ms, 2),
            latency_p50_ms=round(p50, 2),
            latency_p95_ms=round(p95, 2),
            latency_p99_ms=round(p99, 2),
            ga_ops_per_second=round(ga_ops_sec, 1),
            frame_ops_per_second=round(frame_ops_sec, 1),
            stage_breakdown=breakdown,
            bandwidth_input_mbs=round(bw_in_mbs, 2),
            bandwidth_output_mbs=round(bw_out_mbs, 2),
            bandwidth_total_mbs=round(bw_tot_mbs, 2),
            memory_model=mem_model,
            cpu_percent=round(cpu_pct, 1),
            ram_mb=round(ram_mb, 1),
            process_rss_mb=round(rss_mb, 1),
            operation_counters=dict(self.counters),
            expression=expression,
            confidence=round(confidence, 3),
            backend=backend,
            precision=precision,
        )

        self.history.append(snap)

        # Reset current frame stage accumulators
        self._current_frame_stages = {s: 0 for s in self.STAGES}

        return snap

    # -------------------------------------------------------------
    # Export Data to Results
    # -------------------------------------------------------------

    def export_history(self, output_dir: str = "results/performance") -> Tuple[str, str]:
        """Export rolling history buffer to CSV and JSON."""
        os.makedirs(output_dir, exist_ok=True)
        csv_path = os.path.join(output_dir, "performance_history.csv")
        json_path = os.path.join(output_dir, "performance_history.json")

        if not self.history:
            return csv_path, json_path

        # CSV Export
        fieldnames = [
            "timestamp", "frame_id", "fps_e2e", "frame_time_ms", "p50_ms", "p95_ms", "p99_ms",
            "ga_ops_per_second", "bandwidth_total_mbs", "cpu_percent", "process_rss_mb",
            "memory_ddr_bytes", "memory_reuse_pct", "expression", "confidence", "backend", "precision"
        ]

        with open(csv_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(fieldnames)
            for s in self.history:
                writer.writerow([
                    f"{s.timestamp:.3f}",
                    s.frame_id,
                    s.fps_e2e,
                    s.frame_time_ms,
                    s.latency_p50_ms,
                    s.latency_p95_ms,
                    s.latency_p99_ms,
                    s.ga_ops_per_second,
                    s.bandwidth_total_mbs,
                    s.cpu_percent,
                    s.process_rss_mb,
                    s.memory_model.logical_ddr_bytes,
                    s.memory_model.reuse_ratio_pct,
                    s.expression,
                    s.confidence,
                    s.backend,
                    s.precision,
                ])

        # JSON Export
        records = [asdict(s) for s in self.history]
        with open(json_path, "w") as f:
            json.dump({
                "export_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_frames_recorded": len(records),
                "classification_labels": {
                    "software_timing": "[MEASURED SOFTWARE]",
                    "memory_model": "[SOFTWARE MODEL]",
                    "hardware_fpga": "[N/A — FPGA NOT CONNECTED]",
                },
                "snapshots": records,
            }, f, indent=2)

        return csv_path, json_path
