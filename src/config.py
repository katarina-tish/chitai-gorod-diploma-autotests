"""Настройки запуска без секретов в исходном коде."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Адреса стенда и параметры браузера."""

    ui_url: str
    api_url: str
    headless: bool
    timeout_seconds: int


def load_settings() -> Settings:
    """Возвращает настройки из окружения с безопасными значениями."""
    return Settings(
        ui_url=os.getenv("CHITAI_UI_URL", "https://www.chitai-gorod.ru"),
        api_url=os.getenv("CHITAI_API_URL", "https://web-agr.chitai-gorod.ru"),
        headless=os.getenv("HEADLESS", "true").lower() == "true",
        timeout_seconds=int(os.getenv("TIMEOUT_SECONDS", "20")),
    )
