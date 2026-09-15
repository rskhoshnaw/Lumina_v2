import json
from pathlib import Path
from typing import Any, Dict

from .ai_provider import AIProvider


class ContentPlanner:
    """Convert a user's request into a structured video blueprint."""

    def __init__(self, provider: AIProvider, prompt_file: Path):
        self.provider = provider
        self.prompt_file = prompt_file
        self.system_prompt = prompt_file.read_text(encoding="utf-8")

    def create_blueprint(self, user_request: str, settings: Dict[str, Any]) -> Dict[str, Any]:
        prompt = (
            "USER REQUEST:\n"
            f"{user_request}\n\nUSER SETTINGS:\n"
            f"{json.dumps(settings, ensure_ascii=False, indent=2)}\n\n"
            "Create the video blueprint."
        )
        raw = self.provider.generate_text(prompt=prompt, system_prompt=self.system_prompt)
        blueprint = self._parse_json(raw)
        self._validate_blueprint(blueprint)
        return blueprint

    @staticmethod
    def _parse_json(raw: str) -> Dict[str, Any]:
        text = raw.strip()
        if text.startswith("```"):
            text = "\n".join(line for line in text.splitlines() if not line.strip().startswith("```")).strip()
        try:
            result = json.loads(text)
        except json.JSONDecodeError as err:
            raise RuntimeError("Gemini یک Blueprint معتبر JSON تولید نکرد.\n\n" f"پاسخ دریافت‌شده:\n{raw}") from err
        if not isinstance(result, dict):
            raise RuntimeError("Blueprint باید یک شیء JSON باشد.")
        return result

    @staticmethod
    def _validate_blueprint(blueprint: Dict[str, Any]) -> None:
        required = ("title", "category", "language", "audience", "duration_seconds", "style", "scenes")
        missing = [key for key in required if key not in blueprint]
        if missing:
            raise RuntimeError(f"Blueprint ناقص است. فیلدهای مفقود: {missing}")
        if not isinstance(blueprint["scenes"], list) or not blueprint["scenes"]:
            raise RuntimeError("فیلد scenes باید یک فهرستِ غیرخالی باشد.")
        for index, scene in enumerate(blueprint["scenes"], start=1):
            if not isinstance(scene, dict):
                raise RuntimeError(f"Scene شماره {index} معتبر نیست.")
            scene.setdefault("id", f"scene_{index}")
            scene.setdefault("title", f"Scene {index}")
            scene.setdefault("duration", 10)
            scene.setdefault("narration", "")
            scene.setdefault("visual_description", "")
            scene.setdefault("text_elements", [])
            scene.setdefault("formulas", [])
            scene.setdefault("animation_notes", [])
