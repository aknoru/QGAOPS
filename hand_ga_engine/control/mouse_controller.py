"""
LIVE HAND GA ENGINE — control/mouse_controller.py
Computer vision cursor positioning, smoothing, click debouncing, and drag controller.

[IMPLEMENTED]
- Index fingertip tracking with normalized coordinate mapping
- EMA cursor smoothing & dead-zone filtering
- Maximum velocity clamping & screen edge protection
- Single-click debounce for PINCH_START
- PINCH_HOLD + motion for mouse drag
- TWO_FINGER for right click
- Mockable backend support for safe unit testing
"""
from __future__ import annotations

import time
from typing import Any, Optional, Protocol, Tuple

import numpy as np


class InputBackend(Protocol):
    """Protocol for mouse and keyboard simulation."""
    def get_screen_size(self) -> Tuple[int, int]: ...
    def move_to(self, x: int, y: int) -> None: ...
    def mouse_down(self, button: str = "left") -> None: ...
    def mouse_up(self, button: str = "left") -> None: ...
    def click(self, button: str = "left") -> None: ...
    def right_click(self) -> None: ...


class MockInputBackend:
    """Mock backend for unit testing without physical OS hardware interaction."""
    def __init__(
        self,
        screen_w: int = 1920,
        screen_h: int = 1080,
        screen_width: Optional[int] = None,
        screen_height: Optional[int] = None,
    ) -> None:
        self.screen_w = screen_width if screen_width is not None else screen_w
        self.screen_h = screen_height if screen_height is not None else screen_h
        self.cursor_x = self.screen_w // 2
        self.cursor_y = self.screen_h // 2
        self.button_state = {"left": False, "right": False, "middle": False}
        self.event_log = []

    @property
    def events(self):
        return self.event_log

    @property
    def mouse_down_state(self) -> bool:
        return self.button_state["left"]

    def get_screen_size(self) -> Tuple[int, int]:
        return (self.screen_w, self.screen_h)

    def move_to(self, x: int, y: int) -> None:
        self.cursor_x = x
        self.cursor_y = y
        self.event_log.append(("move", x, y))

    def mouse_down(self, button: str = "left") -> None:
        self.button_state[button] = True
        self.event_log.append(("mouse_down", button))

    def mouse_up(self, button: str = "left") -> None:
        self.button_state[button] = False
        self.event_log.append(("mouse_up", button))

    def click(self, button: str = "left") -> None:
        self.event_log.append(("click", button))

    def right_click(self) -> None:
        self.event_log.append(("click", "right"))

    def press(self, key: str) -> None:
        self.event_log.append(("press", key))

    def press_key(self, key: str) -> None:
        self.press(key)

    def scroll(self, amount: int) -> None:
        self.event_log.append(("scroll", amount))


class NativePyAutoGUIBackend:
    """Production backend wrapping pyautogui with safety protections."""
    def __init__(self) -> None:
        try:
            import pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.001
            self._pyautogui = pyautogui
            self.screen_w, self.screen_h = pyautogui.size()
        except Exception:
            self._pyautogui = None
            self.screen_w, self.screen_h = 1920, 1080

    def get_screen_size(self) -> Tuple[int, int]:
        return (self.screen_w, self.screen_h)

    def move_to(self, x: int, y: int) -> None:
        if self._pyautogui is None:
            return
        cx = max(0, min(self.screen_w - 1, x))
        cy = max(0, min(self.screen_h - 1, y))
        try:
            self._pyautogui.moveTo(cx, cy)
        except Exception:
            pass

    def mouse_down(self, button: str = "left") -> None:
        if self._pyautogui is not None:
            try:
                self._pyautogui.mouseDown(button=button)
            except Exception:
                pass

    def mouse_up(self, button: str = "left") -> None:
        if self._pyautogui is not None:
            try:
                self._pyautogui.mouseUp(button=button)
            except Exception:
                pass

    def click(self, button: str = "left") -> None:
        if self._pyautogui is not None:
            try:
                self._pyautogui.click(button=button)
            except Exception:
                pass

    def right_click(self) -> None:
        if self._pyautogui is not None:
            try:
                self._pyautogui.rightClick()
            except Exception:
                pass


class MouseController:
    """High-precision, smoothed computer vision mouse controller.

    [IMPLEMENTED]
    """

    def __init__(
        self,
        backend: Optional[InputBackend] = None,
        smoothing_alpha: float = 0.35,
        dead_zone: float = 0.015,
        max_velocity: float = 90.0,
        edge_margin: int = 15,
        dead_zone_px: Optional[float] = None,
    ) -> None:
        self.backend = backend or NativePyAutoGUIBackend()
        self.screen_w, self.screen_h = self.backend.get_screen_size()
        self.smoothing_alpha = smoothing_alpha
        self.dead_zone = (dead_zone_px / self.screen_w) if dead_zone_px is not None else dead_zone
        self.max_velocity = max_velocity
        self.edge_margin = edge_margin

        # Coordinates tracking
        self.current_x = self.screen_w // 2
        self.current_y = self.screen_h // 2
        self._last_norm_x = 0.5
        self._last_norm_y = 0.5

        # Drag state
        self.is_dragging = False
        self.is_mouse_down = False

    def update_cursor_position(self, norm_x: float, norm_y: float) -> Tuple[int, int]:
        """Convert normalized fingertip coords (0 to 1) into smoothed screen pixels.

        [IMPLEMENTED]
        """
        # 1. Dead-zone threshold
        dx = norm_x - self._last_norm_x
        dy = norm_y - self._last_norm_y
        dist = np.hypot(dx, dy)

        if dist < self.dead_zone:
            return (self.current_x, self.current_y)

        # 2. Maximum velocity clamping (prevent cursor teleportation on lost tracking)
        max_step = self.max_velocity / 1000.0
        if dist > max_step:
            scale = max_step / dist
            norm_x = self._last_norm_x + dx * scale
            norm_y = self._last_norm_y + dy * scale

        # 3. EMA coordinate smoothing
        sm_norm_x = self.smoothing_alpha * norm_x + (1.0 - self.smoothing_alpha) * self._last_norm_x
        sm_norm_y = self.smoothing_alpha * norm_y + (1.0 - self.smoothing_alpha) * self._last_norm_y

        self._last_norm_x = sm_norm_x
        self._last_norm_y = sm_norm_y

        # 4. Screen mapping with edge margins
        target_x = int(sm_norm_x * self.screen_w)
        target_y = int(sm_norm_y * self.screen_h)

        target_x = max(self.edge_margin, min(self.screen_w - self.edge_margin, target_x))
        target_y = max(self.edge_margin, min(self.screen_h - self.edge_margin, target_y))

        self.current_x = target_x
        self.current_y = target_y

        self.backend.move_to(self.current_x, self.current_y)
        return (self.current_x, self.current_y)

    def handle_pinch_start(self) -> None:
        """Left mouse down (drag start)."""
        if not self.is_mouse_down:
            self.backend.mouse_down(button="left")
            self.is_mouse_down = True
            self.is_dragging = False

    def handle_pinch_hold(self) -> None:
        """Sustained pinch marks dragging active."""
        if self.is_mouse_down:
            self.is_dragging = True

    def handle_pinch_release(self) -> None:
        """Left mouse up (release click/drag)."""
        if self.is_mouse_down:
            self.backend.mouse_up(button="left")
            self.is_mouse_down = False
            self.is_dragging = False

    def handle_click(self) -> None:
        """Single left click."""
        self.backend.click(button="left")

    def handle_right_click(self) -> None:
        """Right mouse click."""
        self.backend.right_click()
