import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser_context():
    """Sets up the browser instance for the test session."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True if headless mode is preferred
        context = browser.new_context()
        yield context
        context.close()
        browser.close()

@pytest.fixture
def page(browser_context):

    pg = browser_context.new_page()
    yield pg
    pg.close()