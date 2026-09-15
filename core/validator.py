import ast
from typing import List, Tuple


def check_python_syntax(code: str) -> Tuple[bool, str | None]:
    try:
        ast.parse(code)
        return True, None
    except SyntaxError as err:
        message = f"خطای Syntax در خط {err.lineno}:\n{err.msg}"
        if err.text:
            message += f"\n\nکد مشکل‌دار:\n{err.text.strip()}"
        return False, message
    except Exception as err:
        return False, str(err)


def validate_lumina_code(code: str) -> List[str]:
    errors: List[str] = []
    tree = ast.parse(code)
    imports = {ast.unparse(node) for node in tree.body if isinstance(node, (ast.Import, ast.ImportFrom))}
    required = {"from manim import *", "from lumina import LuminaScene, QuoteCard, FormulaHighlightCard", "from lumina.themes import KURDISH_FONT"}
    for item in required - imports:
        errors.append(f"import ضروری پیدا نشد:\n{item}")
    generated = next((node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "GeneratedVideo"), None)
    if not generated or not any(isinstance(base, ast.Name) and base.id == "LuminaScene" for base in generated.bases):
        errors.append("کلاس GeneratedVideo(LuminaScene) پیدا نشد.")
    elif not any(isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "construct" for node in generated.body):
        errors.append("تابع construct(self) پیدا نشد.")
    expected = {"QuoteCard": {"text_content", "author", "font_name"}, "FormulaHighlightCard": {"latex_str", "label_text", "font_name"}}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name) or node.func.id not in expected:
            continue
        keywords = {keyword.arg for keyword in node.keywords if keyword.arg}
        invalid = keywords & {"quote", "font", "formula", "latex", "text"}
        if invalid:
            errors.append(f"{node.func.id} از پارامتر نامعتبر استفاده کرده است: {', '.join(sorted(invalid))}")
        if not node.args and not (keywords & expected[node.func.id]):
            errors.append(f"{node.func.id} باید یکی از پارامترهای معتبر را داشته باشد.")
    return errors


def validate_code(code: str) -> Tuple[bool, List[str]]:
    syntax_ok, syntax_error = check_python_syntax(code)
    if not syntax_ok:
        return False, [syntax_error or "Syntax error"]
    errors = validate_lumina_code(code)
    return not errors, errors
