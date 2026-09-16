from manim import MathTex, RoundedRectangle, Text, VGroup

from lumina import FormulaHighlightCard, QuoteCard


def test_quote_card_is_vgroup():
    card = QuoteCard(
        text_content="سڵاو لە Lumina",
        author="Lumina Studio",
        font_name="Rudaw",
    )

    assert isinstance(card, VGroup)
    assert isinstance(card.background, RoundedRectangle)
    assert isinstance(card.quote, Text)
    assert card.author_text is not None


def test_quote_card_without_author():
    card = QuoteCard(
        text_content="Hello from Lumina",
        font_name="Rudaw",
    )

    assert card.author_text is None
    assert len(card.submobjects) == 2


def test_formula_card_is_vgroup():
    card = FormulaHighlightCard(
        latex_str=r"F = ma",
        label_text="یاسای دووەمی نیوتن",
        font_name="Rudaw",
    )

    assert isinstance(card, VGroup)
    assert isinstance(card.background, RoundedRectangle)
    assert isinstance(card.formula, MathTex)
    assert isinstance(card.label, Text)


def test_formula_card_without_label():
    card = FormulaHighlightCard(
        latex_str=r"E = mc^2",
        font_name="Rudaw",
    )

    assert card.label is None
    assert len(card.submobjects) == 2


def test_empty_quote_is_rejected():
    try:
        QuoteCard(text_content="")
    except ValueError:
        pass
    else:
        raise AssertionError("Empty quote text must raise ValueError.")


def test_empty_formula_is_rejected():
    try:
        FormulaHighlightCard(latex_str="")
    except ValueError:
        pass
    else:
        raise AssertionError("Empty formula must raise ValueError.")
        
