from pathlib import Path

from lumina.typography import (
    TextDirection,
    detect_text_direction,
    find_rudaw_font,
    resolve_font_name,
)


def test_persian_is_rtl():
    assert detect_text_direction("fa") == TextDirection.RTL


def test_kurdish_is_rtl():
    assert detect_text_direction("ckb") == TextDirection.RTL


def test_arabic_is_rtl():
    assert detect_text_direction("ar") == TextDirection.RTL


def test_english_is_ltr():
    assert detect_text_direction("en") == TextDirection.LTR


def test_unknown_language_defaults_to_ltr():
    assert detect_text_direction("xx") == TextDirection.LTR


def test_rudaw_font_name():
    assert resolve_font_name("Rudaw") == "Rudaw"
    assert resolve_font_name("rudaw") == "Rudaw"


def test_rudaw_font_exists():
    font_path = find_rudaw_font()

    assert isinstance(font_path, Path)
    assert font_path.is_file()
    assert font_path.suffix.lower() == ".ttf"
