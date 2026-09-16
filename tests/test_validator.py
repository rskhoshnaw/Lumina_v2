from core.validator import validate_code

def test_valid_generated_code():
    code = """
from manim import *
from lumina import LuminaScene, QuoteCard, FormulaHighlightCard
from lumina.themes import KURDISH_FONT

class GeneratedVideo(LuminaScene):
    def construct(self):
        card = QuoteCard(text_content="سڵاو", font_name=KURDISH_FONT)
        self.add(card)
"""
    is_valid, errors = validate_code(code)
    assert is_valid is True
    assert len(errors) == 0

def test_missing_mandatory_imports_and_class():
    code = """
class Video(Scene):
    def construct(self):
        pass
"""
    is_valid, errors = validate_code(code)
    assert is_valid is False
    assert any("from manim import *" in e for e in errors)
    assert any("Missing mandatory class" in e for e in errors)

def test_forbidden_parameters_are_caught():
    code = """
from manim import *
class GeneratedVideo(LuminaScene):
    def construct(self):
        # Gemini often hallucinates these parameters
        card = QuoteCard(quote="سڵاو", font="Rudaw")
"""
    is_valid, errors = validate_code(code)
    assert is_valid is False
    assert any("Forbidden parameter 'quote'" in e for e in errors)
    assert any("Forbidden parameter 'font'" in e for e in errors)

def test_syntax_error_handling():
    code = """
from manim import *
class GeneratedVideo(LuminaScene) # Missing colon
    def construct(self):
        pass
"""
    is_valid, errors = validate_code(code)
    assert is_valid is False
    assert any("Syntax Error" in e for e in errors)
