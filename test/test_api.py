"""API-проверки поискового сервиса из коллекции Postman курсовой работы."""

import allure
import pytest
from requests import Response

from src.api_client import ChitaiApiClient


SEARCH_SUGGESTS = "/web/api/v2/search/search-phrase-suggests"
SEARCH_PRODUCTS = "/web/api/v2/search/product"
POPULAR_PHRASES = "/web/api/v2/search/popular-search-phrases"


def assert_status(response: Response, expected_status: int) -> None:
    """Проверяет HTTP-статус и добавляет ответ к Allure-отчёту."""
    with allure.step(f"Проверить HTTP {expected_status}"):
        allure.attach(response.text, "Ответ API", allure.attachment_type.TEXT)
        assert response.status_code == expected_status, response.text


@pytest.mark.api
@allure.title("API: подсказки для валидной поисковой фразы")
@allure.story("Поисковый API")
def test_suggests_for_valid_phrase(api_client: ChitaiApiClient) -> None:
    """Проверяет API-001: подсказки для валидной фразы."""
    response = api_client.get(
        SEARCH_SUGGESTS,
        {
            "phrase": "мастер и маргарита",
            "suggests[page]": "1",
            "suggests[per-page]": "10",
        },
    )
    assert_status(response, 200)


@pytest.mark.api
@allure.title("API: поиск книг по валидной фразе")
@allure.story("Поисковый API")
def test_products_for_valid_phrase(api_client: ChitaiApiClient) -> None:
    """Проверяет API-002: поиск книг по валидной фразе."""
    response = api_client.get(
        SEARCH_PRODUCTS,
        {
            "phrase": "мастер и маргарита",
            "products[page]": "1",
            "products[per-page]": "10",
        },
    )
    assert_status(response, 200)


@pytest.mark.api
@allure.title("API: получение популярных поисковых фраз")
@allure.story("Поисковый API")
def test_popular_search_phrases(api_client: ChitaiApiClient) -> None:
    """Проверяет API-003: получение популярных фраз."""
    response = api_client.get(POPULAR_PHRASES, {})
    assert_status(response, 200)


@pytest.mark.api
@allure.title("API: короткая фраза для подсказок отклоняется")
@allure.story("Поисковый API")
def test_suggests_reject_short_phrase(api_client: ChitaiApiClient) -> None:
    """Проверяет API-004: короткая фраза возвращает HTTP 422."""
    response = api_client.get(
        SEARCH_SUGGESTS,
        {"phrase": "м", "suggests[page]": "1", "suggests[per-page]": "10"},
    )
    assert_status(response, 422)


@pytest.mark.api
@allure.title("API: неподдерживаемый POST к популярным фразам отклоняется")
@allure.story("Поисковый API")
def test_popular_phrases_reject_post(api_client: ChitaiApiClient) -> None:
    """Проверяет API-008: POST вместо GET возвращает HTTP 405."""
    response = api_client.post(POPULAR_PHRASES, {})
    assert_status(response, 405)
