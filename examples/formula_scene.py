from manim import FadeIn, FadeOut

from lumina import FormulaHighlightCard, LuminaScene, QuoteCard
from lumina.themes import KURDISH_FONT


class LuminaFormulaDemo(LuminaScene):
    def construct(self):
        quote = QuoteCard(
            text_content="هێز و خێرایی پەیوەندییەکی گرنگیان هەیە.",
            author="Lumina Studio",
            font_name=KURDISH_FONT,
        )

        self.play(FadeIn(quote))
        self.wait(1.5)

        self.play(FadeOut(quote))

        formula = FormulaHighlightCard(
            latex_str=r"F = ma",
            label_text="یاسای دووەمی نیوتن",
            font_name=KURDISH_FONT,
        )

        self.play(FadeIn(formula))
        self.wait(2)
