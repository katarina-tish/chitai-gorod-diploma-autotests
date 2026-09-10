"""Клиент безопасных публичных поисковых API «Читай-город».

Токен создаётся анонимным штатным маршрутом на время тестовой сессии и нигде
не сохраняется. Операции с заказами, оплатой и персональными данными
отсутствуют.
"""

from typing import Any
from uuid import uuid4

import allure
import requests
from requests import Response

from src.config import Settings


class ChitaiApiClient:
    """Инкапсулирует HTTP-запросы поискового сервиса."""

    def __init__(self, settings: Settings) -> None:
        """Создаёт HTTP-сессию без захардкоженных токенов."""
        self._settings = settings
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Accept": "application/json",
                "Origin": settings.ui_url,
                "Referer": f"{settings.ui_url}/",
                "User-Agent": "Skypro-diploma-autotests/1.0",
                "initial-feature": "web",
                "platform": "web",
                "shop-brand": "chitai-gorod",
                "user-id": str(uuid4()),
            }
        )

    def authenticate_anonymously(self) -> str:
        """Получает временный анонимный Bearer-токен и возвращает его."""
        with allure.step("Получить временный анонимный токен API"):
            response = self._session.post(
                f"{self._settings.api_url}/web/api/v1/auth/anonymous",
                json={},
                timeout=self._settings.timeout_seconds,
            )
            assert response.status_code == 201, response.text
            payload: dict[str, Any] = response.json()
            token = str(payload["token"]["accessToken"])
            self._session.headers["Authorization"] = token
            return str(token)

    def get(self, path: str, params: dict[str, str]) -> Response:
        """Выполняет GET-запрос к относительному пути API."""
        with allure.step(f"Отправить GET {path}"):
            return self._session.get(
                f"{self._settings.api_url}{path}",
                params=params,
                timeout=self._settings.timeout_seconds,
            )

    def post(self, path: str, payload: dict[str, str]) -> Response:
        """Выполняет POST-запрос для негативной проверки метода."""
        with allure.step(f"Отправить POST {path}"):
            return self._session.post(
                f"{self._settings.api_url}{path}",
                json=payload,
                timeout=self._settings.timeout_seconds,
            )

