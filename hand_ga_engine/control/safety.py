"""
LIVE HAND GA ENGINE — control/safety.py
Computer vision control safety, rate limiting, debouncing, and emergency kill-switch.

[IMPLEMENTED]
- Minimum confidence filtering
- Cooldown and per-event debouncing
- Confirmation workflow: high-impact action -> PENDING -> OK_SIGN -> EXECUTE
- Global enable/disable with F12 emergency stop
- State tracking: ENABLED, DISABLED, EMERGENCY_STOPPED
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, Optional, Set, Tuple


class ControlState(Enum):
    DISABLED = auto()
    ENABLED = auto()
    EMERGENCY_STOPPED = auto()


@dataclass
class PendingConfirmation:
    """An action awaiting explicit OK_SIGN confirmation."""
    gesture: str
    command: str
    timestamp: float
    expires_at: float
    meta: Dict = field(default_factory=dict)


class SafetyManager:
    """Manages execution safety, debouncing, confirmation states, and emergency cut-off.

    [IMPLEMENTED]
    """

    def __init__(
        self,
        min_confidence: float = 0.70,
        default_cooldown_s: float = 0.35,
        confirmation_timeout_s: float = 4.0,
    ) -> None:
        self.min_confidence = min_confidence
        self.default_cooldown_s = default_cooldown_s
        self.confirmation_timeout_s = confirmation_timeout_s

        self._state: ControlState = ControlState.DISABLED  # Opt-in by default
        self._last_command_time: Dict[str, float] = {}
        self._pending_confirmation: Optional[PendingConfirmation] = None
        self._gesture_active_state: Dict[str, bool] = {}
        self._ignored_low_conf_count: int = 0
        self._false_trigger_blocked: int = 0
        self._confirmed_count: int = 0

    @property
    def is_enabled(self) -> bool:
        return self._state == ControlState.ENABLED

    @property
    def state(self) -> ControlState:
        return self._state

    @property
    def pending_confirmation(self) -> Optional[PendingConfirmation]:
        if self._pending_confirmation:
            if time.time() > self._pending_confirmation.expires_at:
                self._pending_confirmation = None
        return self._pending_confirmation

    @property
    def metrics(self) -> Dict[str, int]:
        return {
            "ignored_low_conf": self._ignored_low_conf_count,
            "false_triggers_blocked": self._false_trigger_blocked,
            "confirmations_executed": self._confirmed_count,
        }

    def enable(self) -> None:
        """Enable computer control."""
        self._state = ControlState.ENABLED

    def disable(self) -> None:
        """Disable computer control."""
        self._state = ControlState.DISABLED
        self._pending_confirmation = None

    def emergency_stop(self) -> None:
        """Immediate cut-off trigger (e.g., F12 key or Emergency button)."""
        self._state = ControlState.EMERGENCY_STOPPED
        self._pending_confirmation = None

    def reset_emergency(self) -> None:
        """Clear emergency stop and return to DISABLED."""
        self._state = ControlState.DISABLED

    def check_confidence(self, confidence: float, threshold_override: Optional[float] = None) -> bool:
        """Verify gesture confidence exceeds required threshold."""
        thresh = threshold_override if threshold_override is not None else self.min_confidence
        if confidence < thresh:
            self._ignored_low_conf_count += 1
            return False
        return True

    def check_cooldown(self, command_name: str, cooldown_s: Optional[float] = None) -> bool:
        """Verify cooldown period has elapsed for the given command."""
        cd = cooldown_s if cooldown_s is not None else self.default_cooldown_s
        now = time.time()
        last_time = self._last_command_time.get(command_name, 0.0)
        if now - last_time < cd:
            self._false_trigger_blocked += 1
            return False
        return True

    def register_execution(self, command_name: str) -> None:
        """Record that a command was executed now (updates cooldown timer)."""
        self._last_command_time[command_name] = time.time()

    def debounce_edge(self, gesture_name: str, is_active: bool) -> bool:
        """Edge detector: returns True only on the rising edge (0 -> 1) of a gesture."""
        was_active = self._gesture_active_state.get(gesture_name, False)
        self._gesture_active_state[gesture_name] = is_active
        return is_active and not was_active

    def request_confirmation(
        self,
        gesture: Union[str, Any],
        command: Optional[str] = None,
        meta: Optional[Dict] = None,
    ) -> PendingConfirmation:
        """Queue an action for OK_SIGN confirmation."""
        now = time.time()
        if hasattr(gesture, "command"):
            cmd = gesture.command
            gest = gesture.gesture
            m = getattr(gesture, "parameters", {})
        else:
            cmd = command or ""
            gest = str(gesture)
            m = meta or {}

        pending = PendingConfirmation(
            gesture=gest,
            command=cmd,
            timestamp=now,
            expires_at=now + self.confirmation_timeout_s,
            meta=m,
        )
        self._pending_confirmation = pending
        return pending

    def check_confirmation_trigger(self, gesture_name: str) -> Optional[PendingConfirmation]:
        """If an action is pending and OK_SIGN is presented, confirms the action."""
        if gesture_name != "OK_SIGN":
            return None

        pending = self.pending_confirmation
        if pending is not None:
            self._confirmed_count += 1
            self._pending_confirmation = None
            return pending
        return None
