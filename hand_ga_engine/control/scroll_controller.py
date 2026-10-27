"""
LIVE HAND GA ENGINE — control/scroll_controller.py
Rate-limited, debounced page scroll controller.

[IMPLEMENTED]
- SWIPE_UP -> scroll up
- SWIPE_DOWN -> scroll down
- Configurable scroll steps
- Single burst lock per swipe
"""
from __future__ import annotations

import time
from typing import Any, Optional


class ScrollController:
    """Controls vertical scrolling with rate-limiting and debouncing."""

    def __init__(
        self,
        default_scroll_amount: int = 4,
        swipe_lock_s: float = 0.40,
        backend: Any = None,
    ) -> None:
        self.scroll_amount = default_scroll_amount
        self.swipe_lock_s = swipe_lock_s
        self.backend = backend
        self._last_scroll_time = 0.0

    def scroll_up(self, amount: Optional[int] = None) -> bool:
        """Execute discrete scroll up burst."""
        now = time.time()
        if now - self._last_scroll_time < self.swipe_lock_s:
            return False

        steps = amount if amount is not None else self.scroll_amount
        if self.backend is not None and hasattr(self.backend, "scroll"):
            self.backend.scroll(steps)
        else:
            try:
                import pyautogui
                pyautogui.scroll(steps * 50)
            except Exception:
                pass

        self._last_scroll_time = now
        return True

    def scroll_down(self, amount: Optional[int] = None) -> bool:
        """Execute discrete scroll down burst."""
        now = time.time()
        if now - self._last_scroll_time < self.swipe_lock_s:
            return False

        steps = amount if amount is not None else self.scroll_amount
        if self.backend is not None and hasattr(self.backend, "scroll"):
            self.backend.scroll(-steps)
        else:
            try:
                import pyautogui
                pyautogui.scroll(-steps * 50)
            except Exception:
                pass

        self._last_scroll_time = now
        return True
