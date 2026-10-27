"""
LIVE HAND GA ENGINE — control/controller.py
Central Computer Vision Gesture Controller orchestrating safety, mapping, and execution.

[IMPLEMENTED]
- Coordinates safety manager, command mapper, mouse, keyboard, scroll, and 3D GA object
- Rotating event log saved to results/control/control_log.csv
- Real-time latency tracking (detection, decision, action, end-to-end)
- Thread-safe state control with F12 emergency stop
"""
from __future__ import annotations

import csv
import os
import pathlib
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from control.application_controller import ApplicationController
from control.command_mapper import CommandMapper, GestureCommand
from control.keyboard_controller import KeyboardController
from control.mouse_controller import MouseController
from control.object3d import Virtual3DObject
from control.safety import ControlState, SafetyManager
from control.scroll_controller import ScrollController
from hand_detection.landmarks import HandGeometry


@dataclass
class ControlExecutionReport:
    """Telemetry report for a single frame control iteration."""
    gesture: str
    confidence: float
    command: Optional[str]
    is_executed: bool
    status_message: str
    decision_latency_ms: float
    action_latency_ms: float
    total_control_latency_ms: float
    ga_opcode: str
    is_control_enabled: bool


class GestureController:
    """Master computer vision gesture controller.

    [IMPLEMENTED]
    """

    def __init__(
        self,
        profile_name: str = "mouse",
        log_path: str = "results/control/control_log.csv",
        backend: Any = None,
    ) -> None:
        self.safety = SafetyManager(min_confidence=0.70)
        self.mapper = CommandMapper(profile_name=profile_name)

        # Controllers
        self.mouse = MouseController(backend=backend)
        self.scroll = ScrollController(backend=backend)
        self.keyboard = KeyboardController(backend=backend)
        self.app = ApplicationController(keyboard=self.keyboard)
        self.object3d = Virtual3DObject()

        # Performance & telemetry
        self.commands_executed_count: int = 0
        self.last_command: Optional[GestureCommand] = None
        self.last_execution_report: Optional[ControlExecutionReport] = None
        self.recent_latencies: deque = deque(maxlen=100)

        # Rotating CSV Log
        self.log_path = pathlib.Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_csv_log()

    def _init_csv_log(self) -> None:
        """Initialize CSV log header if file does not exist."""
        if not self.log_path.exists():
            with open(self.log_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp", "gesture", "confidence", "command",
                    "ga_opcode", "result", "total_latency_ms", "profile"
                ])

    def log_event(
        self,
        gesture: str,
        confidence: float,
        command: str,
        ga_opcode: str,
        result: str,
        latency_ms: float,
    ) -> None:
        """Append executed event to CSV log with rotation if exceeding 5MB."""
        try:
            if self.log_path.exists() and self.log_path.stat().st_size > 5 * 1024 * 1024:
                # Rotate log
                backup = self.log_path.with_name("control_log_prev.csv")
                if backup.exists():
                    backup.unlink()
                self.log_path.rename(backup)
                self._init_csv_log()

            with open(self.log_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    gesture,
                    f"{confidence:.3f}",
                    command,
                    ga_opcode,
                    result,
                    f"{latency_ms:.2f}",
                    self.mapper.active_profile_name,
                ])
        except Exception:
            pass

    def set_profile(self, profile_name: str) -> bool:
        """Switch active profile (mouse, presentation, media, object3d)."""
        success = self.mapper.set_profile(profile_name)
        return success

    def enable(self) -> None:
        """Enable gesture control."""
        self.safety.enable()

    def disable(self) -> None:
        """Disable gesture control."""
        self.safety.disable()

    def emergency_stop(self) -> None:
        """Trigger emergency stop cut-off."""
        self.safety.emergency_stop()

    def reset_emergency(self) -> None:
        """Clear emergency stop and reset to DISABLED."""
        self.safety.reset_emergency()

    @property
    def is_enabled(self) -> bool:
        return self.safety.is_enabled

    def process_frame(
        self,
        gesture: str,
        confidence: float,
        geom: Optional[HandGeometry],
        detection_latency_ms: float = 0.0,
    ) -> ControlExecutionReport:
        """Main control loop invoked every video frame.

        [IMPLEMENTED]
        """
        t0_decision = time.perf_counter()
        ga_opcode = "VECTOR"
        executed = False
        status_msg = "IDLE"

        # Check confirmation trigger if OK_SIGN presented
        confirmed_pending = self.safety.check_confirmation_trigger(gesture)
        if confirmed_pending:
            status_msg = f"CONFIRMED: {confirmed_pending.command}"
            t0_action = time.perf_counter()
            executed = self._execute_command_name(confirmed_pending.command, geom)
            t_action = (time.perf_counter() - t0_action) * 1000.0
            t_decision = (time.perf_counter() - t0_decision) * 1000.0
            report = ControlExecutionReport(
                gesture=gesture,
                confidence=confidence,
                command=confirmed_pending.command,
                is_executed=executed,
                status_message=status_msg,
                decision_latency_ms=round(t_decision, 2),
                action_latency_ms=round(t_action, 2),
                total_control_latency_ms=round(t_decision + t_action, 2),
                ga_opcode="INNER",
                is_control_enabled=self.safety.is_enabled,
            )
            self.last_execution_report = report
            return report

        # Safety: check if computer control is emergency stopped or globally disabled
        if self.safety.state == ControlState.EMERGENCY_STOPPED:
            t_dec = (time.perf_counter() - t0_decision) * 1000.0
            return ControlExecutionReport(
                gesture=gesture,
                confidence=confidence,
                command=None,
                is_executed=False,
                status_message="EMERGENCY STOPPED (Press Reset in GUI or CLI)",
                decision_latency_ms=round(t_dec, 2),
                action_latency_ms=0.0,
                total_control_latency_ms=round(t_dec, 2),
                ga_opcode=ga_opcode,
                is_control_enabled=False,
            )

        if not self.safety.is_enabled:
            t_dec = (time.perf_counter() - t0_decision) * 1000.0
            return ControlExecutionReport(
                gesture=gesture,
                confidence=confidence,
                command=None,
                is_executed=False,
                status_message="CONTROL DISABLED (Opt-in via GUI or CLI)",
                decision_latency_ms=round(t_dec, 2),
                action_latency_ms=0.0,
                total_control_latency_ms=round(t_dec, 2),
                ga_opcode=ga_opcode,
                is_control_enabled=False,
            )

        # Safety: check confidence threshold
        min_conf = self.mapper.current_settings.get("min_confidence", 0.70)
        if not self.safety.check_confidence(confidence, threshold_override=min_conf):
            t_dec = (time.perf_counter() - t0_decision) * 1000.0
            return ControlExecutionReport(
                gesture=gesture,
                confidence=confidence,
                command=None,
                is_executed=False,
                status_message="LOW CONFIDENCE (Ignored)",
                decision_latency_ms=round(t_dec, 2),
                action_latency_ms=0.0,
                total_control_latency_ms=round(t_dec, 2),
                ga_opcode=ga_opcode,
                is_control_enabled=True,
            )

        # Map gesture to command
        cmd = self.mapper.map_gesture(gesture, confidence)
        if not cmd:
            t_dec = (time.perf_counter() - t0_decision) * 1000.0
            return ControlExecutionReport(
                gesture=gesture,
                confidence=confidence,
                command=None,
                is_executed=False,
                status_message="UNMAPPED GESTURE",
                decision_latency_ms=round(t_dec, 2),
                action_latency_ms=0.0,
                total_control_latency_ms=round(t_dec, 2),
                ga_opcode=ga_opcode,
                is_control_enabled=True,
            )

        ga_opcode = cmd.ga_opcode
        self.last_command = cmd

        # Check confirmation requirement
        if cmd.requires_confirmation:
            self.safety.request_confirmation(gesture, cmd.command)
            t_dec = (time.perf_counter() - t0_decision) * 1000.0
            return ControlExecutionReport(
                gesture=gesture,
                confidence=confidence,
                command=cmd.command,
                is_executed=False,
                status_message=f"PENDING CONFIRMATION: Show OK_SIGN to execute {cmd.command}",
                decision_latency_ms=round(t_dec, 2),
                action_latency_ms=0.0,
                total_control_latency_ms=round(t_dec, 2),
                ga_opcode=ga_opcode,
                is_control_enabled=True,
            )

        # Check cooldown (skip cooldown for continuous tracking commands like CURSOR_MOVE / MOUSE_DRAG)
        is_continuous = cmd.command in ("CURSOR_MOVE", "MOUSE_DRAG", "OBJECT_POINT_SELECT", "OBJECT_TRANSLATE")
        if not is_continuous:
            if not self.safety.check_cooldown(cmd.command, cmd.cooldown_s):
                t_dec = (time.perf_counter() - t0_decision) * 1000.0
                return ControlExecutionReport(
                    gesture=gesture,
                    confidence=confidence,
                    command=cmd.command,
                    is_executed=False,
                    status_message=f"COOLDOWN ACTIVE ({cmd.command})",
                    decision_latency_ms=round(t_dec, 2),
                    action_latency_ms=0.0,
                    total_control_latency_ms=round(t_dec, 2),
                    ga_opcode=ga_opcode,
                    is_control_enabled=True,
                )

        t_decision = (time.perf_counter() - t0_decision) * 1000.0

        # Execute command
        t0_action = time.perf_counter()
        executed = self._dispatch_command(cmd, geom)
        t_action = (time.perf_counter() - t0_action) * 1000.0
        total_latency = t_decision + t_action

        if executed:
            self.commands_executed_count += 1
            self.safety.register_execution(cmd.command)
            status_msg = f"EXECUTED: {cmd.command}"
            self.recent_latencies.append(total_latency)
            self.log_event(gesture, confidence, cmd.command, ga_opcode, "SUCCESS", total_latency)
        else:
            status_msg = f"FAILED: {cmd.command}"

        report = ControlExecutionReport(
            gesture=gesture,
            confidence=confidence,
            command=cmd.command,
            is_executed=executed,
            status_message=status_msg,
            decision_latency_ms=round(t_decision, 2),
            action_latency_ms=round(t_action, 2),
            total_control_latency_ms=round(total_latency, 2),
            ga_opcode=ga_opcode,
            is_control_enabled=True,
        )
        self.last_execution_report = report
        return report

    def _dispatch_command(self, cmd: GestureCommand, geom: Optional[HandGeometry]) -> bool:
        """Route command to specific subsystem."""
        c = cmd.command

        # Mouse actions
        if c == "CURSOR_MOVE" and geom is not None:
            tip = geom.finger_tip_pos.get("index")
            if tip is not None:
                self.mouse.update_cursor_position(float(tip[0]), float(tip[1]))
                return True
            return False

        elif c == "MOUSE_DOWN":
            self.mouse.handle_pinch_start()
            return True

        elif c == "MOUSE_DRAG" and geom is not None:
            self.mouse.handle_pinch_hold()
            tip = geom.finger_tip_pos.get("index")
            if tip is not None:
                self.mouse.update_cursor_position(float(tip[0]), float(tip[1]))
            return True

        elif c == "MOUSE_UP":
            self.mouse.handle_pinch_release()
            return True

        elif c == "RIGHT_CLICK":
            self.mouse.handle_right_click()
            return True

        elif c == "SCROLL_UP":
            return self.scroll.scroll_up()

        elif c == "SCROLL_DOWN":
            return self.scroll.scroll_down()

        # Presentation actions
        elif c == "NEXT_SLIDE":
            return self.app.next_slide()

        elif c == "PREV_SLIDE":
            return self.app.prev_slide()

        elif c == "START_PRESENTATION":
            return self.app.start_presentation()

        elif c == "ESCAPE_PRESENTATION":
            return self.app.escape_presentation()

        # Media actions
        elif c == "PLAY_PAUSE":
            return self.app.media_play_pause()

        elif c == "MEDIA_NEXT":
            return self.app.media_next()

        elif c == "MEDIA_PREVIOUS":
            return self.app.media_previous()

        elif c == "MEDIA_STOP":
            return self.app.media_stop()

        # 3D Object actions
        elif c == "OBJECT_ROTATE_CW":
            self.object3d.rotate_via_rotor(np.array([0.0, 1.0, 0.0]), np.radians(12.0))
            return True

        elif c == "OBJECT_ROTATE_CCW":
            self.object3d.rotate_via_rotor(np.array([0.0, 1.0, 0.0]), np.radians(-12.0))
            return True

        elif c == "OBJECT_ZOOM_IN":
            self.object3d.zoom(1.10)
            return True

        elif c == "OBJECT_ZOOM_OUT":
            self.object3d.zoom(0.90)
            return True

        elif c == "OBJECT_RESET":
            self.object3d.reset()
            return True

        return False

    def _execute_command_name(self, command_name: str, geom: Optional[HandGeometry]) -> bool:
        """Helper to execute by command string alone."""
        dummy_cmd = GestureCommand(
            gesture="CONFIRMED",
            confidence=1.0,
            duration=0.0,
            command=command_name,
        )
        return self._dispatch_command(dummy_cmd, geom)

    def get_latency_percentiles(self) -> Dict[str, float]:
        """Compute P50, P95, P99 control latency in ms."""
        if not self.recent_latencies:
            return {"p50": 0.0, "p95": 0.0, "p99": 0.0}
        arr = sorted(list(self.recent_latencies))
        n = len(arr)
        return {
            "p50": round(float(np.percentile(arr, 50)), 2),
            "p95": round(float(np.percentile(arr, 95)), 2),
            "p99": round(float(np.percentile(arr, 99)), 2),
        }
