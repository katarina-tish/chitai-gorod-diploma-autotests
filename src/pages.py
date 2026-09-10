"""Page Object для публичных страниц «Читай-город»."""

from urllib.parse import quote_plus

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as conditions
from selenium.webdriver.support.ui import WebDriverWait


class SearchPage:
    """Страница поисковой выдачи сайта."""

    _heading = (By.CSS_SELECTOR, "h1")
    _search_field = (By.CSS_SELECTOR, 'input[name="phrase"]')
    _product_link = (By.CSS_SELECTOR, 'a[href*="/product/"]')

    def __init__(self, driver: WebDriver, base_url: str, timeout: int) -> None:
        """Сохраняет драйвер, базовый адрес и явное ожидание."""
        self._driver = driver
        self._base_url = base_url.rstrip("/")
        self._wait = WebDriverWait(driver, timeout)

    def open_home(self) -> None:
        """Открывает главную страницу."""
        with allure.step("Открыть главную страницу магазина"):
            self._driver.get(self._base_url)
            self._wait.until(
                conditions.visibility_of_element_located(self._search_field)
            )

    def open_search(self, phrase: str) -> None:
        """Открывает выдачу по переданной поисковой фразе."""
        with allure.step(f"Открыть выдачу по запросу «{phrase}»"):
            url = f"{self._base_url}/search?phrase={quote_plus(phrase)}"
            self._driver.get(url)
            self._wait.until(
                conditions.visibility_of_element_located(self._heading)
            )

    def heading_text(self) -> str:
        """Возвращает текст заголовка поисковой страницы."""
        with allure.step("Получить заголовок выдачи"):
            return self._driver.find_element(*self._heading).text

    def has_products(self) -> bool:
        """Проверяет наличие хотя бы одной ссылки на карточку товара."""
        with allure.step("Проверить наличие карточек в выдаче"):
            return bool(self._driver.find_elements(*self._product_link))

    def search_is_visible(self) -> bool:
        """Проверяет доступность поисковой строки."""
        with allure.step("Проверить видимость строки поиска"):
            field = self._driver.find_element(*self._search_field)
            return field.is_displayed()
