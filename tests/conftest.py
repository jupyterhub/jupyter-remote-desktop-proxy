from os import getenv

import pytest
from playwright.sync_api import sync_playwright

HEADLESS = getenv("HEADLESS", "1") == "1"


@pytest.fixture()
def browser():
    # browser_type in ["chromium", "firefox", "webkit"]
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=HEADLESS)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.clear_cookies()
        browser.close()
