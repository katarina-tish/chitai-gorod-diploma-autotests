"""UI-проверки из функционального чек-листа курсовой работы."""

import allure
import pytest

from src.pages import SearchPage


@pytest.mark.ui
@allure.title("Поисковая строка доступна на главной странице")
@allure.story("Поиск книги")
def test_home_page_has_search(search_page: SearchPage) -> None:
    """Проверяет доступность главного пользовательского действия — поиска."""
    search_page.open_home()
    with allure.step("Проверить отображение поисковой строки"):
        assert search_page.search_is_visible()


@pytest.mark.ui
@allure.title("Поиск книги по полному названию")
@allure.story("Поиск книги")
def test_search_by_full_title(search_page: SearchPage) -> None:
    """Проверяет выдачу по полному названию из чек-листа F-001."""
    search_page.open_search("Мастер и Маргарита")
    with allure.step("Проверить релевантный заголовок и карточки"):
        assert "мастер" in search_page.heading_text().lower()
        assert search_page.has_products()


@pytest.mark.ui
@allure.title("Поиск книги по части названия")
@allure.story("Поиск книги")
def test_search_by_partial_title(search_page: SearchPage) -> None:
    """Проверяет выдачу по части названия из чек-листа F-002."""
    search_page.open_search("мастер")
    with allure.step("Проверить наличие карточек в выдаче"):
        assert "мастер" in search_page.heading_text().lower()
        assert search_page.has_products()


@pytest.mark.ui
@allure.title("Поиск книг по автору")
@allure.story("Поиск книги")
def test_search_by_author(search_page: SearchPage) -> None:
    """Проверяет выдачу по автору из чек-листа F-003."""
    search_page.open_search("Булгаков")
    with allure.step("Проверить релевантный заголовок и карточки"):
        assert "булгаков" in search_page.heading_text().lower()
        assert search_page.has_products()


@pytest.mark.ui
@allure.title("Понятное состояние для несуществующего поискового запроса")
@allure.story("Поиск книги")
def test_unknown_search_shows_no_results(search_page: SearchPage) -> None:
    """Проверяет обработку несуществующего запроса из чек-листа F-005."""
    search_page.open_search("qzxyk no book 9874321")
    with allure.step("Проверить сообщение об отсутствии результатов"):
        assert "не принес результатов" in search_page.heading_text().lower()
