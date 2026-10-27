# tests/conftest.py
"""Shared pytest fixtures and path setup for the hand GA engine."""
import sys
import pathlib

# Ensure the project root is on sys.path so all modules resolve correctly
_project_root = pathlib.Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))
