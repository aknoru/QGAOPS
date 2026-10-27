"""
LIVE HAND GA ENGINE — mapping/dataset_classes.py
Centralized Kaggle LeapGestRecog 6-class definitions and utilities.

[IMPLEMENTED] Exactly 6 static expression classes:
    0: PALM
    1: L_GESTURE
    2: FIST
    3: THUMB
    4: INDEX
    5: OK
"""
from __future__ import annotations

from typing import Dict, List, Optional

CLASS_NAMES: Dict[int, str] = {
    0: "PALM",
    1: "L_GESTURE",
    2: "FIST",
    3: "THUMB",
    4: "INDEX",
    5: "OK",
}

NAME_TO_ID: Dict[str, int] = {v: k for k, v in CLASS_NAMES.items()}

FOLDER_TO_NAME: Dict[str, str] = {
    "01_palm": "PALM",
    "02_l": "L_GESTURE",
    "03_fist": "FIST",
    "05_thumb": "THUMB",
    "06_index": "INDEX",
    "07_ok": "OK",
}

NAME_TO_FOLDER: Dict[str, str] = {v: k for k, v in FOLDER_TO_NAME.items()}

UNKNOWN_CLASS: str = "UNKNOWN"
NUM_CLASSES: int = len(CLASS_NAMES)


def get_class_name(class_id: int) -> str:
    """Return class name from integer ID (defaulting to UNKNOWN)."""
    return CLASS_NAMES.get(class_id, UNKNOWN_CLASS)


def get_class_id(class_name: str) -> Optional[int]:
    """Return integer ID from class name."""
    return NAME_TO_ID.get(class_name.upper())
