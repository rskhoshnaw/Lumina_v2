import json
import re
from pathlib import Path
from typing import Any, Dict

from .ai_provider import AIProvider


class CodeGenerator:
    """Convert a video blueprint into Python/Manim source code."""

    def __init__(self, provider: AIProvider, prompt_file: Path):
        self.provider = provider
        self.prompt_file = prompt_file
        self.system_prompt = prompt_file.read_text(encoding="utf-8")

    def generate(self, blueprint: Dict[str, Any]) -> str:
        prompt = "VIDEO BLUEPRINT:\n\n" + json.dumps(blueprint, ensure_ascii=False, indent=2)
        raw = self.provider.generate_text(prompt=prompt, system_prompt=self.system_prompt)
        return self.clean_code(raw)

    @staticmethod
    def clean_code(raw_text: str) -> str:
        if not raw_text:
            return ""
        text = raw_text.strip()
        match = re.search(r"```(?:python|py)?\s*(.*?)```", text, flags=re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return re.sub(r"^```(?:python|py)?\s*|\s*```$", "", text, flags=re.IGNORECASE).strip()
