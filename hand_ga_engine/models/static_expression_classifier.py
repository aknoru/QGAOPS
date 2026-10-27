"""
LIVE HAND GA ENGINE — models/static_expression_classifier.py
Interpretable landmark-geometry classifier & lightweight image baseline.

[IMPLEMENTED] Standard interface:
    classifier.fit(X_train, y_train)
    classifier.predict(X)
    classifier.predict_proba(X)
    classifier.evaluate(X_test, y_test)
[IMPLEMENTED] Rejection threshold for UNKNOWN class.
"""
from __future__ import annotations

import os
import pickle
import time
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from mapping.dataset_classes import CLASS_NAMES, UNKNOWN_CLASS
from mapping.expression_classes import STATIC_13_NAMES


class StaticExpressionClassifier:
    """Interpretable classifier trained on normalized hand-geometry features.

    [IMPLEMENTED]

    Args:
        model_type: 'random_forest' or 'svm'.
        confidence_threshold: Minimum probability to assign a class, else UNKNOWN.
        random_state: Seed for reproducibility.
        class_names: Optional dictionary mapping int ID to class name.
    """

    def __init__(
        self,
        model_type: str = "random_forest",
        confidence_threshold: float = 0.60,
        random_state: int = 42,
        class_names: Optional[Dict[int, str]] = None,
    ) -> None:
        self.model_type = model_type.lower()
        self.confidence_threshold = confidence_threshold
        self.random_state = random_state
        self.class_names = dict(class_names) if class_names is not None else dict(STATIC_13_NAMES)

        self.scaler = StandardScaler()
        self.classes_ = np.array(sorted(self.class_names.keys()))
        self.num_classes = len(self.classes_)

        if self.model_type == "svm":
            self.model = SVC(
                kernel="rbf",
                C=10.0,
                gamma="scale",
                probability=True,
                random_state=random_state,
            )
        else:
            self.model = RandomForestClassifier(
                n_estimators=120,
                max_depth=12,
                min_samples_split=4,
                class_weight="balanced",
                random_state=random_state,
                n_jobs=-1,
            )

        self._is_fitted = False

    def fit(self, X_train: np.ndarray, y_train: np.ndarray) -> "StaticExpressionClassifier":
        """Fit scaler and classifier on training data."""
        if len(X_train) == 0:
            raise ValueError("Cannot fit on empty dataset.")

        unique_y = np.unique(y_train)
        all_classes = sorted(list(set(self.class_names.keys()) | set(unique_y)))
        self.classes_ = np.array(all_classes)
        self.num_classes = len(self.classes_)

        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self._is_fitted = True
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict class probabilities."""
        if not self._is_fitted:
            raise RuntimeError("Classifier is not fitted yet.")

        if X.ndim == 1:
            X = X.reshape(1, -1)

        X_scaled = self.scaler.transform(X)
        probs = self.model.predict_proba(X_scaled)

        # Ensure full 6-class probability distribution even if some classes were unrepresented in training
        if probs.shape[1] < self.num_classes:
            full_probs = np.zeros((len(X), self.num_classes), dtype=np.float32)
            for idx, c in enumerate(self.model.classes_):
                full_probs[:, c] = probs[:, idx]
            return full_probs

        return probs

    def predict(self, X: np.ndarray) -> List[Union[int, str]]:
        """Predict class ID or UNKNOWN if confidence < threshold."""
        probs = self.predict_proba(X)
        max_probs = np.max(probs, axis=1)
        best_classes = np.argmax(probs, axis=1)

        predictions = []
        for best_cls, max_prob in zip(best_classes, max_probs):
            if max_prob < self.confidence_threshold:
                predictions.append(UNKNOWN_CLASS)
            else:
                predictions.append(int(best_cls))
        return predictions

    def predict_single(self, feature_vector: np.ndarray) -> Tuple[str, float]:
        """Convenience method for single-frame live inference.

        Returns:
            (class_name, confidence)
        """
        if not self._is_fitted:
            return UNKNOWN_CLASS, 0.0

        probs = self.predict_proba(feature_vector.reshape(1, -1))[0]
        best_id = int(np.argmax(probs))
        conf = float(probs[best_id])

        if conf < self.confidence_threshold:
            return UNKNOWN_CLASS, conf

        c_names = getattr(self, "class_names", CLASS_NAMES)
        class_name = c_names.get(best_id, UNKNOWN_CLASS)
        return class_name, conf

    def evaluate(
        self, X_test: np.ndarray, y_test: np.ndarray, class_names: Optional[Dict[int, str]] = None
    ) -> Dict[str, Any]:
        """Evaluate model performance on test data with microsecond latency measurement."""
        if not self._is_fitted:
            raise RuntimeError("Classifier is not fitted.")

        c_names = class_names or getattr(self, "class_names", CLASS_NAMES)

        # Measure inference latency
        t0 = time.perf_counter()
        probs = self.predict_proba(X_test)
        elapsed = time.perf_counter() - t0
        latency_us = (elapsed / max(len(X_test), 1)) * 1e6

        y_pred_raw = np.argmax(probs, axis=1)

        # Standard metrics
        acc = float(accuracy_score(y_test, y_pred_raw))
        prec = float(precision_score(y_test, y_pred_raw, average="weighted", zero_division=0))
        rec = float(recall_score(y_test, y_pred_raw, average="weighted", zero_division=0))
        f1 = float(f1_score(y_test, y_pred_raw, average="weighted", zero_division=0))

        # Distinct labels present
        labels_present = [int(x) for x in sorted(list(set(y_test) | set(y_pred_raw)))]
        target_names = [c_names.get(i, f"Class_{i}") for i in labels_present]

        cm = confusion_matrix(y_test, y_pred_raw, labels=labels_present)
        report_str = classification_report(
            y_test, y_pred_raw, labels=labels_present, target_names=target_names, zero_division=0
        )

        return {
            "model_type": self.model_type,
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "f1": round(f1, 4),
            "inference_latency_us": round(latency_us, 2),
            "confusion_matrix": cm.tolist(),
            "labels_present": labels_present,
            "target_names": target_names,
            "classification_report": report_str,
            "test_samples": len(y_test),
        }

    def save(self, filepath: str) -> None:
        """Save fitted model and scaler to file."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load(cls, filepath: str) -> "StaticExpressionClassifier":
        """Load fitted model from file."""
        with open(filepath, "rb") as f:
            return pickle.load(f)
