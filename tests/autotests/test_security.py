import pytest
from playwright.sync_api import Page, Dialog
from qase.pytest import qase


@pytest.mark.usefixtures("browser_page")
class TestSecurity:
    alert_message: str = ""

    def handle_dialog(self, alert: Dialog):
        self.alert_message = alert.message
        alert.accept()

    @qase.id(153)
    @qase.title("XSS-атака на поле username при регистрации")
    def test_username_registration_xss_attack(self, browser_page: Page):
        @qase.step('Ввести в поле "Username"')
        def fill_username_field(page: Page):
            page.fill("#sign-username", "< script > alert('XSS') < / script >")

        @qase.step("Ввести валидный пароль")
        def fill_password_field(page: Page):
            page.fill("#sign-password", "password123")

        @qase.step('Нажать "Sign up"')
        def click_sign_up_button(page: Page):
            page.get_by_role("button", name="Sign up").click()
            page.wait_for_event("dialog")

        page = browser_page

        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        page.get_by_role("link", name="Sign up").click()
        fill_username_field(page)
        fill_password_field(page)
        click_sign_up_button(page)

        assert self.alert_message.__contains__("Недопустимый ввод") or self.alert_message.__contains__("Invalid input"), \
            "Error message not displayed"
        self.alert_message = ""

    def pre_log_in_action(self, page: Page) -> Page:
        page.goto("https://demoblaze.com/")
        page.get_by_role("link", name="Log in").click()

        return page

    @qase.id(154)
    @qase.title("SQL-инъекция в поле username при авторизации")
    def test_username_authorization_sql_injection(self, browser_page: Page):
        @qase.step('Ввести в поле "Username"')
        def fill_username_field(page: Page):
            page.fill("#loginusername", "admin' OR '1'='1")

        @qase.step('Ввести в поле "Password".')
        def fill_password_field(page: Page):
            page.fill("#loginpassword", "password123")

        @qase.step('Нажать "Log in"')
        def click_log_in_button(page: Page):
            page.get_by_role("button", name="Log in").click()

        page = browser_page
        page = self.pre_log_in_action(page)
        fill_username_field(page)
        fill_password_field(page)
        page.on("dialog", self.handle_dialog)
        click_log_in_button(page)

        assert self.alert_message.__contains__("Ошибка") or self.alert_message.__contains__("Error"), \
            "Error message not displayed"
        self.alert_message = ""

    @qase.id(155)
    @qase.title("XSS-атака на поле username при авторизации")
    def test_username_authorization_xss_attack(self, browser_page: Page):
        @qase.step('Ввести в поле "Username"')
        def fill_username_field(page: Page):
            page.fill("#loginusername", "< script > alert('XSS') < / script >")

        @qase.step("Ввести любой пароль")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", "password123")

        @qase.step('Нажать "Log in"')
        def click_log_in_button(page: Page):
            page.get_by_role("button", name="Log in").click()

        page = browser_page
        page = self.pre_log_in_action(page)
        fill_username_field(page)
        fill_password_field(page)
        page.on("dialog", self.handle_dialog)
        click_log_in_button(page)

        assert self.alert_message.__contains__("Недопустимый ввод") or self.alert_message.__contains__("Invalid input"),\
            "Error message not displayed"
        self.alert_message = ""
