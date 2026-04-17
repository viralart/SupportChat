import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage

@pytest.fixture
def logged_in_page(page: Page, base_url: str):
    """Fixture that logs in and returns the authenticated page context."""
    login_page = LoginPage(page)
    login_page.navigate(base_url)
    login_page.login("viral.maurya@yopmail.com", "Artoon1#")
    page.wait_for_url("**/agent/**", timeout=10000)
    return page
