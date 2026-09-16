"""Reusable visual cards for the Lumina animation engine."""

from __future__ import annotations

from typing import Any

from manim import (
    DOWN,
    GOLD,
    LEFT,
    MathTex,
    RIGHT,
    RoundedRectangle,
    UP,
    VGroup,
    WHITE,
    YELLOW,
)

from .themes import DEFAULT_COLORS, KURDISH_FONT
from .typography import make_text


class QuoteCard(VGroup):
    """
    Visual quote card.

    Public API:

        QuoteCard(
            text_content,
            author="",
            font_name="Rudaw",
            **kwargs
        )
    """

    def __init__(
        self,
        text_content: str,
        author: str = "",
        font_name: str = KURDISH_FONT,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        if not isinstance(text_content, str) or not text_content.strip():
            raise ValueError("text_content must be a non-empty string.")

        self.text_content = text_content
        self.author = author
        self.font_name = font_name

        card_width = float(kwargs.pop("card_width", 10.8))
        card_height = float(kwargs.pop("card_height", 4.8))
        corner_radius = float(kwargs.pop("corner_radius", 0.25))

        background_color = kwargs.pop(
            "background_color",
            DEFAULT_COLORS.background,
        )
        border_color = kwargs.pop(
            "border_color",
            DEFAULT_COLORS.accent,
        )
        border_width = float(kwargs.pop("border_width", 2.0))

        quote_font_size = float(kwargs.pop("quote_font_size", 32))
        author_font_size = float(kwargs.pop("author_font_size", 22))

        self.background = RoundedRectangle(
            width=card_width,
            height=card_height,
            corner_radius=corner_radius,
            stroke_color=border_color,
            stroke_width=border_width,
            fill_color=background_color,
            fill_opacity=0.95,
        )

        self.quote = make_text(
            text_content,
            font_name=font_name,
            font_size=quote_font_size,
            color=WHITE,
        )

        max_quote_width = card_width - 1.2

        if self.quote.width > max_quote_width:
            self.quote.scale_to_fit_width(max_quote_width)

        self.quote.move_to(self.background.get_center())

        self.author_text = None

        if author.strip():
            self.author_text = make_text(
                f"— {author.strip()}",
                font_name=font_name,
                font_size=author_font_size,
                color=GOLD,
            )

            self.author_text.next_to(
                self.background.get_bottom(),
                UP,
                buff=0.45,
            )

            self.author_text.align_to(
                self.background,
                RIGHT,
            )

            self.author_text.shift(LEFT * 0.55)

        components = [
            self.background,
            self.quote,
        ]

        if self.author_text is not None:
            components.append(self.author_text)

        self.add(*components)


class FormulaHighlightCard(VGroup):
    """
    Visual formula card.

    Public API:

        FormulaHighlightCard(
            latex_str,
            label_text="",
            font_name="Rudaw",
            **kwargs
        )
    """

    def __init__(
        self,
        latex_str: str,
        label_text: str = "",
        font_name: str = KURDISH_FONT,
        **kwargs: Any,
    ) -> None:
        super().__init__()

        if not isinstance(latex_str, str) or not latex_str.strip():
            raise ValueError("latex_str must be a non-empty string.")

        self.latex_str = latex_str
        self.label_text = label_text
        self.font_name = font_name

        card_width = float(kwargs.pop("card_width", 10.8))
        card_height = float(kwargs.pop("card_height", 4.8))

        border_color = kwargs.pop(
            "border_color",
            DEFAULT_COLORS.secondary,
        )
        background_color = kwargs.pop(
            "background_color",
            DEFAULT_COLORS.background,
        )
        border_width = float(kwargs.pop("border_width", 2.0))

        formula_color = kwargs.pop("formula_color", YELLOW)
        label_color = kwargs.pop("label_color", WHITE)

        formula_font_size = float(kwargs.pop("formula_font_size", 54))
        label_font_size = float(kwargs.pop("label_font_size", 26))

        self.background = RoundedRectangle(
            width=card_width,
            height=card_height,
            corner_radius=0.25,
            stroke_color=border_color,
            stroke_width=border_width,
            fill_color=background_color,
            fill_opacity=0.95,
        )

        self.formula = MathTex(
            latex_str,
            color=formula_color,
            font_size=formula_font_size,
        )

        max_formula_width = card_width - 1.2

        if self.formula.width > max_formula_width:
            self.formula.scale_to_fit_width(max_formula_width)

        if label_text.strip():
            self.label = make_text(
                label_text,
                font_name=font_name,
                font_size=label_font_size,
                color=label_color,
            )

            content = VGroup(
                self.formula,
                self.label,
            ).arrange(
                DOWN,
                buff=0.45,
            )

            content.move_to(self.background.get_center())

            self.add(
                self.background,
                self.formula,
                self.label,
            )

        else:
            self.label = None
            self.formula.move_to(self.background.get_center())

            self.add(
                self.background,
                self.formula,
            )
