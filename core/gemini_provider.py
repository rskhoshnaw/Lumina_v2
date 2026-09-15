import os
from typing import Any, Dict, Optional, Sequence

from google import genai

from .ai_provider import AIProvider

DEFAULT_MODELS = ("gemini-flash-latest", "gemini-flash-lite-latest", "gemini-pro-latest")


class GeminiProvider(AIProvider):
    """Google Gemini implementation with fallback for transient failures."""

    def __init__(self, api_key: Optional[str] = None, models: Optional[Sequence[str]] = None):
        self.api_key = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY تنظیم نشده است.")
        self.models = tuple(models or DEFAULT_MODELS)
        if not self.models:
            raise ValueError("حداقل یک مدل Gemini لازم است.")
        self.client = genai.Client(api_key=self.api_key)
        self.last_model: Optional[str] = None

    def generate_text(self, prompt: str, system_prompt: Optional[str] = None, response_schema: Optional[Dict[str, Any]] = None) -> str:
        contents = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        last_error: Optional[Exception] = None
        for model_name in self.models:
            try:
                config = None
                if response_schema:
                    config = {"response_mime_type": "application/json", "response_schema": response_schema}
                response = self.client.models.generate_content(model=model_name, contents=contents, config=config)
                response_text = getattr(response, "text", None)
                if not response_text:
                    raise RuntimeError("Gemini پاسخ متنی برنگرداند.")
                self.last_model = model_name
                return response_text.strip()
            except Exception as err:
                last_error = err
                error_text = str(err).upper()
                if any(marker in error_text for marker in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "TIMEOUT")):
                    continue
                raise RuntimeError(f"خطا در Gemini ({model_name}):\n{err}") from err
        raise RuntimeError(f"هیچ‌یک از مدل‌های Gemini پاسخ ندادند.\n\nآخرین خطا:\n{last_error}")
