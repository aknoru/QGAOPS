"""
LIVE HAND GA ENGINE — expression/temporal_smoother.py
Temporal smoothing and majority voting for static expression predictions.

[IMPLEMENTED] Prevents single-frame flicker using a rolling prediction buffer.
[IMPLEMENTED] Rejects unstable transitions or low-confidence frames as UNKNOWN.
"""
from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from typing import Deque, Optional, Tuple

from mapping.dataset_classes import UNKNOWN_CLASS


@dataclass
class SmoothedPrediction:
    """Result of temporal smoothing over recent expression predictions."""
    expression: str
    confidence: float
    is_stable: bool
    vote_ratio: float
    history_length: int


class ExpressionTemporalSmoother:
    """Maintains a rolling window of recent predictions to provide stable output.

    [IMPLEMENTED]
    """

    def __init__(
        self,
        window_size: int = 5,
        min_majority_ratio: float = 0.60,
        confidence_threshold: float = 0.60,
    ) -> None:
        self.window_size = window_size
        self.min_majority_ratio = min_majority_ratio
        self.confidence_threshold = confidence_threshold

        self._history: Deque[Tuple[str, float]] = deque(maxlen=window_size)
        self._current_stable_expr: str = UNKNOWN_CLASS
        self._current_stable_conf: float = 0.0

    def update(self, raw_expression: str, raw_confidence: float) -> SmoothedPrediction:
        """Add new frame prediction and compute smoothed consensus.

        Args:
            raw_expression: Raw predicted class name.
            raw_confidence: Confidence score in [0, 1].

        Returns:
            SmoothedPrediction dataclass.
        """
        if raw_confidence < self.confidence_threshold:
            raw_expression = UNKNOWN_CLASS

        self._history.append((raw_expression, raw_confidence))

        # Count occurrences of each expression in window
        expressions = [expr for expr, _ in self._history]
        counts = Counter(expressions)

        # Most common expression
        winner, count = counts.most_common(1)[0]
        ratio = count / len(self._history)

        # Average confidence for the winner
        winner_confs = [conf for expr, conf in self._history if expr == winner]
        avg_conf = float(sum(winner_confs) / len(winner_confs)) if winner_confs else 0.0

        is_stable = (ratio >= self.min_majority_ratio) and (winner != UNKNOWN_CLASS)

        if is_stable:
            self._current_stable_expr = winner
            self._current_stable_conf = avg_conf
        elif ratio >= self.min_majority_ratio and winner == UNKNOWN_CLASS:
            self._current_stable_expr = UNKNOWN_CLASS
            self._current_stable_conf = avg_conf

        return SmoothedPrediction(
            expression=self._current_stable_expr,
            confidence=self._current_stable_conf,
            is_stable=is_stable,
            vote_ratio=ratio,
            history_length=len(self._history),
        )

    def reset(self) -> None:
        """Clear temporal history (e.g. when hand disappears)."""
        self._history.clear()
        self._current_stable_expr = UNKNOWN_CLASS
        self._current_stable_conf = 0.0
