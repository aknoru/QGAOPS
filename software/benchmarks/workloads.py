"""Versioned, deterministic workload generation for software baselines."""

from __future__ import annotations

from dataclasses import dataclass, asdict
import random
from typing import Iterable

from software.reference_model.qgaops_reference import Multivector

WORKLOAD_VERSION = "1"


@dataclass(frozen=True)
class WorkloadConfig:
    operation: str = "geometric_product"
    count: int = 16
    seed: int = 20261026
    distribution: str = "dense"
    coefficient_limit: int = 2

    def as_dict(self) -> dict:
        return {"version": WORKLOAD_VERSION, **asdict(self)}


def _validate(config: WorkloadConfig) -> None:
    if config.count < 1:
        raise ValueError("count must be positive")
    if config.coefficient_limit < 0:
        raise ValueError("coefficient_limit must not be negative")
    if config.distribution not in {"scalar", "basis", "sparse", "dense", "boundary"}:
        raise ValueError("unsupported workload distribution")
    if config.operation not in {
        "geometric_product", "wedge", "hestenes_inner", "add", "subtract"
    }:
        raise ValueError("unsupported workload operation")


def _vector(rng: random.Random, config: WorkloadConfig) -> Multivector:
    if config.distribution == "scalar":
        return Multivector.from_coefficients([rng.randint(-config.coefficient_limit, config.coefficient_limit)] + [0] * 7)
    if config.distribution == "basis":
        index = rng.randrange(8)
        return Multivector.from_coefficients([1 if i == index else 0 for i in range(8)])
    if config.distribution == "boundary":
        limit = max(1, config.coefficient_limit)
        values = [limit if i % 2 == 0 else -limit for i in range(8)]
        return Multivector.from_coefficients(values)
    values = [
        rng.randint(-config.coefficient_limit, config.coefficient_limit)
        if config.distribution == "dense" or rng.random() < 0.35 else 0
        for _ in range(8)
    ]
    return Multivector.from_coefficients(values)


def generate_pairs(config: WorkloadConfig) -> list[tuple[Multivector, Multivector]]:
    _validate(config)
    rng = random.Random(config.seed)
    return [(_vector(rng, config), _vector(rng, config)) for _ in range(config.count)]


def execute_pair(operation: str, left: Multivector, right: Multivector) -> Multivector:
    if operation == "add":
        return left + right
    if operation == "subtract":
        return left - right
    return getattr(left, operation)(right)


def workload_record(config: WorkloadConfig) -> dict:
    return {"config": config.as_dict(), "pairs": [
        {"left": left.coefficients, "right": right.coefficients}
        for left, right in generate_pairs(config)
    ]}
