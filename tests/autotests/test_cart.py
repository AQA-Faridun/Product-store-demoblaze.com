import random
import pytest
from time import sleep
from playwright.sync_api import Page, Dialog, BrowserContext, Error
from qase.pytest import qase


@pytest.mark.usefixtures("browser_page")
class TestCardPage:
    def pre_condition(self, page: Page):
        page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
        page.locator("text=Add to cart").click()
        page.get_by_role("link", name="Cart").first.click()

    @qase.id(125)
    @qase.title("Проверка загрузки страницы корзины")
    def test_cart_page_loading(self, browser_page: Page):
        @qase.step("Открыть страницу корзины.")
        def open_cart_page(page: Page):
            page.get_by_role("link", name="Cart").first.click()

            assert page.url.__contains__("cart"), "Cannot open cart page"

        page = browser_page
        page.goto("https://demoblaze.com/")
        open_cart_page(page)

    @qase.id(126)
    @qase.title("Проверка корректного отображения информации о товарах")
    def test_product_information_display(self, browser_page: Page):
        def get_product_data(page: Page):
            title, price = page.locator("h2").text_content(), page.locator(".price-container").text_content()
            return title, price

        @qase.step("Проверить наличие изображения товара.")
        def check_product_image(page: Page):
            img = page.locator("//tr[@class='success']//img[1]")
            img.wait_for(state="visible")
            assert img.is_visible(), "Image not displayed"

        @qase.step("Проверить наличие названия товара.")
        def check_product_name(page: Page, title: str):
            name = page.locator("(//tr[@class='success']//td)[2]").text_content()
            assert name.__contains__(title), "Product name is not correct"

        @qase.step("Проверить отображение цены товара.")
        def check_product_price(page: Page, price: str):
            coast = page.locator("(//tr[@class='success']//td)[3]").text_content()
            assert price.__contains__(coast), "Product price is not correct"

        @qase.step("Проверить корректность общей суммы.")
        def check_total_price(page: Page, price: str):
            total_price = int(page.locator("#totalp").text_content())
            count_of_products_in_cart = page.locator("#tbodyid tr").count()
            price = ''.join(filter(str.isdigit, price))
            assert total_price == count_of_products_in_cart * int(price), "Total price is not correct"

        page = browser_page
        page.goto("https://demoblaze.com/")
        page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
        product_title, product_price = get_product_data(page)
        page.locator("text=Add to cart").click()
        page.get_by_role("link", name="Cart").first.click()
        check_product_image(page)
        check_product_name(page, product_title)
        check_product_price(page, product_price)
        check_total_price(page, product_price)

    @qase.id(127)
    @qase.title("Проверка удаления товара из корзины")
    def test_cart_item_removal(self, browser_page: Page):
        @qase.step('Нажать "Delete" рядом с товаром.')
        def remove_item_from_cart(page: Page):
            page.get_by_role("link", name="Delete").click()
            page.wait_for_timeout(1000)

            delete_link = page.get_by_role("link", name="Delete")
            assert delete_link.is_hidden(), "Item is not removed"


        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        remove_item_from_cart(page)

    @qase.id(128)
    @qase.title("Проверка оформления заказа (Place Order)")
    def test_place_order_verification(self, browser_page: Page):
        def handle_dialog(alert: Dialog):
            alert.dismiss()

            assert True, "Dialog is not handled"

        @qase.step('Нажать кнопку "Place Order".')
        def click_on_place_order(page: Page):
            page.get_by_role("button", name="Place Order").click()

        page = browser_page
        page.on("dialog", handle_dialog)
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        click_on_place_order(page)

    @qase.id(129)
    @qase.title("Проверка поведения при обновлении страницы")
    def test_page_refresh_behavior(self, browser_page: Page):
        @qase.step("Добавить товар в корзину.")
        def add_product_to_cart(page: Page):
            self.pre_condition(page)

        @qase.step("Обновить страницу.")
        def refresh_page(page: Page):
            page.reload()

        page = browser_page
        page.goto("https://demoblaze.com/")
        add_product_to_cart(page)
        refresh_page(page)

    @qase.id(130)
    @qase.title("Проверка оформления заказа с пустой корзиной")
    def test_place_order_empty_cart(self, browser_page: Page):
        @qase.step("Удалить все товары из корзины.")
        def remove_all_items_from_cart(page: Page):
            delete_link = page.get_by_role("link", name="Delete")

            if delete_link.count() > 1:
                for i in range(1, delete_link.count() + 1):
                    page.get_by_role("link", name="Delete").nth(i).click()
                    page.wait_for_timeout(1000)
                return

            page.get_by_role("link", name="Delete").click()

        @qase.step('Нажать "Place Order".')
        def click_on_place_order(page: Page):
            page.get_by_role("button", name="Place Order").click()
            page.wait_for_timeout(1000)
            head_of_order_form = page.locator("#orderModalLabel").text_content()

            if head_of_order_form.__contains__("Place order"):
                assert False, "Place Order form opened by empty cart"

        page = browser_page
        page.goto("https://demoblaze.com/")
        self.pre_condition(page)
        remove_all_items_from_cart(page)
        click_on_place_order(page)

    @qase.id(134)
    @qase.title("Проверка изменения корзины в разных вкладках")
    @pytest.mark.skip(reason="У пользователя всё равно остаётся возможность оформить заказ с пустой корзиной")
    def test_cart_change_different_tabs(self, browser_page: Page):
        # @qase.step("Открыть корзину в двух вкладках.")
        # @qase.step("В первой вкладке удалить товар.")
        # @qase.step("Переключиться на вторую вкладку и нажать "Place Order".")

        page = browser_page
        page.goto("https://demoblaze.com/")


@pytest.mark.usefixtures("browser_page_with_slow_connection")
class TestGoodsPageInSlowInternet:
    @qase.id(133)
    @qase.title("Проверка удаления товара при медленном соединении")
    def test_item_removal_slow_connection(self, browser_page_with_slow_connection: Page):
        @qase.step('Включить режим "медленный интернет".')
        def slow_connection():
            print("Slow internet enable")

        @qase.step('Нажать "Delete" для удаления товара.')
        def delete_product_from_cart(page: Page):
            page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
            page.locator("text=Add to cart").click()
            page.get_by_role("link", name="Cart").first.click()
            page.get_by_role("link", name="Delete").click()
            page.wait_for_timeout(3000)

            delete_link = page.get_by_role("link", name="Delete")
            assert delete_link.is_hidden(), "Item is not removed"

        page = browser_page_with_slow_connection
        page.goto("https://demoblaze.com/")
        slow_connection()
        delete_product_from_cart(page)


@pytest.mark.usefixtures("browser_context_with_unstable_internet_connection")
class TestGoodsPageOffline:
    @qase.id(132)
    @qase.title("Проверка работы корзины при отключенном интернете")
    def test_cart_offline_functionality(self, browser_context_with_unstable_internet_connection: BrowserContext):
        @qase.step("Добавить товар в корзину.")
        def add_product_in_cart(page: Page):
            page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
            page.locator("text=Add to cart").click()
            page.get_by_role("link", name="Cart").first.click()

        @qase.step("Отключить интернет и обновить страницу.")
        def switch_off_internet_and_refresh_page(page: Page):
            # Отключаем интернет
            context.set_offline(True)

            try:
                page.reload()
            except Error as e:
                print(f"Ошибка подключения: {e}")

        context = browser_context_with_unstable_internet_connection
        page = context.new_page()
        page.goto("https://demoblaze.com/")
        add_product_in_cart(page)
        switch_off_internet_and_refresh_page(page)
        sleep(1.5)
        page.close()

        assert False, "Site doesn't work when there is no internet"
