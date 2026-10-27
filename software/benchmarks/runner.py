"""Small standard-library benchmark runner with explicit measurement boundaries."""

from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path

from software.reference_model.qgaops_reference import FixedPointMultivector
from .workloads import WorkloadConfig, execute_pair, generate_pairs


def _fixed(value):
    return FixedPointMultivector.from_reals(value.coefficients)


def run(config: WorkloadConfig, repetitions: int = 5, warmup: int = 1) -> dict:
    if repetitions < 1 or warmup < 0:
        raise ValueError("repetitions must be positive and warmup non-negative")
    pairs = generate_pairs(config)
    fixed_pairs = [(_fixed(left), _fixed(right)) for left, right in pairs]
    operation = config.operation
    for _ in range(warmup):
        for left, right in pairs:
            execute_pair(operation, left, right)
    samples = []
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        for left, right in pairs:
            execute_pair(operation, left, right)
        samples.append((time.perf_counter_ns() - start) / 1e9)
    fixed_samples = []
    for _ in range(repetitions):
        start = time.perf_counter_ns()
        for left, right in fixed_pairs:
            if operation == "add":
                left + right
            elif operation == "subtract":
                left - right
            else:
                getattr(left, operation)(right)
        fixed_samples.append((time.perf_counter_ns() - start) / 1e9)

    def summary(values):
        ordered = sorted(values)
        return {
            "samples_seconds": values,
            "mean_seconds": statistics.mean(values),
            "median_seconds": statistics.median(values),
            "stdev_seconds": statistics.stdev(values) if len(values) > 1 else 0.0,
            "p95_seconds": ordered[min(len(ordered) - 1, int(len(ordered) * 0.95))],
            "operations_per_second_median": config.count / statistics.median(values),
        }

    return {
        "schema_version": "1",
        "config": config.as_dict(),
        "measurement_boundary": "Python reference operation batch only; conversion excluded",
        "environment": {"python": sys.version, "platform": platform.platform()},
        "floating_point": summary(samples),
        "fixed_point": summary(fixed_samples),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def write_result(result: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
