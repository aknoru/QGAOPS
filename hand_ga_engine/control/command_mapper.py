"""
LIVE HAND GA ENGINE — control/command_mapper.py
Mapping gestures to computer commands via configurable YAML profiles.

[IMPLEMENTED]
- GestureCommand dataclass
- Profile loader from profiles/*.yaml
- Dynamic profile switching (Mouse, Presentation, Media, Object3D)
- Whitelisted commands only (Zero arbitrary shell/code execution)
"""
from __future__ import annotations

import os
import pathlib
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import yaml

from mapping.expression_classes import get_expression_meta


@dataclass
class GestureCommand:
    """A semantic computer control command derived from a gesture.

    [IMPLEMENTED]
    """
    gesture: str
    confidence: float
    duration: float
    command: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    ga_opcode: str = "VECTOR"
    enabled: bool = True
    requires_confirmation: bool = False
    cooldown_s: float = 0.35
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gesture": self.gesture,
            "confidence": round(self.confidence, 3),
            "duration": round(self.duration, 3),
            "command": self.command,
            "parameters": self.parameters,
            "timestamp": round(self.timestamp, 4),
            "ga_opcode": self.ga_opcode,
            "enabled": self.enabled,
            "requires_confirmation": self.requires_confirmation,
            "cooldown_s": self.cooldown_s,
            "description": self.description,
        }


class CommandMapper:
    """Loads and resolves gesture commands based on active profile.

    [IMPLEMENTED]
    """

    DEFAULT_PROFILES_DIR = "profiles"

    def __init__(self, profile_name: str = "mouse", profiles_dir: Optional[str] = None) -> None:
        self.profiles_dir = profiles_dir or self.DEFAULT_PROFILES_DIR
        self.active_profile_name = profile_name.lower()
        self.profiles: Dict[str, Dict[str, Any]] = {}
        self.load_all_profiles()

    def load_all_profiles(self) -> None:
        """Load all YAML profiles from directory."""
        p_dir = pathlib.Path(self.profiles_dir)
        if not p_dir.exists():
            alt = pathlib.Path(__file__).resolve().parent.parent / "profiles"
            if alt.exists():
                p_dir = alt
            else:
                alt2 = pathlib.Path("hand_ga_engine/profiles")
                if alt2.exists():
                    p_dir = alt2
                else:
                    return

        for yml_file in p_dir.glob("*.yaml"):
            try:
                with open(yml_file, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict) and "name" in data:
                        self.profiles[data["name"].lower()] = data
            except Exception as e:
                print(f"[WARN] Failed to load profile {yml_file}: {e}")

    def set_profile(self, profile_name: str) -> bool:
        """Switch active control profile."""
        clean_name = profile_name.lower()
        if clean_name in self.profiles:
            self.active_profile_name = clean_name
            return True
        return False

    @property
    def current_profile(self) -> Dict[str, Any]:
        """Return the active profile data."""
        return self.profiles.get(self.active_profile_name, {})

    @property
    def current_settings(self) -> Dict[str, Any]:
        """Return the settings of the active profile."""
        return self.current_profile.get("settings", {})

    @property
    def active_mappings(self) -> Dict[str, GestureCommand]:
        """Return dict of gesture -> GestureCommand for active profile."""
        mappings = {}
        raw = self.current_profile.get("mappings", {})
        if isinstance(raw, dict):
            for gest, m in raw.items():
                if isinstance(m, dict):
                    mappings[gest] = GestureCommand(
                        gesture=gest,
                        confidence=m.get("min_confidence", self.current_settings.get("min_confidence", 0.70)),
                        duration=0.0,
                        command=m.get("command", m.get("action", "")),
                        parameters=m.get("parameters", {}),
                        requires_confirmation=m.get("requires_confirmation", m.get("confirmation", False)),
                        description=m.get("description", ""),
                    )
        elif isinstance(raw, list):
            for m in raw:
                if isinstance(m, dict) and "gesture" in m:
                    gest = m["gesture"]
                    mappings[gest] = GestureCommand(
                        gesture=gest,
                        confidence=m.get("min_confidence", self.current_settings.get("min_confidence", 0.70)),
                        duration=0.0,
                        command=m.get("command", m.get("action", "")),
                        parameters=m.get("parameters", {}),
                        requires_confirmation=m.get("requires_confirmation", m.get("confirmation", False)),
                        description=m.get("description", ""),
                    )
        return mappings

    def get_available_profiles(self) -> List[str]:
        """Return names of all loaded profiles."""
        return sorted(list(self.profiles.keys()))

    def map_gesture(
        self,
        gesture: str,
        confidence: float,
        duration: float = 0.0,
        extra_params: Optional[Dict[str, Any]] = None,
    ) -> Optional[GestureCommand]:
        """Map a recognized gesture to a structured GestureCommand.

        [IMPLEMENTED]
        """
        prof = self.current_profile
        mappings = prof.get("mappings", {})
        mapping = mappings.get(gesture)

        if not mapping or not mapping.get("enabled", True):
            return None

        meta = get_expression_meta(gesture)
        ga_opcode = meta.ga_operation if meta else "VECTOR"

        params = dict(mapping.get("parameters", {}))
        if "key" in mapping:
            params["key"] = mapping["key"]
        if extra_params:
            params.update(extra_params)

        cooldown_ms = mapping.get("cooldown_ms", 350)
        cooldown_s = cooldown_ms / 1000.0

        return GestureCommand(
            gesture=gesture,
            confidence=confidence,
            duration=duration,
            command=mapping.get("command", "NONE"),
            parameters=params,
            timestamp=time.time(),
            ga_opcode=ga_opcode,
            enabled=mapping.get("enabled", True),
            requires_confirmation=mapping.get("requires_confirmation", False),
            cooldown_s=cooldown_s,
            description=mapping.get("description", ""),
        )
