import random
import pytest
from playwright.sync_api import Page, BrowserContext, Error
from qase.pytest import qase


@pytest.mark.usefixtures("browser_page")
class TestProductCardPage:

    @qase.id(117)
    @qase.title("Проверка загрузки страницы карточки товара")
    def test_product_card_loading(self, browser_page: Page):
        @qase.step("Открыть страницу карточки товара.")
        def open_product_card_page(page: Page):
            page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()

        @qase.step("Проверить, что название товара отображается.")
        def check_product_name(page: Page):
            assert page.locator("h2").is_visible(), "Product name not visible"

        @qase.step("Проверить отображение цены.")
        def check_product_price(page: Page):
            assert page.locator(".price-container").is_visible(), "Product price not visible"

        @qase.step("Проверить наличие и читаемость описания товара.")
        def check_product_description(page: Page):
            assert page.locator("div#more-information>p").is_visible(), "Product description not visible"

        @qase.step("Проверить отображение изображения товара.")
        def check_product_image(page: Page):
            assert page.locator("div#imgp>div>img").is_visible(), "Product image not visible"

        page = browser_page
        page.goto("https://demoblaze.com/")

        open_product_card_page(page)
        page.wait_for_timeout(2000)
        check_product_name(page)
        check_product_price(page)
        check_product_description(page)
        check_product_image(page)

    @qase.id(118)
    @qase.title('Проверка работы кнопки "Add to cart"')
    def test_add_to_cart_button_functionality(self, browser_page: Page):
        @qase.step('Нажать кнопку "Add to cart".')
        def click_add_to_cart_button(page: Page):
            page.locator("text=Add to cart").click()

        @qase.step("Перейти в корзину.")
        def navigate_to_cart(page: Page):
            page.get_by_role("link", name="Cart").first.click()

        @qase.step("Увеличить количество товара в корзине.")
        def increase_quantity_in_cart():
            assert False, "Button for increase quantity in cart is not implemented"

        page = browser_page
        page.goto("https://demoblaze.com/")
        page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()

        click_add_to_cart_button(page)
        navigate_to_cart(page)
        increase_quantity_in_cart()

    @qase.id(119)
    @qase.title("Проверка поведения при обновлении страницы")
    def test_page_refresh_behavior(self, browser_page: Page):
        @qase.step("Добавить товар в корзину.")
        def add_product_to_cart(page: Page):
            page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
            page.locator("text=Add to cart").click()

        @qase.step("Обновить страницу.")
        def refresh_page(page: Page):
            page.reload()

        page = browser_page
        page.goto("https://demoblaze.com/")
        add_product_to_cart(page)
        refresh_page(page)

    @qase.id(121)
    @qase.title('Проверка работы кнопки "Add to cart" при добавлении 100 товаров')
    def test_add_to_cart_100_products_verification(self, browser_page: Page):
        @qase.step("Добавить товар в корзину 100 раз.")
        def add_100_products_to_cart(page: Page) -> int:
            for _ in range(100):
                page.locator("text=Add to cart").click()

            page.get_by_role("link", name="Cart").first.click()
            table = page.locator("#tbodyid")
            table.wait_for(state="visible")
            page.wait_for_timeout(1900)
            products = page.locator("#tbodyid tr")
            return products.count()

        page = browser_page
        page.goto("https://demoblaze.com/")
        page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
        page.on("dialog", lambda alert: alert.accept())
        count_of_products = add_100_products_to_cart(page)

        assert not count_of_products == 100, "The user would can add 100 items to the cart"

    @qase.id(124)
    @qase.title("Проверка перехода на несуществующую страницу товара")
    def test_non_existent_product_page_navigation(self, browser_page: Page):
        @qase.step("Ввести в адресную строку /prod.html?idp_=999999.")
        def navigate_to_non_existent_product_page(page: Page):
            page.goto("https://demoblaze.com/prod.html?idp_=999999")

        page = browser_page
        page.goto("https://demoblaze.com/")
        navigate_to_non_existent_product_page(page)
        non_exist_product = page.locator("//div[contains(@class,'product-content product-wrap')]")

        assert not non_exist_product.is_visible(), "Not exist product appears and have opportunity add to cart"


@pytest.mark.usefixtures("browser_page_with_slow_connection")
class TestGoodsPageInSlowInternet:

    @qase.id(123)
    @qase.title("Проверка отображения при медленном интернете")
    def test_slow_internet_display(self, browser_page_with_slow_connection: Page):
        @qase.step('Включить режим "медленный интернет" в DevTools.')
        def enable_slow_connection_mode(page: Page):
            page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()
            page.locator("text=Add to cart").click()
            page.get_by_role("link", name="Cart").first.click()
            product = page.locator("#tbodyid tr")
            product.wait_for(state="visible")

            assert product.is_visible(), "Cart doesn't work in slow connection"

        page = browser_page_with_slow_connection
        page.goto("https://demoblaze.com/")
        enable_slow_connection_mode(page)


@pytest.mark.usefixtures("browser_context_with_unstable_internet_connection")
class TestGoodsPageOffline:

    @qase.id(120)
    @qase.title("Проверка поведения при отключенном интернете")
    def test_offline_behavior(self, browser_context_with_unstable_internet_connection: BrowserContext):
        @qase.step("Открыть страницу товара и отключить интернет.")
        def open_product_card_page(page: Page):
            page.locator(f"(//div[@class='card h-100']//img)[{random.randint(1, 9)}]").click()

        @qase.step("Обновить страницу.")
        def refresh_page(page: Page):
            try:
                page.reload()
            except Error as e:
                print(f"Ошибка подключения: {e}")

        context = browser_context_with_unstable_internet_connection
        page = context.new_page()
        page.goto("https://demoblaze.com/")
        open_product_card_page(page)

        # Отключаем интернет
        context.set_offline(True)

        refresh_page(page)

        try:
            online_status: bool = page.evaluate("() => navigator.onLine")
            assert online_status, "Нет интернет-соединения"
        except Error as e:
            assert False, f"Ошибка подключения: {e}"

        page.close()