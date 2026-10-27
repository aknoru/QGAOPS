"""
LIVE HAND GA ENGINE — experiments/run_expression_experiment.py
End-to-end reproducible experiment measuring dataset statistics, detection rate,
classification metrics, inference latency, real-time throughput, GA latency, and FIX16 error.

[IMPLEMENTED] Generates results/experiments/expression_experiment_results.json.
"""
from __future__ import annotations

import json
import os
import sys
import time
from typing import Any, Dict

import numpy as np

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.algebra_engine import AlgebraEngine
from fixed_point.fix16 import fix16_error_analysis
from ga.multivector import Multivector
from models.static_expression_classifier import StaticExpressionClassifier
from train import load_dataset_features, split_data


def run_experiment() -> Dict[str, Any]:
    print("=" * 65)
    print("  QGAOPS HAND-EXPRESSION & GA BENCHMARK EXPERIMENT")
    print("=" * 65)

    os.makedirs("results/experiments", exist_ok=True)

    # 1. Dataset statistics
    audit_report_path = "results/dataset_report.json"
    if os.path.exists(audit_report_path):
        with open(audit_report_path, "r") as f:
            dataset_audit = json.load(f)
    else:
        from scripts.dataset_audit import audit_dataset
        dataset_audit = audit_dataset()

    # 2. Feature extraction / detection success rate
    feat_report_path = "results/feature_extraction_report.json"
    if os.path.exists(feat_report_path):
        with open(feat_report_path, "r") as f:
            feat_report = json.load(f)
    else:
        from scripts.extract_features import process_dataset
        feat_report = process_dataset()

    # 3. Model evaluation
    data = load_dataset_features()
    model_path = "models/static_expression_model.pkl"
    if os.path.exists(model_path):
        clf_lm = StaticExpressionClassifier.load(model_path)
    else:
        from train import run_training
        run_training()
        clf_lm = StaticExpressionClassifier.load(model_path)

    # Evaluate on held-out test split
    X_lm, y_lm = data["X_landmark"], data["y_landmark"]
    _, _, _, _, X_te, y_te = split_data(X_lm, y_lm, seed=42)
    eval_lm = clf_lm.evaluate(X_te, y_te)

    # Image baseline evaluation
    img_model_path = "models/image_baseline_model.pkl"
    eval_im = {}
    if os.path.exists(img_model_path):
        clf_im = StaticExpressionClassifier.load(img_model_path)
        X_im, y_im = data["X_image"], data["y_image"]
        _, _, _, _, X_te_im, y_te_im = split_data(X_im, y_im, seed=42)
        eval_im = clf_im.evaluate(X_te_im, y_te_im)

    # 4. GA operation latency & throughput
    engine = AlgebraEngine(precision="FLOAT32", trace=False)
    v1 = Multivector.vector(0.6, 0.8, 0.0)
    v2 = Multivector.vector(0.3, 0.5, 0.7)

    ga_latencies = {}
    ga_ops = {
        "GP": lambda: engine.gp(v1, v2),
        "WEDGE": lambda: engine.wedge(v1, v2),
        "DOT": lambda: engine.dot(v1, v2),
        "NORM": lambda: engine.norm(v1),
        "DISTANCE": lambda: engine.distance(v1, v2),
    }

    N = 10000
    for op_name, fn in ga_ops.items():
        # warmup
        for _ in range(500):
            fn()
        t0 = time.perf_counter_ns()
        for _ in range(N):
            fn()
        t_tot_ns = time.perf_counter_ns() - t0
        mean_us = (t_tot_ns / N) / 1000.0
        ops_sec = N / (t_tot_ns / 1e9)
        ga_latencies[op_name] = {
            "mean_latency_us": round(mean_us, 3),
            "ops_per_second": round(ops_sec, 1),
        }

    # 5. FIX16 Error Analysis
    from fixed_point.fix16 import Fix16Multivector, fix16_geometric_product
    float_gp = engine.gp(v1, v2)
    fix_v1 = Fix16Multivector.from_multivector(v1)
    fix_v2 = Fix16Multivector.from_multivector(v2)
    fix_gp = fix16_geometric_product(fix_v1, fix_v2)
    max_err, mean_err, rms_err = fix16_error_analysis(float_gp, fix_gp)

    # 6. Combined Report
    results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "dataset_statistics": {
            "total_images": dataset_audit.get("total_images", 1200),
            "classes": list(dataset_audit.get("classes", {}).keys()),
            "corrupted_images": dataset_audit.get("corrupted_count", 0),
        },
        "landmark_detection": {
            "detected_samples": feat_report.get("landmark_samples_extracted", 0),
            "detection_success_rate_pct": feat_report.get("overall_detection_rate_pct", 0.0),
            "detection_failure_rate_pct": feat_report.get("overall_failure_rate_pct", 0.0),
            "by_class": feat_report.get("detection_by_class", {}),
        },
        "landmark_classifier_metrics": {
            "model_type": eval_lm.get("model_type", "random_forest"),
            "accuracy": eval_lm.get("accuracy", 0.0),
            "precision": eval_lm.get("precision", 0.0),
            "recall": eval_lm.get("recall", 0.0),
            "f1": eval_lm.get("f1", 0.0),
            "inference_latency_us": eval_lm.get("inference_latency_us", 0.0),
            "confusion_matrix": eval_lm.get("confusion_matrix", []),
            "target_names": eval_lm.get("target_names", []),
        },
        "image_baseline_metrics": {
            "model_type": eval_im.get("model_type", "random_forest"),
            "accuracy": eval_im.get("accuracy", 0.0),
            "precision": eval_im.get("precision", 0.0),
            "recall": eval_im.get("recall", 0.0),
            "f1": eval_im.get("f1", 0.0),
            "inference_latency_us": eval_im.get("inference_latency_us", 0.0),
        },
        "ga_operation_benchmarks": ga_latencies,
        "fix16_numerical_error": {
            "max_absolute_error": float(max_err),
            "mean_absolute_error": float(mean_err),
            "rms_error": float(rms_err),
        },
        "classification": "[MEASURED SOFTWARE]",
    }

    out_file = "results/experiments/expression_experiment_results.json"
    with open(out_file, "w") as f:
        json.dump(results, f, indent=2)

    print("\nExperiment Summary:")
    print(f"  Landmark Classifier Accuracy: {results['landmark_classifier_metrics']['accuracy']*100:.2f}%")
    print(f"  Image Baseline Accuracy:     {results['image_baseline_metrics']['accuracy']*100:.2f}%")
    print(f"  Landmark Inference Latency:   {results['landmark_classifier_metrics']['inference_latency_us']} µs")
    print(f"  GP Throughput:                {ga_latencies['GP']['ops_per_second']} ops/s")
    print(f"  FIX16 Max Error:              {results['fix16_numerical_error']['max_absolute_error']:.6f}")
    print(f"\n[SAVED] Full experiment results written to {out_file}")

    return results


if __name__ == "__main__":
    run_experiment()
