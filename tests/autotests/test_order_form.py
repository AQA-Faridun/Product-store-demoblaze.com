import random
from time import sleep

import pytest
from playwright.sync_api import Page, Dialog, BrowserContext, Request
from qase.pytest import qase


@pytest.mark.usefixtures("browser_page")
class TestOrderForm:
    def pre_condition(self, page: Page):
        page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
        page.locator("text=Add to cart").click()
        page.get_by_role("link", name="Cart").first.click()
        page.get_by_role("button", name="Place Order").click()

    alert_message: str = ""
    def handle_dialog(self, alert: Dialog):
        self.alert_message = alert.message
        alert.accept()

    @qase.step('Нажать на "Purchase".')
    def click_purchase_button(self, page: Page):
        page.get_by_role("button", name="Purchase").click()

    @qase.id(135)
    @qase.title("Ввод минимальных и максимальных значений месяца и года (01 и текущий год)")
    def test_min_max_month_year_input(self, browser_page: Page):
        @qase.step("Заполнить следующие поля: Name, Country, City, Credit Card, Month, Year.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'USA')
            page.fill('#city', 'New York')
            page.fill('#card', '4111111111111111')
            page.fill('#month', '03')
            page.fill('#year', '2025')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(136)
    @qase.title("Проверка карты Visa с максимальным месяцем и будущим годом")
    def test_visa_max_month_future_year(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Tajikistan')
            page.fill('#city', 'New York')
            page.fill('#card', '4111111111111111')
            page.fill('#month', '12')
            page.fill('#year', '2027')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(137)
    @qase.title("Проверка MasterCard с минимальным месяцем и будущим годом")
    def test_mastercard_min_month_future_year(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Uzbekistan')
            page.fill('#city', 'Samarkand')
            page.fill('#card', '5555555555554444')
            page.fill('#month', '01')
            page.fill('#year', '2026')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(138)
    @qase.title("Проверка American Express с валидным годом и максимальным месяцем")
    def test_american_express_valid_year_max_month(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Kazakhstan')
            page.fill('#city', 'Shimkent')
            page.fill('#card', '378282246310005')
            page.fill('#month', '12')
            page.fill('#year', '2025')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(139)
    @qase.title("Проверка минимально допустимой длины номера карты (15 цифр) с текущим годом")
    def test_min_card_number_length_current_year(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Chines')
            page.fill('#city', 'Beijing')
            page.fill('#card', '378282246310005')
            page.fill('#month', '06')
            page.fill('#year', '2025')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(140)
    @qase.title("Проверка MasterCard с будущим годом и случайным валидным месяцем")
    def test_mastercard_future_year_random_month(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Japan')
            page.fill('#city', 'Kyoto')
            page.fill('#card', '5555555555554444')
            page.fill('#month', '09')
            page.fill('#year', '2026')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(141)
    @qase.title("Проверка American Express с валидной комбинацией номера, месяца и года")
    def test_american_express_valid_combination(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'South Korea')
            page.fill('#city', 'Seoul')
            page.fill('#card', '371449635398431')
            page.fill('#month', '07')
            page.fill('#year', '2025')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(142)
    @qase.title("Проверка Visa с будущим годом и случайным валидным месяцем")
    def test_visa_future_year_random_month(self, browser_page: Page):
        @qase.step("Проверка Visa с будущим годом и случайным валидным месяцем")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Azerbaijan')
            page.fill('#city', 'Baku')
            page.fill('#card', '4111111111111111')
            page.fill('#month', '04')
            page.fill('#year', '2028')

        @qase.step('Нажать на "Purchase".')
        def click_purchase_button(page: Page):
            page.get_by_role("button", name="Purchase").click()

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(143)
    @qase.title("Проверка MasterCard с минимально допустимым месяцем и годом")
    def test_mastercard_min_month_year(self, browser_page: Page):
        @qase.step("Проверка MasterCard с минимально допустимым месяцем и годом")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'North Korea')
            page.fill('#city', 'Pyongyang')
            page.fill('#card', '5555555555554444')
            page.fill('#month', '01')
            page.fill('#year', '2025')

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(144)
    @qase.title("Проверка AmEx с максимальным допустимым месяцем и будущим годом")
    def test_american_express_max_month_future_year(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. Остальные поля заполнить валидными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'Taiwan')
            page.fill('#city', 'Taipei')
            page.fill('#card', '371449635398431')
            page.fill('#month', '12')
            page.fill('#year', '2030')

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        purchase_alert = page.locator("//h2[text()='Thank you for your purchase!']")
        purchase_alert.wait_for(state="visible")
        assert purchase_alert.text_content() == "Thank you for your purchase!", "User cannot order product"

    @qase.id(145)
    @qase.title("Попытка оформить заказ с пустыми полями")
    def test_place_order_empty_fields(self, browser_page: Page):
        @qase.step("Оставить все поля пустыми.")
        def all_field_empty():
            print("All fields are empty")

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        all_field_empty()
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill out Name and Creditcard.", "User can order product with empty fields"

    @qase.id(146)
    @qase.title('Проверка ввода нечислового значения в поле "Year"')
    def test_non_numeric_year_input(self, browser_page: Page):
        @qase.step("Заполнить поле Year, не валидными данными, а остальные поля валидными")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Vegas')
            page.fill('#card', '371449635398431')
            page.fill('#month', '12')
            page.fill('#year', 'abcd')

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill out Year.", "User can order product with not valid data in Year field"

    @qase.id(147)
    @qase.title("Ввод устаревшей даты карты (старый год + валидный месяц + валидный номер карты)")
    def test_expired_card_date_input(self, browser_page: Page):
        @qase.step("Заполнить поля Credit Card, Month, Year не валидными данными, а остальные поля валидными")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Vegas')
            page.fill('#card', '371449635398431')
            page.fill('#month', '12')
            page.fill('#year', '2022')

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill valid data in Year field.", \
            "The user can order product with old date in credit card"

    @qase.id(148)
    @qase.title("Ввод слишком длинного номера карты (17 цифр + валидный месяц + валидный год)")
    def test_too_long_card_number_input(self, browser_page: Page):
        @qase.step("Заполнить поле Credit Card слишком длинным значением")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Vegas')
            page.fill('#card', '41111111111111111')
            page.fill('#month', '12')
            page.fill('#year', '2026')

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill valid data in Credit Card.", \
            "The user can order product with not valid number of credit card"

    @qase.id(149)
    @qase.title('Проверка специальных символов в поле "Name"')
    def test_special_characters_name_field(self, browser_page: Page):
        @qase.step('Заполнить поле "Name" спецсимволами.')
        def fill_order_form(page: Page):
            page.fill('#name', '@#&!%^*()')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Vegas')
            page.fill('#card', '41111111111111111')
            page.fill('#month', '12')
            page.fill('#year', '2026')

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill valid data in Name field.", "The user can order product with not valid name"

    @qase.id(150)
    @qase.title('Ввод нечислового значения в поле "Credit Card"')
    def test_non_numeric_credit_card(self, browser_page: Page):
        @qase.step('В поле "Credit Card" ввести значение в перемешку с цифрами и буквами')
        def fill_order_form(page: Page):
            page.fill('#name', 'John Doe')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Vegas')
            page.fill('#card', 'abcd1234efgh5678')
            page.fill('#month', '12')
            page.fill('#year', '2026')

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill out Name and Creditcard.", \
            "The user can order product with not valid credit card"

    @qase.id(151)
    @qase.title("Проверка оформления заказа с неверным сочетанием месяца и года")
    def test_place_order_invalid_month_year(self, browser_page: Page):
        @qase.step("Заполнить поля: Credit Card, Month, Year. В поле Month ввести не корректные данные")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Wick')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Alamos')
            page.fill('#card', '41111111111111111')
            page.fill('#month', '15')
            page.fill('#year', '2025')

        page = browser_page
        page.on("dialog", self.handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        self.click_purchase_button(page)
        assert self.alert_message == "Please fill out Month with valid data.", \
            "The user can order product with not valid data in month field"


@pytest.mark.usefixtures("browser_context_with_unstable_internet_connection")
class TestOrderFormOffline:
    def handle_failed_request(self, request: Request):
        if request.url.__contains__("view"):
            print("❌ Запрос не удался:")
            print("URL:", request.url)
            print("Метод:", request.method)
            print("Причина:", request.failure)

            if request.failure == "ERR_INTERNET_DISCONNECTED":
                assert True, "The user cannot order product when he offline"

    def pre_condition(self, page: Page):
        page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
        page.locator("text=Add to cart").click()
        page.get_by_role("link", name="Cart").first.click()
        page.get_by_role("button", name="Place Order").click()

    @qase.step('Нажать на "Purchase".')
    def click_purchase_button(self, page: Page):
        page.get_by_role("button", name="Purchase").click()

    @qase.id(152)
    @qase.title("Проверка работы формы при отключенном интернете")
    def test_form_offline_functionality(self, browser_context_with_unstable_internet_connection: BrowserContext):
        @qase.step("Заполнить форму корректными данными.")
        def fill_order_form(page: Page):
            page.fill('#name', 'John Wick')
            page.fill('#country', 'USA')
            page.fill('#city', 'Los Angeles')
            page.fill('#card', '41111111111111111')
            page.fill('#month', '12')
            page.fill('#year', '2025')

        @qase.step("Отключить интернет.")
        def switch_off_internet(context: BrowserContext):
            # Отключаем интернет
            context.set_offline(True)

        context = browser_context_with_unstable_internet_connection
        page = context.new_page()
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        fill_order_form(page)
        switch_off_internet(context)
        page.on("requestfailed", self.handle_failed_request)
        self.click_purchase_button(page)

        sleep(1.5)
        page.close()
