"""
LIVE HAND GA ENGINE — train.py
Training and evaluation script for Kaggle LeapGestRecog 6-class static expression classifiers.

[IMPLEMENTED]
1. Stratified 70/15/15 train/val/test split with fixed random seed.
2. 5-fold cross-validation on training data.
3. Trains interpretable Landmark/Geometry Classifier (Random Forest / SVM).
4. Trains Image Baseline Classifier (HOG + Classifier) for rigorous comparison.
5. Saves models to models/ and comprehensive metrics, classification report,
   and confusion matrix plots to results/training/.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, Tuple

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import StratifiedKFold, train_test_split

from mapping.dataset_classes import CLASS_NAMES
from models.static_expression_classifier import StaticExpressionClassifier


def load_dataset_features(features_path: str = "dataset/features/extracted_features.npz"):
    """Load pre-extracted features or run extraction if missing."""
    if not os.path.exists(features_path):
        print(f"[INFO] Features not found at {features_path}. Running feature extraction...")
        from scripts.extract_features import process_dataset
        process_dataset()

    data = np.load(features_path)
    return {
        "X_image": data["X_image"],
        "y_image": data["y_image"],
        "X_landmark": data["X_landmark"],
        "y_landmark": data["y_landmark"],
    }


def split_data(
    X: np.ndarray, y: np.ndarray, train_ratio: float = 0.70, val_ratio: float = 0.15, test_ratio: float = 0.15, seed: int = 42
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Stratified 70/15/15 split without data leakage."""
    test_size = test_ratio
    val_size_adjusted = val_ratio / (train_ratio + val_ratio)

    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, stratify=y, random_state=seed
    )

    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=val_size_adjusted, stratify=y_train_val, random_state=seed
    )

    return X_train, y_train, X_val, y_val, X_test, y_test


def plot_confusion_matrix(cm: np.ndarray, target_names: list, out_path: str, title: str):
    """Render and save publication-quality confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
    im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.figure.colorbar(im, ax=ax)

    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=target_names,
        yticklabels=target_names,
        ylabel="True Label",
        xlabel="Predicted Label",
        title=title,
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    thresh = cm.max() / 2.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j, i, format(cm[i, j], "d"),
                ha="center", va="center",
                color="white" if cm[i, j] > thresh else "black",
                fontweight="bold" if i == j else "normal",
            )
    fig.tight_layout()
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    fig.savefig(out_path)
    plt.close(fig)


def run_training(
    dataset_path: str = "LeapGestRecog_1/LeapGestRecog_1",
    model_choice: str = "both",  # 'landmark', 'image', or 'both'
    seed: int = 42,
) -> Dict[str, Any]:
    print("=" * 65)
    print("  QGAOPS STATIC HAND EXPRESSION CLASSIFIER TRAINING")
    print("=" * 65)
    print(f"Dataset path:  {dataset_path}")
    print(f"Model choice:  {model_choice}")
    print(f"Random seed:   {seed}")

    os.makedirs("models", exist_ok=True)
    os.makedirs("results/training", exist_ok=True)

    data = load_dataset_features()
    results_summary: Dict[str, Any] = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "random_seed": seed,
        "models": {},
    }

    # -------------------------------------------------------------
    # 1. LANDMARK / GEOMETRIC CLASSIFIER
    # -------------------------------------------------------------
    if model_choice in ("landmark", "both"):
        X_lm = data["X_landmark"]
        y_lm = data["y_landmark"]

        print(f"\n[1] LANDMARK GEOMETRY CLASSIFIER")
        print(f"  Total valid landmark samples: {len(X_lm)} (feature dim: {X_lm.shape[1]})")

        if len(X_lm) > 20:
            X_tr, y_tr, X_val, y_val, X_te, y_te = split_data(X_lm, y_lm, seed=seed)
            print(f"  Split: Train={len(y_tr)}, Val={len(y_val)}, Test={len(y_te)}")

            # 5-fold CV on training set
            skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
            cv_scores = []
            for fold, (trn_idx, val_idx) in enumerate(skf.split(X_tr, y_tr)):
                m_fold = StaticExpressionClassifier(model_type="random_forest", random_state=seed)
                m_fold.fit(X_tr[trn_idx], y_tr[trn_idx])
                ev = m_fold.evaluate(X_tr[val_idx], y_tr[val_idx])
                cv_scores.append(ev["accuracy"])

            cv_mean = float(np.mean(cv_scores))
            cv_std = float(np.std(cv_scores))
            print(f"  5-Fold CV Accuracy: {cv_mean*100:.2f}% ± {cv_std*100:.2f}%")

            # Final model trained on train split
            clf_lm = StaticExpressionClassifier(model_type="random_forest", random_state=seed)
            clf_lm.fit(X_tr, y_tr)

            # Evaluate on held-out test split
            eval_lm = clf_lm.evaluate(X_te, y_te)
            eval_lm["cv_5fold_mean"] = round(cv_mean, 4)
            eval_lm["cv_5fold_std"] = round(cv_std, 4)

            # Save model
            model_file = "models/static_expression_model.pkl"
            clf_lm.save(model_file)
            print(f"  Saved model: {model_file}")

            # Plot confusion matrix
            cm_plot_path = "results/training/confusion_matrix_landmark.png"
            plot_confusion_matrix(
                np.array(eval_lm["confusion_matrix"]),
                eval_lm["target_names"],
                cm_plot_path,
                "Landmark Geometry Classifier — Confusion Matrix",
            )

            results_summary["models"]["landmark_geometry"] = eval_lm
            print(f"  Test Accuracy:  {eval_lm['accuracy']*100:.2f}%")
            print(f"  Test Precision: {eval_lm['precision']*100:.2f}%")
            print(f"  Test Recall:    {eval_lm['recall']*100:.2f}%")
            print(f"  Test F1-Score:  {eval_lm['f1']*100:.2f}%")
            print(f"  Latency:        {eval_lm['inference_latency_us']} µs/sample")

    # -------------------------------------------------------------
    # 2. IMAGE BASELINE CLASSIFIER (Full 6-Class Comparison)
    # -------------------------------------------------------------
    if model_choice in ("image", "both"):
        X_im = data["X_image"]
        y_im = data["y_image"]

        print(f"\n[2] IMAGE BASELINE CLASSIFIER (6 Classes)")
        print(f"  Total image samples: {len(X_im)} (feature dim: {X_im.shape[1]})")

        X_tr, y_tr, X_val, y_val, X_te, y_te = split_data(X_im, y_im, seed=seed)
        print(f"  Split: Train={len(y_tr)}, Val={len(y_val)}, Test={len(y_te)}")

        # 5-fold CV
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=seed)
        cv_scores = []
        for fold, (trn_idx, val_idx) in enumerate(skf.split(X_tr, y_tr)):
            m_fold = StaticExpressionClassifier(model_type="random_forest", random_state=seed)
            m_fold.fit(X_tr[trn_idx], y_tr[trn_idx])
            ev = m_fold.evaluate(X_tr[val_idx], y_tr[val_idx])
            cv_scores.append(ev["accuracy"])

        cv_mean = float(np.mean(cv_scores))
        cv_std = float(np.std(cv_scores))
        print(f"  5-Fold CV Accuracy: {cv_mean*100:.2f}% ± {cv_std*100:.2f}%")

        clf_im = StaticExpressionClassifier(model_type="random_forest", random_state=seed)
        clf_im.fit(X_tr, y_tr)

        eval_im = clf_im.evaluate(X_te, y_te)
        eval_im["cv_5fold_mean"] = round(cv_mean, 4)
        eval_im["cv_5fold_std"] = round(cv_std, 4)

        model_file = "models/image_baseline_model.pkl"
        clf_im.save(model_file)
        print(f"  Saved model: {model_file}")

        cm_plot_path = "results/training/confusion_matrix.png"
        plot_confusion_matrix(
            np.array(eval_im["confusion_matrix"]),
            eval_im["target_names"],
            cm_plot_path,
            "Image Baseline Classifier (All 6 Classes) — Confusion Matrix",
        )

        results_summary["models"]["image_baseline"] = eval_im
        print(f"  Test Accuracy:  {eval_im['accuracy']*100:.2f}%")
        print(f"  Test Precision: {eval_im['precision']*100:.2f}%")
        print(f"  Test Recall:    {eval_im['recall']*100:.2f}%")
        print(f"  Test F1-Score:  {eval_im['f1']*100:.2f}%")
        print(f"  Latency:        {eval_im['inference_latency_us']} µs/sample")

    # -------------------------------------------------------------
    # Save Reports
    # -------------------------------------------------------------
    metrics_path = "results/training/metrics.json"
    with open(metrics_path, "w") as f:
        json.dump(results_summary, f, indent=2, default=lambda o: int(o) if isinstance(o, (np.integer, int)) else float(o) if isinstance(o, (np.floating, float)) else str(o))
    print(f"\n[SAVED] Metrics JSON written to {metrics_path}")

    # Text report
    txt_report_path = "results/training/classification_report.txt"
    with open(txt_report_path, "w") as f:
        f.write("=" * 65 + "\n")
        f.write("  STATIC HAND EXPRESSION CLASSIFIER EVALUATION REPORT\n")
        f.write("=" * 65 + "\n\n")
        for mname, mdata in results_summary["models"].items():
            f.write(f"--- MODEL: {mname.upper()} ---\n")
            f.write(f"Accuracy:  {mdata['accuracy']*100:.2f}%\n")
            f.write(f"Precision: {mdata['precision']*100:.2f}%\n")
            f.write(f"Recall:    {mdata['recall']*100:.2f}%\n")
            f.write(f"F1-Score:  {mdata['f1']*100:.2f}%\n")
            f.write(f"5-Fold CV: {mdata.get('cv_5fold_mean', 0)*100:.2f}% ± {mdata.get('cv_5fold_std', 0)*100:.2f}%\n")
            f.write(f"Inference: {mdata['inference_latency_us']} µs\n\n")
            f.write("Classification Report:\n")
            f.write(mdata["classification_report"] + "\n\n")
    print(f"[SAVED] Text classification report written to {txt_report_path}")

    return results_summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Static Expression Classifiers")
    parser.add_argument("--dataset", type=str, default="LeapGestRecog_1/LeapGestRecog_1", help="Dataset root path")
    parser.add_argument("--model", type=str, default="both", choices=["landmark", "image", "both"], help="Model type to train")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    run_training(dataset_path=args.dataset, model_choice=args.model, seed=args.seed)
