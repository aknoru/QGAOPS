"""Small fixture-based gesture pipeline; camera support is intentionally absent."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


@dataclass(frozen=True)
class GestureSample:
    label: str
    landmarks: tuple[tuple[float, float, float], ...]


def load_fixture(path: Path) -> list[GestureSample]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("gesture fixture must be a list")
    samples = []
    for item in data:
        if not isinstance(item, dict) or not isinstance(item.get("label"), str):
            raise ValueError("each gesture sample needs a string label")
        points = item.get("landmarks")
        if not isinstance(points, list) or not points:
            raise ValueError("each gesture sample needs non-empty landmarks")
        parsed = []
        for point in points:
            if not isinstance(point, list) or len(point) != 3:
                raise ValueError("each landmark must contain exactly three coordinates")
            parsed.append(tuple(float(value) for value in point))
        samples.append(GestureSample(item["label"], tuple(parsed)))
    return samples


def features(sample: GestureSample) -> tuple[float, ...]:
    origin = sample.landmarks[0]
    return tuple(value - origin[coordinate] for point in sample.landmarks for coordinate, value in enumerate(point))


def nearest_centroid(samples: Sequence[GestureSample]) -> dict:
    if len(samples) < 2:
        raise ValueError("at least two samples are required")
    labels = sorted({sample.label for sample in samples})
    centroids = {}
    for label in labels:
        vectors = [features(sample) for sample in samples if sample.label == label]
        if not vectors:
            continue
        centroids[label] = tuple(sum(vector[i] for vector in vectors) / len(vectors) for i in range(len(vectors[0])))
    correct = 0
    predictions = []
    for sample in samples:
        vector = features(sample)
        label = min(centroids, key=lambda candidate: sum((a - b) ** 2 for a, b in zip(vector, centroids[candidate])))
        correct += label == sample.label
        predictions.append({"expected": sample.label, "predicted": label})
    accuracy = correct / len(samples)
    return {"schema_version": "1", "sample_count": len(samples), "labels": labels,
            "accuracy": accuracy, "predictions": predictions, "classifier": "nearest_centroid_fixture"}
