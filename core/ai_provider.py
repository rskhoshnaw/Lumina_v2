from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class AIProvider(ABC):
    """
    رابط پایه برای سرویس‌های هوش مصنوعی Lumina.

    در حال حاضر Gemini Provider استفاده می‌شود،
    اما معماری طوری طراحی شده که Providerهای دیگر
    بعداً بدون تغییر موتور اصلی اضافه شوند.
    """

    @abstractmethod
    def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        تولید متن توسط مدل هوش مصنوعی.

        Args:
            prompt: متن اصلی درخواست.
            system_prompt: دستور سیستمی اختیاری.
            response_schema: ساختار مورد انتظار پاسخ، در صورت نیاز.

        Returns:
            متن تولیدشده توسط مدل.

        Raises:
            NotImplementedError:
                اگر Provider پیاده‌سازی نشده باشد.
        """
        raise NotImplementedError
