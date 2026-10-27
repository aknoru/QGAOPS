"""
LIVE HAND GA ENGINE — control/application_controller.py
Application-level controller for presentations and media player workflows.

[IMPLEMENTED]
- Presentation slideshow navigation (prev, next, start, escape)
- Media player playback commands (play/pause, next, previous, stop)
- Whitelisted and safe dispatching via KeyboardController
"""
from __future__ import annotations

from typing import Optional
from control.keyboard_controller import KeyboardController


class ApplicationController:
    """Dispatches application-specific commands safely."""

    def __init__(self, keyboard: Optional[KeyboardController] = None) -> None:
        self.keyboard = keyboard or KeyboardController()

    # -----------------------------------------------------------------------
    # Presentation Profile Actions
    # -----------------------------------------------------------------------
    def next_slide(self) -> bool:
        """Advance to next slide."""
        return self.keyboard.press_key("right")

    def prev_slide(self) -> bool:
        """Return to previous slide."""
        return self.keyboard.press_key("left")

    def start_presentation(self) -> bool:
        """Start full-screen presentation."""
        return self.keyboard.press_key("f5")

    def escape_presentation(self) -> bool:
        """Exit presentation or restore view."""
        return self.keyboard.press_key("escape")

    def black_screen(self) -> bool:
        """Toggle blank/black slide screen."""
        return self.keyboard.press_key("b")

    # Method aliases for flexibility
    slide_next = next_slide
    slide_previous = prev_slide
    presentation_start = start_presentation
    presentation_stop = escape_presentation

    # -----------------------------------------------------------------------
    # Media Profile Actions
    # -----------------------------------------------------------------------
    def media_play_pause(self) -> bool:
        """Toggle media play/pause."""
        return self.keyboard.press_key("playpause") or self.keyboard.press_key("space")

    def media_next(self) -> bool:
        """Skip to next media track."""
        return self.keyboard.press_key("nexttrack")

    def media_previous(self) -> bool:
        """Skip to previous media track."""
        return self.keyboard.press_key("prevtrack")

    def media_stop(self) -> bool:
        """Stop media playback."""
        return self.keyboard.press_key("stop")
