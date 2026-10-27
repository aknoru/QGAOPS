"""
LIVE HAND GA ENGINE — scripts/train_13pose_model.py
Procedural generation and training of 13-class static hand pose model.

[IMPLEMENTED] Generates diverse, physically consistent hand landmark geometries
for all 13 static poses, extracts 107D geometric features, and trains
a high-accuracy Random Forest classifier saved to models/static_expression_model.pkl.
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
from typing import Dict, List, Tuple

import numpy as np
from sklearn.model_selection import StratifiedKFold

# Ensure project root in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hand_detection.landmarks import HandGeometryExtractor, HandGeometry
from mapping.expression_classes import (
    STATIC_POSES,
    STATIC_13_NAMES,
    STATIC_NAME_TO_ID,
    NUM_STATIC_CLASSES,
)
from models.static_expression_classifier import StaticExpressionClassifier
from scripts.extract_features import extract_geometric_features


def _rotation_matrix(rx: float, ry: float, rz: float) -> np.ndarray:
    """Construct 3D rotation matrix from Euler angles (radians)."""
    cx, sx = np.cos(rx), np.sin(rx)
    cy, sy = np.cos(ry), np.sin(ry)
    cz, sz = np.cos(rz), np.sin(rz)

    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def generate_pose_landmarks(
    pose_name: str,
    noise_sigma: float = 0.005,
    rng: np.random.RandomState = None,
) -> np.ndarray:
    """Generate 21 landmarks (x, y, z) for a given static hand pose with physical kinematics."""
    if rng is None:
        rng = np.random.RandomState()

    wrist = np.array([0.5, 0.7, 0.0], dtype=np.float32)

    # MCP base points relative to wrist
    mcp_rel = {
        "thumb":  np.array([-0.06, -0.06, 0.0], dtype=np.float32),
        "index":  np.array([-0.04, -0.16, 0.0], dtype=np.float32),
        "middle": np.array([0.00,  -0.18, 0.0], dtype=np.float32),
        "ring":   np.array([0.04,  -0.16, 0.0], dtype=np.float32),
        "pinky":  np.array([0.08,  -0.13, 0.0], dtype=np.float32),
    }

    # Segment lengths for each digit (3 segments for fingers: MCP->PIP->DIP->TIP)
    seg_lens = {
        "thumb":  [0.04, 0.035, 0.035],
        "index":  [0.045, 0.035, 0.028],
        "middle": [0.050, 0.038, 0.030],
        "ring":   [0.045, 0.035, 0.028],
        "pinky":  [0.035, 0.026, 0.022],
    }

    # Base extension vectors (pointing up in -y by default, thumb outward)
    base_dirs = {
        "thumb":  np.array([-0.7, -0.7, 0.0], dtype=np.float32),
        "index":  np.array([-0.1, -1.0, 0.0], dtype=np.float32),
        "middle": np.array([0.0,  -1.0, 0.0], dtype=np.float32),
        "ring":   np.array([0.1,  -1.0, 0.0], dtype=np.float32),
        "pinky":  np.array([0.2,  -1.0, 0.0], dtype=np.float32),
    }

    # Normalize base dirs
    for k in base_dirs:
        base_dirs[k] = base_dirs[k] / np.linalg.norm(base_dirs[k])

    # Extension states per pose (True = extended, False = curled)
    # Pose specific overrides can modify directions or curl
    ext = {
        "OPEN_PALM":   {"thumb": True,  "index": True,  "middle": True,  "ring": True,  "pinky": True},
        "FIST":        {"thumb": False, "index": False, "middle": False, "ring": False, "pinky": False},
        "THUMBS_UP":   {"thumb": True,  "index": False, "middle": False, "ring": False, "pinky": False},
        "THUMBS_DOWN": {"thumb": True,  "index": False, "middle": False, "ring": False, "pinky": False},
        "INDEX_POINT": {"thumb": False, "index": True,  "middle": False, "ring": False, "pinky": False},
        "TWO_FINGER":  {"thumb": False, "index": True,  "middle": True,  "ring": False, "pinky": False},
        "PEACE_SIGN":  {"thumb": False, "index": True,  "middle": True,  "ring": False, "pinky": False},
        "THREE_FINGER":{"thumb": False, "index": True,  "middle": True,  "ring": True,  "pinky": False},
        "FOUR_FINGER": {"thumb": False, "index": True,  "middle": True,  "ring": True,  "pinky": True},
        "PINCH":       {"thumb": True,  "index": True,  "middle": False, "ring": False, "pinky": False},
        "OK_SIGN":     {"thumb": True,  "index": True,  "middle": True,  "ring": True,  "pinky": True},
        "ROCK_SIGN":   {"thumb": False, "index": True,  "middle": False, "ring": False, "pinky": True},
        "CALL_ME":     {"thumb": True,  "index": False, "middle": False, "ring": False, "pinky": True},
    }[pose_name]

    # Direction overrides
    dirs = {k: v.copy() for k, v in base_dirs.items()}

    if pose_name == "THUMBS_UP":
        dirs["thumb"] = np.array([0.0, -1.0, 0.0], dtype=np.float32)  # directly up
    elif pose_name == "THUMBS_DOWN":
        dirs["thumb"] = np.array([0.0, 1.0, 0.0], dtype=np.float32)   # directly down
    elif pose_name == "TWO_FINGER":
        # Parallel index and middle
        dirs["index"]  = np.array([-0.02, -1.0, 0.0], dtype=np.float32)
        dirs["middle"] = np.array([ 0.02, -1.0, 0.0], dtype=np.float32)
    elif pose_name == "PEACE_SIGN":
        # Spread apart index and middle (> 30 deg)
        dirs["index"]  = np.array([-0.35, -0.94, 0.0], dtype=np.float32)
        dirs["middle"] = np.array([ 0.35, -0.94, 0.0], dtype=np.float32)
    elif pose_name == "ROCK_SIGN":
        # Spread index and pinky
        dirs["index"] = np.array([-0.2, -0.98, 0.0], dtype=np.float32)
        dirs["pinky"] = np.array([ 0.3, -0.95, 0.0], dtype=np.float32)
    elif pose_name == "CALL_ME":
        # Thumb left-up, pinky right-down
        dirs["thumb"] = np.array([-0.9, -0.4, 0.0], dtype=np.float32)
        dirs["pinky"] = np.array([ 0.9,  0.4, 0.0], dtype=np.float32)

    for k in dirs:
        dirs[k] = dirs[k] / np.linalg.norm(dirs[k])

    lms = np.zeros((21, 3), dtype=np.float32)
    lms[0] = wrist

    # Thumb landmarks: 1=CMC, 2=MCP, 3=IP, 4=TIP
    thumb_base = wrist + mcp_rel["thumb"]
    lms[1] = wrist + mcp_rel["thumb"] * 0.5
    lms[2] = thumb_base

    # Build fingers
    finger_indices = {
        "thumb":  [2, 3, 4],
        "index":  [5, 6, 7, 8],
        "middle": [9, 10, 11, 12],
        "ring":   [13, 14, 15, 16],
        "pinky":  [17, 18, 19, 20],
    }

    # Set MCPs
    for f in ["index", "middle", "ring", "pinky"]:
        lms[finger_indices[f][0]] = wrist + mcp_rel[f]

    # Extrude digits
    for f, indices in finger_indices.items():
        is_ext = ext[f]
        d = dirs[f]
        cur_pos = lms[indices[0]].copy()
        lens = seg_lens[f]

        if is_ext:
            # Straight segments with subtle natural curve
            for i, idx in enumerate(indices[1:]):
                seg_d = d + rng.normal(0, 0.02, size=3).astype(np.float32)
                seg_d /= np.linalg.norm(seg_d)
                cur_pos = cur_pos + seg_d * lens[i]
                lms[idx] = cur_pos
        else:
            # Curled towards palm center (inward + positive z)
            palm_vec = (wrist - cur_pos)
            palm_vec /= (np.linalg.norm(palm_vec) + 1e-6)
            for i, idx in enumerate(indices[1:]):
                curl_d = 0.5 * palm_vec + np.array([0.0, 0.0, 0.4], dtype=np.float32)
                curl_d /= np.linalg.norm(curl_d)
                cur_pos = cur_pos + curl_d * (lens[i] * 0.75)
                lms[idx] = cur_pos

    # Special adjustments for PINCH and OK_SIGN: thumb tip touches index tip
    if pose_name in ("PINCH", "OK_SIGN"):
        touch_point = lms[8] + np.array([0.005, 0.005, 0.0], dtype=np.float32)
        lms[4] = touch_point + rng.normal(0, 0.004, size=3).astype(np.float32)

    # Apply global 3D rotation, scaling, and translation noise
    rx = rng.uniform(-0.35, 0.35)
    ry = rng.uniform(-0.35, 0.35)
    rz = rng.uniform(-0.35, 0.35)
    R = _rotation_matrix(rx, ry, rz).astype(np.float32)

    scale = rng.uniform(0.75, 1.25)
    shift = rng.uniform(-0.06, 0.06, size=(1, 3)).astype(np.float32)

    center = lms[0:1].copy()
    lms = ((lms - center) @ R.T) * scale + center + shift

    # Sensor jitter
    lms += rng.normal(0, noise_sigma, size=lms.shape).astype(np.float32)

    return lms


def generate_dataset(
    samples_per_class: int = 250,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray]:
    """Generate normalized geometric feature dataset across all 13 static poses."""
    rng = np.random.RandomState(random_state)
    extractor = HandGeometryExtractor()

    X_list: List[np.ndarray] = []
    y_list: List[int] = []

    print(f"Generating synthetic geometry dataset for {NUM_STATIC_CLASSES} static hand poses...")

    for class_id, pose_meta in STATIC_POSES.items():
        pose_name = pose_meta.name
        print(f"  Class {class_id:2d}: {pose_name:<14} ({samples_per_class} samples)")
        for s in range(samples_per_class):
            lms = generate_pose_landmarks(pose_name, noise_sigma=0.004, rng=rng)
            geom = extractor.extract(lms, lms, confidence=0.95, handedness="Right", frame_index=s)
            feat = extract_geometric_features(geom, lms)
            X_list.append(feat)
            y_list.append(class_id)

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int64)
    print(f"Dataset generated: X shape {X.shape}, y shape {y.shape}")
    return X, y


def train_and_save_model(
    output_path: str = "models/static_expression_model.pkl",
    samples_per_class: int = 250,
    random_state: int = 42,
) -> StaticExpressionClassifier:
    """Train Random Forest classifier on all 13 poses, cross-validate, and save model."""
    X, y = generate_dataset(samples_per_class=samples_per_class, random_state=random_state)

    # 5-fold cross-validation
    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)
    fold_accs = []
    for fold, (train_idx, val_idx) in enumerate(skf.split(X, y)):
        clf_fold = StaticExpressionClassifier(
            model_type="random_forest",
            confidence_threshold=0.60,
            random_state=random_state + fold,
            class_names=STATIC_13_NAMES,
        )
        clf_fold.fit(X[train_idx], y[train_idx])
        ev = clf_fold.evaluate(X[val_idx], y[val_idx], class_names=STATIC_13_NAMES)
        fold_accs.append(ev["accuracy"])

    mean_acc = float(np.mean(fold_accs))
    print(f"\n5-Fold Cross-Validation Accuracy: {mean_acc:.4f} (folds: {[round(a, 4) for a in fold_accs]})")

    # Fit final model on all data
    final_clf = StaticExpressionClassifier(
        model_type="random_forest",
        confidence_threshold=0.60,
        random_state=random_state,
        class_names=STATIC_13_NAMES,
    )
    final_clf.fit(X, y)

    # Evaluate full set
    eval_res = final_clf.evaluate(X, y, class_names=STATIC_13_NAMES)
    print(f"Final Model Overall Accuracy: {eval_res['accuracy']:.4f}, F1: {eval_res['f1']:.4f}")
    print(f"Mean Single-Frame Inference Latency: {eval_res['inference_latency_us']:.2f} µs")
    print("\nClassification Report:\n" + eval_res["classification_report"])

    # Save model
    out_file = pathlib.Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    final_clf.save(str(out_file))
    print(f"\n[SUCCESS] 13-Pose Model saved successfully to: {out_file.resolve()}")

    # Save summary report
    report_path = pathlib.Path("results/experiments/static_13pose_training_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w") as f:
        json.dump(
            {
                "num_classes": NUM_STATIC_CLASSES,
                "classes": STATIC_13_NAMES,
                "total_samples": len(X),
                "samples_per_class": samples_per_class,
                "cv_accuracy_5fold": round(mean_acc, 4),
                "final_accuracy": eval_res["accuracy"],
                "final_f1": eval_res["f1"],
                "inference_latency_us": eval_res["inference_latency_us"],
                "confusion_matrix": eval_res["confusion_matrix"],
            },
            f,
            indent=2,
        )
    print(f"Report saved to {report_path}")
    return final_clf


if __name__ == "__main__":
    train_and_save_model()
