"""
LIVE HAND GA ENGINE — control/keyboard_controller.py
Strictly whitelisted keyboard action dispatcher.

[IMPLEMENTED]
- Restricts keypresses to explicitly safe keys (arrows, navigation, media keys)
- Zero arbitrary command or keystroke injection
- Mockable backend for test safety
"""
from __future__ import annotations

import time
from typing import Any, List, Optional, Set


class KeyboardController:
    """Dispatches whitelisted keyboard actions safely."""

    # Explicit whitelist of permitted keys
    ALLOWED_KEYS: Set[str] = {
        "left", "right", "up", "down",
        "pageup", "pagedown", "home", "end",
        "space", "enter", "escape", "tab",
        "f5", "b", "w",
        "playpause", "prevtrack", "nexttrack", "stop",
        "volumeup", "volumedown", "volumemute",
    }

    def __init__(self, backend: Any = None) -> None:
        self.backend = backend
        self.last_key_sent: Optional[str] = None
        self.last_key_time: float = 0.0

    def press_key(self, key_name: str) -> bool:
        """Press a single whitelisted key."""
        clean_key = key_name.lower().strip()
        if clean_key not in self.ALLOWED_KEYS:
            print(f"[SECURITY REJECT] Disallowed key rejected: '{key_name}'")
            return False

        if self.backend is not None and hasattr(self.backend, "press"):
            self.backend.press(clean_key)
        else:
            try:
                import pyautogui
                pyautogui.press(clean_key)
            except Exception:
                pass

        self.last_key_sent = clean_key
        self.last_key_time = time.time()
        return True

    def hotkey(self, *keys: str) -> bool:
        """Press a key combination if all are whitelisted."""
        clean_keys = [k.lower().strip() for k in keys]
        for k in clean_keys:
            if k not in self.ALLOWED_KEYS and k not in ("ctrl", "alt", "shift"):
                print(f"[SECURITY REJECT] Disallowed modifier/key: '{k}'")
                return False

        if self.backend is not None and hasattr(self.backend, "hotkey"):
            self.backend.hotkey(*clean_keys)
        else:
            try:
                import pyautogui
                pyautogui.hotkey(*clean_keys)
            except Exception:
                pass

        self.last_key_sent = "+".join(clean_keys)
        self.last_key_time = time.time()
        return True
