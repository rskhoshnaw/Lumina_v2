"""Base scene for Lumina-generated animations."""

from __future__ import annotations

from manim import BLACK, Scene


class LuminaScene(Scene):
    """
    Base Scene used by all generated Lumina videos.

    The class intentionally remains lightweight in v0.1.
    Future concerns such as theme management, transitions,
    language configuration, and shared animation helpers can be
    added without changing generated scene inheritance.
    """

    background_color = BLACK

    def setup(self) -> None:
        """Initialize Lumina defaults before scene construction."""
        super().setup()

        self.camera.background_color = self.background_color

