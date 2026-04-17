from playwright.sync_api import expect
from pages.dashboard_page import DashboardPage

class TestDashboard:
    def test_sidebar_routing(self, logged_in_page, base_url):
        dashboard_page = DashboardPage(logged_in_page)
        routes = [
            "/agent/profile",
            "/agent/chats/assigned",
            "/agent/queue",
            "/agent/tickets"
        ]
        for route in routes:
            dashboard_page.navigate(f"{base_url}{route}")
            dashboard_page.wait_for_load()
            assert route in logged_in_page.url

    def test_profile_update(self, logged_in_page, base_url):
        dashboard_page = DashboardPage(logged_in_page)
        dashboard_page.navigate(f"{base_url}/agent/profile")
        dashboard_page.wait_for_load()
        expect(logged_in_page.locator("body")).to_contain_text("Viral")

    def test_logout_functionality(self, logged_in_page):
        dashboard_page = DashboardPage(logged_in_page)
        dashboard_page.logout()
        logged_in_page.wait_for_timeout(2000)
        # Verify user is redirected back to login page
        assert "/agent" not in logged_in_page.url
