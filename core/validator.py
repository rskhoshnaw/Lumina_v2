"""Validator for generated Lumina Python code."""
from __future__ import annotations
import ast
from typing import Tuple, List

def validate_code(code: str) -> Tuple[bool, List[str]]:
    """
    Parse and validate generated Manim/Lumina code.
    Returns (is_valid, list_of_error_messages).
    """
    errors = []
    
    # 1. Syntax Check
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, [f"Syntax Error: {e.msg} at line {e.lineno}"]

    # 2. Structural & API Check
    class LuminaVisitor(ast.NodeVisitor):
        def __init__(self):
            self.has_class = False
            self.has_construct = False
            self.errors = []

        def visit_ClassDef(self, node: ast.ClassDef):
            if node.name == "GeneratedVideo":
                self.has_class = True
                
                # Check Base Class
                bases = [b.id for b in node.bases if isinstance(b, ast.Name)]
                if "LuminaScene" not in bases:
                    self.errors.append("GeneratedVideo must inherit from LuminaScene.")
                
                # Check for construct method
                for child in node.body:
                    if isinstance(child, ast.FunctionDef) and child.name == "construct":
                        self.has_construct = True
                        
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call):
            # Enforce API parameter rules for Cards
            if isinstance(node.func, ast.Name) and node.func.id in ("QuoteCard", "FormulaHighlightCard"):
                forbidden = {"quote", "font", "formula", "latex", "text"}
                for kw in node.keywords:
                    if kw.arg in forbidden:
                        self.errors.append(f"Forbidden parameter '{kw.arg}' used in {node.func.id}.")
            self.generic_visit(node)

    visitor = LuminaVisitor()
    visitor.visit(tree)
    
    if not visitor.has_class:
        errors.append("Missing mandatory class: class GeneratedVideo(LuminaScene)")
    if not visitor.has_construct:
        errors.append("Missing mandatory method: def construct(self)")
        
    errors.extend(visitor.errors)

    # 3. Import Checks (String-based for strictness matching prompt instructions)
    if "from manim import *" not in code:
        errors.append("Missing required import: from manim import *")

    is_valid = len(errors) == 0
    return is_valid, errors
