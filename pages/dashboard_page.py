from playwright.sync_api import Page
from .base_page import BasePage

class DashboardPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.logout_locators = [
            page.locator("button:has-text('Logout')"),
            page.locator("button:has-text('Sign out')"),
            page.locator("a:has-text('Logout')")
        ]

    def logout(self):
        for locator in self.logout_locators:
            if locator.count() > 0:
                locator.first.click()
                break
