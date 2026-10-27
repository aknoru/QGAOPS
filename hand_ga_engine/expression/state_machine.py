"""
LIVE HAND GA ENGINE — expression/state_machine.py
Expression State Machine.

[IMPLEMENTED] IDLE → HAND_DETECTED → POSE_STABLE → GESTURE_STARTED
              → GESTURE_ACTIVE → GESTURE_COMPLETED → COOLDOWN → IDLE

Prevents rapid expression switching via temporal hysteresis.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class ExpressionState(Enum):
    IDLE               = auto()
    HAND_DETECTED      = auto()
    POSE_STABLE        = auto()
    GESTURE_STARTED    = auto()
    GESTURE_ACTIVE     = auto()
    GESTURE_COMPLETED  = auto()
    COOLDOWN           = auto()


@dataclass
class ExpressionEvent:
    """A completed expression event from the state machine.

    [IMPLEMENTED]
    """
    expression:  str
    confidence:  float
    stability:   float
    duration_s:  float
    start_frame: int
    end_frame:   int
    timestamp:   float = field(default_factory=time.time)


class ExpressionStateMachine:
    """Manages expression recognition lifecycle.

    [IMPLEMENTED]

    Args:
        stable_frames:   Frames required in POSE_STABLE before GESTURE_STARTED.
        cooldown_frames: Frames to wait in COOLDOWN before returning to IDLE.
        confidence_min:  Minimum confidence to transition from HAND_DETECTED.
    """

    def __init__(
        self,
        stable_frames:   int   = 5,
        cooldown_frames: int   = 15,
        confidence_min:  float = 0.60,
    ) -> None:
        self.stable_frames   = stable_frames
        self.cooldown_frames = cooldown_frames
        self.confidence_min  = confidence_min

        self._state            = ExpressionState.IDLE
        self._current_expr     = "UNKNOWN"
        self._current_conf     = 0.0
        self._stable_count     = 0
        self._cooldown_count   = 0
        self._start_frame      = 0
        self._frame_count      = 0
        self._start_time       = 0.0
        self._last_completed   = "UNKNOWN"
        self._stability_history: list = []  # last N confidences

    @property
    def state(self) -> ExpressionState:
        return self._state

    @property
    def current_expression(self) -> str:
        return self._current_expr

    def update(
        self,
        hand_detected: bool,
        expression:    str,
        confidence:    float,
    ) -> Optional[ExpressionEvent]:
        """Advance the state machine with current frame info.

        [IMPLEMENTED]

        Args:
            hand_detected: Whether a hand is visible this frame.
            expression:    Current recognized expression/pose.
            confidence:    Confidence of that expression.

        Returns:
            ExpressionEvent if an expression was completed, else None.
        """
        self._frame_count += 1
        completed: Optional[ExpressionEvent] = None

        if self._state == ExpressionState.IDLE:
            if hand_detected:
                self._state = ExpressionState.HAND_DETECTED
                self._stable_count = 0
                self._stability_history = []

        elif self._state == ExpressionState.HAND_DETECTED:
            if not hand_detected:
                self._state = ExpressionState.IDLE
            elif confidence >= self.confidence_min:
                if expression == self._current_expr:
                    self._stable_count += 1
                else:
                    self._current_expr = expression
                    self._stable_count = 1
                    self._stability_history = []
                self._stability_history.append(confidence)
                if self._stable_count >= self.stable_frames:
                    self._state = ExpressionState.POSE_STABLE

        elif self._state == ExpressionState.POSE_STABLE:
            if not hand_detected:
                self._state = ExpressionState.COOLDOWN
                self._cooldown_count = 0
            else:
                # Track if expression changed
                if expression != self._current_expr:
                    self._state = ExpressionState.GESTURE_STARTED
                    self._start_frame = self._frame_count
                    self._start_time = time.time()
                    self._current_expr = expression
                else:
                    # Stable hold → GESTURE_ACTIVE
                    self._state = ExpressionState.GESTURE_ACTIVE
                    self._start_frame = self._frame_count
                    self._start_time = time.time()
                self._stability_history.append(confidence)

        elif self._state == ExpressionState.GESTURE_STARTED:
            if not hand_detected:
                self._state = ExpressionState.GESTURE_COMPLETED
            elif expression != self._current_expr and confidence > self.confidence_min:
                self._state = ExpressionState.GESTURE_COMPLETED
            else:
                self._state = ExpressionState.GESTURE_ACTIVE
            self._stability_history.append(confidence)

        elif self._state == ExpressionState.GESTURE_ACTIVE:
            if not hand_detected:
                self._state = ExpressionState.GESTURE_COMPLETED
            elif expression != self._current_expr and confidence > self.confidence_min:
                # New expression started
                completed = self._make_event(confidence)
                self._state = ExpressionState.COOLDOWN
                self._cooldown_count = 0
            self._stability_history.append(confidence)

        elif self._state == ExpressionState.GESTURE_COMPLETED:
            completed = self._make_event(confidence)
            self._last_completed = self._current_expr
            self._state = ExpressionState.COOLDOWN
            self._cooldown_count = 0

        elif self._state == ExpressionState.COOLDOWN:
            self._cooldown_count += 1
            if self._cooldown_count >= self.cooldown_frames:
                self._state = ExpressionState.IDLE
                self._stable_count = 0
                self._current_expr = "UNKNOWN"
                self._stability_history = []

        return completed

    def _make_event(self, confidence: float) -> ExpressionEvent:
        duration = time.time() - self._start_time
        stability = (
            float(sum(self._stability_history[-10:]) / max(1, len(self._stability_history[-10:])))
            if self._stability_history else 0.0
        )
        return ExpressionEvent(
            expression=self._current_expr,
            confidence=float(confidence),
            stability=float(stability),
            duration_s=float(duration),
            start_frame=self._start_frame,
            end_frame=self._frame_count,
        )

    def force_reset(self) -> None:
        """Reset the state machine to IDLE."""
        self._state          = ExpressionState.IDLE
        self._current_expr   = "UNKNOWN"
        self._stable_count   = 0
        self._cooldown_count = 0
        self._stability_history = []

    def __repr__(self) -> str:
        return (
            f"ExpressionStateMachine(state={self._state.name}, "
            f"expr={self._current_expr!r}, stable_count={self._stable_count})"
        )
