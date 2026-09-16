"""Internal utilities for the Lumina animation engine."""

from __future__ import annotations

from pathlib import Path


_PACKAGE_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _PACKAGE_DIR.parent
_FONT_DIR = _PROJECT_ROOT / "font"


def get_project_root() -> Path:
    """Return the root directory of the Lumina project."""
    return _PROJECT_ROOT


def get_font_directory() -> Path:
    """Return the repository font directory."""
    return _FONT_DIR


def find_rudaw_font() -> Path:
    """
    Find the preferred Rudaw font shipped with the repository.

    The regular font is preferred for general text rendering.
    """
    candidates = (
        _FONT_DIR / "rudaw_regular.ttf",
        _FONT_DIR / "rudawregular.ttf",
        _FONT_DIR / "rudaw_bold.ttf",
    )

    for path in candidates:
        if path.is_file():
            return path

    raise FileNotFoundError(
        "Rudaw font was not found. Expected one of: "
        "font/rudaw_regular.ttf, "
        "font/rudawregular.ttf, "
        "font/rudaw_bold.ttf"
    )


def is_rudaw_font(font_name: str | None) -> bool:
    """Return whether a font name refers to the Lumina Rudaw family."""
    if not font_name:
        return False

    normalized = font_name.strip().lower()
    return normalized == "rudaw"

