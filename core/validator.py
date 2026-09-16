"""Validator for generated Lumina Python code."""
from __future__ import annotations
import ast
from typing import Tuple, List

def validate_code(code: str) -> Tuple[bool, List[str]]:
    errors = []
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, [f"Syntax Error: {e.msg} at line {e.lineno}"]

    class LuminaVisitor(ast.NodeVisitor):
        def __init__(self):
            self.has_class = False
            self.has_construct = False
            self.errors = []

        def visit_ClassDef(self, node: ast.ClassDef):
            if node.name == "GeneratedVideo":
                self.has_class = True
                bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                if "LuminaScene" not in bases:
                    self.errors.append("GeneratedVideo must inherit from LuminaScene.")
                for child in node.body:
                    if isinstance(child, ast.FunctionDef) and child.name == "construct":
                        self.has_construct = True
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id == "QuoteCard":
                    allowed = {"text_content", "author", "font_name"}
                    for kw in node.keywords:
                        if kw.arg not in allowed:
                            self.errors.append(f"Invalid param '{kw.arg}' in QuoteCard. Use: {allowed}")
                elif node.func.id == "FormulaHighlightCard":
                    allowed = {"latex_str", "label_text", "font_name"}
                    for kw in node.keywords:
                        if kw.arg not in allowed:
                            self.errors.append(f"Invalid param '{kw.arg}' in FormulaHighlightCard. Use: {allowed}")
            self.generic_visit(node)

    visitor = LuminaVisitor()
    visitor.visit(tree)
    
    if not visitor.has_class:
        errors.append("Missing mandatory class: class GeneratedVideo(LuminaScene)")
    if not visitor.has_construct:
        errors.append("Missing mandatory method: def construct(self)")
        
    errors.extend(visitor.errors)
    if "from manim import *" not in code:
        errors.append("Missing required import: from manim import *")

    return len(errors) == 0, errors
