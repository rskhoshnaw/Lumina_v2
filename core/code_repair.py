"""Component for repairing hallucinated or faulty generated code."""
import re
from pathlib import Path
from typing import Dict, Any
from core.ai_provider import AIProvider

class CodeRepairer:
    def __init__(self, provider: AIProvider, prompt_file: Path):
        self.provider = provider
        self.system_prompt = prompt_file.read_text(encoding="utf-8")

    def repair(self, blueprint: Dict[str, Any], bad_code: str, error_log: str) -> str:
        prompt = (
            "ORIGINAL BLUEPRINT:\n"
            f"{blueprint}\n\n"
            "FAULTY CODE:\n"
            f"{bad_code}\n\n"
            "ERROR LOG:\n"
            f"{error_log}\n\n"
            "Please provide the corrected Python code inside a ```python block."
        )
        response = self.provider.generate_text(
            prompt=prompt,
            system_prompt=self.system_prompt
        )
        return self._clean_code(response)

    def _clean_code(self, text: str) -> str:
        """Extract clean Python code from Markdown fences."""
        match = re.search(r'```python\s*(.*?)\s*```', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return text.strip()
