"""Typography helpers for the Lumina animation engine."""

from __future__ import annotations

from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Iterator

from manim import Text, WHITE
from manim.mobject.text.text_mobject import register_font

from .utils import find_rudaw_font, is_rudaw_font


class TextDirection(str, Enum):
    """Logical text direction."""

    LTR = "ltr"
    RTL = "rtl"


RTL_LANGUAGES = frozenset({"fa", "ckb", "ar"})
LTR_LANGUAGES = frozenset({"en"})


def detect_text_direction(language: str | None) -> TextDirection:
    """
    Determine the logical text direction from a language code.

    This is intentionally limited to direction metadata in v0.1.
    It does not attempt bidirectional text shaping.
    """
    normalized = (language or "").strip().lower()

    if normalized in RTL_LANGUAGES:
        return TextDirection.RTL

    return TextDirection.LTR


def resolve_font_name(font_name: str | None) -> str:
    """
    Resolve a Lumina font name to the Pango family name.

    For v0.1, Rudaw is the only repository-managed font family.
    """
    normalized = (font_name or "").strip()

    if not normalized:
        return "sans-serif"

    if is_rudaw_font(normalized):
        return "Rudaw"

    return normalized


@contextmanager
def registered_font(font_name: str | None) -> Iterator[None]:
    """
    Register a repository-managed font for the lifetime of the context.

    Non-Lumina/system fonts do not require registration here.
    """
    if is_rudaw_font(font_name):
        font_path = find_rudaw_font()

        with register_font(font_path):
            yield

        return

    yield


def make_text(
    text: str,
    *,
    font_name: str | None = None,
    font_size: float = 36,
    color=WHITE,
    weight: str = "NORMAL",
    language: str | None = None,
    **kwargs,
) -> Text:
    """
    Create a Manim Text object using Lumina typography rules.

    v0.1 handles font selection and logical text direction.
    Full RTL shaping is intentionally deferred to a later typography stage.
    """
    del language  # Direction metadata is exposed separately for future use.

    resolved_font = resolve_font_name(font_name)

    with registered_font(resolved_font):
        return Text(
            text,
            font=resolved_font,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )


def rudaw_font_path() -> Path:
    """Return the repository path of the preferred Rudaw font."""
    return find_rudaw_font()


__all__ = [
    "TextDirection",
    "RTL_LANGUAGES",
    "LTR_LANGUAGES",
    "detect_text_direction",
    "resolve_font_name",
    "registered_font",
    "make_text",
    "rudaw_font_path",
]

