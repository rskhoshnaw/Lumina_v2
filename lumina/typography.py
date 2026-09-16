"""Typography helpers for the Lumina animation engine"""
from __future__ import annotations
from contextlib import contextmanager
from enum import Enum
from pathlib import Path
from typing import Iterator
import re

from manim import Text, WHITE
from manim.mobject.text.text_mobject import register_font
from .utils import find_rudaw_font, is_rudaw_font

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    HAS_RTL_LIBS = True
except ImportError:
    HAS_RTL_LIBS = False

class TextDirection(str, Enum):
    LTR = "ltr"
    RTL = "rtl"

RTL_LANGUAGES = frozenset({"fa", "ckb", "ar"})
LTR_LANGUAGES = frozenset({"en"})

def detect_text_direction(language: str | None) -> TextDirection:
    normalized = (language or "").strip().lower()
    if normalized in RTL_LANGUAGES:
        return TextDirection.RTL
    return TextDirection.LTR

def resolve_font_name(font_name: str | None) -> str:
    normalized = (font_name or "").strip()
    if not normalized:
        return "sans-serif"
    if is_rudaw_font(normalized):
        return "Rudaw"
    return normalized

@contextmanager
def registered_font(font_name: str | None) -> Iterator[None]:
    if is_rudaw_font(font_name):
        font_path = find_rudaw_font()
        with register_font(font_path):
            yield
        return
    yield

def shape_rtl_text(text: str) -> str:
    if not HAS_RTL_LIBS:
        return text
    
    configuration = {
        'delete_harakat': False,
        'support_ligatures': True,
        'use_unshaped_instead_of_isolated': True
    }
    reshaper = arabic_reshaper.ArabicReshaper(configuration=configuration)
    reshaped_text = reshaper.reshape(text)
    return get_display(reshaped_text)

def has_rtl_chars(text: str) -> bool:
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text))

def make_text(
    text: str,
    font_name: str | None = None,
    font_size: float = 32.0,
    color=WHITE,
    weight: str = "NORMAL",
    language: str | None = None,
    **kwargs,
) -> Text:
    resolved_font = resolve_font_name(font_name)
    final_text = text
    
    if has_rtl_chars(text) or detect_text_direction(language) == TextDirection.RTL:
        final_text = shape_rtl_text(text)

    with registered_font(resolved_font):
        return Text(
            final_text,
            font=resolved_font,
            font_size=font_size,
            color=color,
            weight=weight,
            **kwargs,
        )

def rudaw_font_path() -> Path:
    return find_rudaw_font()
