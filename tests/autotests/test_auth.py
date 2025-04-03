import pytest
from playwright.sync_api import Page, Dialog
from qase.pytest import qase

alert_message: str = ""

def handle_dialog(alert: Dialog):
    global alert_message
    alert_message = alert.message
    alert.accept()

def pre_condition(page: Page):
    page.on("dialog", handle_dialog)
    page.goto("https://demoblaze.com/")

def click_to_log_in_link(page: Page):
    page.get_by_role("link", name="Log in").click()

@qase.step('Нажать кнопку "Log in".')
def click_log_in_button(page: Page):
    page.get_by_role("button", name="Log in").click()


@pytest.mark.usefixtures("browser_page")
class TestAuthPage:

    @qase.id(95)
    @qase.title("Успешный вход с корректными учетными данными.")
    def test_successful_login(self, browser_page: Page, get_userdata, logout):
        @qase.step('Открыть форму логина')
        def click_to_log_in_link_2(page: Page):
            page.get_by_role("link", name="Log in").click()

        @qase.step('Ввести существующее имя пользователя')
        def fill_username_field(page: Page):
            page.fill("#loginusername", value=get_userdata["valid_data"]["username"])

        @qase.step('Ввести корректный пароль')
        def fill_password_field(page: Page):
            page.fill("#loginpassword", value=get_userdata["valid_data"]["password"])

        page: Page = browser_page

        page.goto("https://demoblaze.com/")
        click_to_log_in_link_2(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        logged_user = page.locator("a:text('Welcome')")

        assert get_userdata["valid_data"]["username"] in logged_user.inner_text(), \
            "User cannot successfully log in with valid data"


    @qase.id(96)
    @qase.title("Проверка минимально допустимой длины имени пользователя и максимальной длины пароля.")
    @pytest.mark.xfail(strict=True,
                       reason="Невозможно войти c одним символом в username, т.к. система говорит что пользователь с таким именем уже есть, а пароль к такому пользователю не известен")
    def test_minimum_username_maximum_password_verification(self, browser_page: Page):
        @qase.step('Ввести имя пользователя с минимальной длиной (например, a при минимуме 1 символ).')
        def fill_username_field(page: Page):
            page.fill("#loginusername", "a")

        @qase.step('Ввести пароль с максимально допустимой длиной (например, 50 символов).')
        def fill_password_field(page: Page):
            page.fill("#loginpassword", "secret")

        page: Page = browser_page

        pre_condition(page)
        click_to_log_in_link(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        page.wait_for_event("dialog")
        logged_user = page.locator("a:text('Welcome')")

        assert "a" in logged_user.inner_text(), "User cannot successfully log in with valid data"


    @qase.id(97)
    @qase.title("Проверка максимально допустимой длины имени пользователя и минимальной длины пароля.")
    def test_maximum_username_minimum_password_verification(self, browser_page: Page, get_userdata, logout):
        @qase.step("Ввести имя пользователя, состоящее из максимально допустимого количества символов (например, 30 символов).")
        def fill_username_field(page: Page):
            page.fill("#loginusername", value=get_userdata["max_username_min_password_symbols"]["username"])

        @qase.step("Ввести пароль минимально допустимой длины (например, aB@123 при минимуме 6 символов).")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", value=get_userdata["max_username_min_password_symbols"]["password"])

        page: Page = browser_page

        page.goto("https://demoblaze.com/")
        click_to_log_in_link(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        logged_user = page.locator("a:text('Welcome')")

        assert get_userdata["max_username_min_password_symbols"]["username"] in logged_user.inner_text(), \
            "User cannot successfully log in with maximum username and minimum password symbols"


    @qase.id(98)
    @qase.title("Проверка ввода пароля с разными регистрами букв.")
    def test_password_case_verification(self, browser_page: Page, get_userdata, logout):
        @qase.step("Ввести существующее имя пользователя.")
        def fill_username_field(page: Page):
            page.fill("#loginusername", value=get_userdata["password_with_different_case"]["username"])

        @qase.step("Ввести пароль соответствующий пользователю, содержащий строчные и заглавные буквы.")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", value=get_userdata["password_with_different_case"]["password"])

        page: Page = browser_page

        page.goto("https://demoblaze.com/")
        click_to_log_in_link(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        logged_user = page.locator("a:text('Welcome')")

        assert get_userdata["password_with_different_case"]["username"] in logged_user.inner_text(), \
            "User cannot successfully log in with different password case"


    @qase.id(99)
    @qase.title("Вход с пробелами перед/после имени пользователя (тестирование обработки ввода).")
    def test_username_spaces_login_verification(self, browser_page: Page, get_userdata, logout):
        @qase.step("Ввести существующее имя пользователя с пробелами перед и после.")
        def fill_username_field(page: Page):
            page.fill("#loginusername", value=get_userdata["spec_symbol_in_username"]["username"])

        @qase.step("Ввести корректный пароль.")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", value=get_userdata["spec_symbol_in_username"]["password"])

        page: Page = browser_page

        page.goto("https://demoblaze.com/")
        click_to_log_in_link(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        logged_user = page.locator("a:text('Welcome')")

        assert get_userdata["spec_symbol_in_username"]["username"] in logged_user.inner_text(), \
            "User cannot successfully log in with username which have spaces on both side"


    @qase.id(100)
    @qase.title("Попытка входа с пустыми полями.")
    def test_empty_fields_login_attempt(self, browser_page: Page):
        @qase.step('Оставить поля "Username" и "Password" пустыми.')
        def empty_username_and_password(page: Page):
            page.fill("#loginusername", "")
            page.fill("#loginpassword", "")

        @qase.step('Нажать "Log in".')
        def click_log_in_button_2(page: Page):
            page.get_by_role("button", name="Log in").click()
            page.wait_for_timeout(500)

        page: Page = browser_page

        pre_condition(page)
        click_to_log_in_link(page)
        empty_username_and_password(page)
        click_log_in_button_2(page)

        assert "Please fill out username and password" in alert_message.capitalize(), "User can log in with empty fields"


    @qase.id(101)
    @qase.title("Попытка входа с неверным паролем.")
    def test_incorrect_password_login_attempt(self, browser_page: Page, get_userdata):
        @qase.step("Ввести корректное имя пользователя.")
        def fill_username_field(page: Page):
            page.fill("#loginusername", value=get_userdata["valid_data"]["username"])

        @qase.step("Ввести неверный пароль.")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", "secret")

        page: Page = browser_page

        pre_condition(page)
        click_to_log_in_link(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        page.wait_for_event("dialog")

        assert alert_message == "Wrong password.", "User can log in with wrong password"


    @qase.id(102)
    @qase.title("Попытка входа с несуществующим именем пользователя.")
    def test_non_existent_username_login_attempt(self, browser_page: Page, get_userdata):
        @qase.step("Ввести несуществующее имя пользователя.")
        def fill_username_field(page: Page):
            page.fill("#loginusername", "not_exist_user")

        @qase.step("Ввести любой пароль.")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", "secret")

        page: Page = browser_page

        pre_condition(page)
        click_to_log_in_link(page)
        fill_username_field(page)
        fill_password_field(page)
        click_log_in_button(page)
        page.wait_for_event("dialog")

        assert alert_message == "User does not exist.", "User can log in with wrong password"


    @qase.id(103)
    @qase.title("Попытка входа с учетной записью, которая была заблокирована.")
    @pytest.mark.skip(reason="Невозможно войти от имени заблокированного пользователя, т.к. не известно есть ли вообще такой пользователь")
    def test_locked_account_login_attempt(self):
        print("We dont have locked account for test this case")


    @qase.id(104)
    @qase.title("Попытка входа с многократными ошибочными попытками (тестирование ограничений).")
    def test_multiple_failed_login_attempts_rate_limit_test(self, browser_page: Page, get_userdata):
        print("Тест запустился")
        @qase.step("Ввести корректное имя пользователя.")
        def fill_username_field(page: Page):
            page.fill("#loginusername", value=get_userdata["valid_data"]["username"])

        @qase.step("Ввести неверный пароль.")
        def fill_password_field(page: Page):
            page.fill("#loginpassword", "secret")

        counter = 0
        page: Page = browser_page
        pre_condition(page)

        print("Тест дошёл до цикла")
        for i in range(5):
            if i > 1:
                page.reload()

            click_to_log_in_link(page)
            fill_username_field(page)
            fill_password_field(page)
            click_log_in_button(page)
            page.wait_for_event("dialog")
            page.get_by_role("button", name="Close").nth(1).click()

            if alert_message == "Wrong password.":
                counter+=1

        print("counter:", counter)
        assert not counter == 5, "System doesn't have limits for multiple try for log in"
