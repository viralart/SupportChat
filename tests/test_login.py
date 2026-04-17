from pages.login_page import LoginPage

class TestLogin:
    def test_positive_login(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate(base_url)
        login_page.login("viral.maurya@yopmail.com", "Artoon1#")
        page.wait_for_url("**/agent/**", timeout=10000)
        assert "/agent" in page.url

    def test_invalid_password(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate(base_url)
        login_page.login("viral.maurya@yopmail.com", "WrongPassword123")
        page.wait_for_timeout(2000)
        assert "/agent" not in page.url

    def test_empty_credentials(self, page, base_url):
        login_page = LoginPage(page)
        login_page.navigate(base_url)
        login_page.submit_empty()
        page.wait_for_timeout(2000)
        assert "/agent" not in page.url
