"""Theme constants for Lumina."""

from __future__ import annotations

from dataclasses import dataclass

from manim import BLACK, BLUE, GOLD, GREEN, WHITE


KURDISH_FONT = "Rudaw"


@dataclass(frozen=True)
class LuminaColors:
    """Core colors used by Lumina components."""

    background: object = BLACK
    foreground: object = WHITE
    accent: object = BLUE
    secondary: object = GREEN
    highlight: object = GOLD


DEFAULT_COLORS = LuminaColors()


__all__ = [
    "KURDISH_FONT",
    "LuminaColors",
    "DEFAULT_COLORS",
]

