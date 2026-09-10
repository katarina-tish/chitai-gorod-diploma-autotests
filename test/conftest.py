"""Общие фикстуры для UI- и API-тестов."""

from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from src.api_client import ChitaiApiClient
from src.config import Settings, load_settings
from src.pages import SearchPage


@pytest.fixture(scope="session")
def settings() -> Settings:
    """Возвращает единые параметры тестового запуска."""
    return load_settings()


@pytest.fixture(scope="session")
def driver(settings: Settings) -> Generator[WebDriver, None, None]:
    """Создаёт чистый Chrome без chromedriver в репозитории."""
    options = Options()
    options.add_argument("--window-size=1440,1000")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    if settings.headless:
        options.add_argument("--headless=new")
    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(settings.timeout_seconds)
    yield browser
    browser.quit()


@pytest.fixture()
def search_page(driver: WebDriver, settings: Settings) -> SearchPage:
    """Возвращает Page Object поисковой страницы."""
    return SearchPage(driver, settings.ui_url, settings.timeout_seconds)


@pytest.fixture()
def api_client(settings: Settings) -> ChitaiApiClient:
    """Возвращает авторизованный анонимный API-клиент."""
    client = ChitaiApiClient(settings)
    client.authenticate_anonymously()
    return client
