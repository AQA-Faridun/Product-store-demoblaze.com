import random
import pytest
from playwright.sync_api import Page
from qase.pytest import qase


@pytest.mark.usefixtures("browser_page")
class TestMainPage:

    @qase.id(105)
    @qase.title("Проверка загрузки главной страницы")
    def test_main_page_loading(self, browser_page: Page):
        @qase.step("Открыть главную страницу в браузере.")
        def open_main_page(page: Page):
            page.goto("https://demoblaze.com/")

        @qase.step("Все элементы отображаются (меню, слайдер, категории, список товаров, кнопки навигации).")
        def all_element_visible(page: Page):
            navbar = page.locator("#navbarExample")
            navbar.wait_for(state="visible")
            carousel = page.locator(".carousel-inner")
            carousel.wait_for(state="visible")
            goods_category = page.locator(".list-group")
            goods_category.wait_for(state="visible")
            list_of_goods = page.locator("#tbodyid")
            list_of_goods.wait_for(state="visible")
            pagination_buttons = page.locator(".pagination")
            pagination_buttons.wait_for(state="visible")

            assert (navbar.is_visible() & carousel.is_visible() & goods_category.is_visible() & list_of_goods.is_visible()
                    & pagination_buttons.is_visible()), "Something went wrong"

        page = browser_page
        open_main_page(page)
        all_element_visible(page)


    @qase.id(106)
    @qase.title("Проверка работы главного меню")
    def test_main_menu_functionality(self, browser_page: Page):
        @qase.step('Нажать на ссылку "Home".')
        def click_home_in_navbar(page: Page):
            page.get_by_role("link", name="Home")
            assert page.title() == "STORE", "Cannot open home page"

        @qase.step('Нажать на "Contact".')
        def click_contact_in_navbar(page: Page):
            page.get_by_role("link", name="Contact")
            assert page.title() == "Contacts", "Cannot open contact page"

        @qase.step('Нажать на "About us".')
        def click_about_us_in_navbar(page: Page):
            page.get_by_role("link", name="About us")
            assert page.title() == "About us", "Cannot open about page"

        @qase.step('Нажать на "Cart".')
        def click_cart_in_navbar(page: Page):
            page.get_by_role("link", name="Cart")
            assert page.title() == "Cart", "Cannot open cart page"

        @qase.step('Нажать "Log in".')
        def click_log_in_in_navbar(page: Page):
            page.get_by_role("link", name="Log in")
            assert page.title() == "Log in", "Cannot open log in form"

        @qase.step('Нажать "Sign up".')
        def click_sign_up_in_navbar(page: Page):
            page.get_by_role("link", name="Sign up")
            assert page.title() == "Sign up", "Cannot open sign up form"

        page = browser_page

        page.goto("https://demoblaze.com/")
        click_home_in_navbar(page)
        click_contact_in_navbar(page)
        click_about_us_in_navbar(page)
        click_cart_in_navbar(page)
        click_log_in_in_navbar(page)
        click_sign_up_in_navbar(page)


    @qase.id(107)
    @qase.title("Проверка работы слайдера на главной странице")
    def test_main_page_slider_functionality(self, browser_page: Page):
        @qase.step("Проверить отображение первого слайда.")
        def is_first_slide_show(page: Page):
            first_slide = page.locator(".carousel-item").first
            assert first_slide.is_visible(), "1st slide not showed"

        @qase.step('Нажать кнопку "вперед" (>).')
        def is_next_slide_show(page: Page):
            page.locator(".carousel-control-next").click()
            next_slide = page.locator(".carousel-item").nth(1)
            assert next_slide.is_visible(), "next slide not showed"

        @qase.step('Нажать кнопку "назад" (<).')
        def is_previously_slide_show(page: Page):
            page.locator(".carousel-control-prev").click()
            previously_slide = page.locator(".carousel-item").first
            assert previously_slide.is_visible(), "previously slide not showed"

        page = browser_page

        page.goto("https://demoblaze.com/")
        is_first_slide_show(page)
        is_next_slide_show(page)
        is_previously_slide_show(page)


    @qase.id(108)
    @qase.title("Проверка списка категорий товаров")
    def test_product_categories_list(self, browser_page: Page):
        @qase.step('Нажать "Phones".')
        def click_phones_category(page: Page):
            page.get_by_role("link", name="Phones").click()
            page.wait_for_timeout(2500)
            items = page.locator(".col-lg-4.col-md-6.mb-4")
            assert items.count() == 7, "After clicking on the Phones category, the list of products didn't change"

        @qase.step('Нажать "Laptops".')
        def click_laptops_category(page: Page):
            page.get_by_role("link", name="Laptops").click()
            page.wait_for_timeout(2000)
            items = page.locator(".col-lg-4.col-md-6.mb-4")
            assert items.count() == 6, "After clicking on the Laptops category, the list of products didn't change"

        @qase.step('Нажать "Monitors".')
        def click_monitors_category(page: Page):
            page.get_by_role("link", name="Monitors").click()
            page.wait_for_timeout(2000)
            items = page.locator(".col-lg-4.col-md-6.mb-4")
            assert items.count() == 2, "After clicking on the Monitors category, the list of products didn't change"

        page = browser_page

        page.goto("https://demoblaze.com/")
        click_phones_category(page)
        click_laptops_category(page)
        click_monitors_category(page)


    @qase.id(109)
    @qase.title("Проверка работы пагинации")
    def test_pagination_functionality(self, browser_page: Page):
        @qase.step("Проверить, загружается ли первая страница товаров.")
        def is_all_goods_downloaded(page: Page):
            page.wait_for_timeout(2000)
            items = page.locator(".col-lg-4.col-md-6.mb-4")
            assert items.count() == 9, "Not all goods downloaded"

        @qase.step('Нажать "Next".')
        def click_next_pagination_button(page: Page):
            next_pagination_btn = page.locator("#next2")
            next_pagination_btn.scroll_into_view_if_needed()
            next_pagination_btn.click()
            page.wait_for_timeout(1500)
            items = page.locator(".col-lg-4.col-md-6.mb-4")
            assert items.count() == 6, "After click on next button list of products didn't change"

        @qase.step('Нажать "Previous".')
        def click_previous_pagination_button(page: Page):
            next_pagination_btn = page.locator("#prev2")
            next_pagination_btn.scroll_into_view_if_needed()
            next_pagination_btn.click()
            page.wait_for_timeout(1500)
            items = page.locator(".col-lg-4.col-md-6.mb-4")
            assert items.count() == 9, "After click on previous button list of products didn't change"

        page = browser_page

        page.goto("https://demoblaze.com/")
        is_all_goods_downloaded(page)
        click_next_pagination_button(page)
        click_previous_pagination_button(page)


    @qase.id(110)
    @qase.title("Проверка кликабельности товаров")
    def test_product_clickability(self, browser_page: Page):
        @qase.step("Нажать на любую карточку товара.")
        def click_on_any_product_card(page: Page) -> (str, str, str):
            goods_card = page.locator(f"(//div[@class='card h-100'])[{random.randint(1, 9)}]")
            goods_title = goods_card.get_by_role("heading").first.inner_text()
            goods_price = goods_card.get_by_role("heading").last.inner_text()
            goods_description = goods_card.get_by_role("paragraph").inner_text()
            goods_card.get_by_role("link").first.click()

            return goods_title, goods_price, goods_description

        @qase.step("Проверить, что отображается цена, описание, изображение товара.")
        def check_title_price_description_picture_of_goods(page: Page, title_of_goods: str, price_of_goods: str, description_of_goods: str):
            product_title = page.get_by_role("heading", name=title_of_goods)
            product_price = page.get_by_role("heading", name=price_of_goods)
            product_description = page.get_by_text(description_of_goods)
            image = page.locator("div#imgp>div>img")

            assert (product_title.inner_text() == title_of_goods
                    and price_of_goods in product_price.inner_text()
                    and product_description.inner_text() in description_of_goods
                    and image.is_visible()
                    ), "Clicked another goods"

        page = browser_page

        page.goto("https://demoblaze.com/")
        title_of_goods, price_of_goods, description_of_goods = click_on_any_product_card(page)
        check_title_price_description_picture_of_goods(page, title_of_goods, price_of_goods, description_of_goods)


    @qase.id(115)
    @qase.title("Проверка работы пагинации при отсутствии предыдущих страниц")
    def test_pagination_no_previous_pages_verification(self, browser_page: Page):
        @qase.step("Будучи на 1ой странице попробовать перейти на предыдущую страницу")
        def click_previous_pagination_button(page: Page):
            page.wait_for_timeout(1700)
            next_pagination_btn = page.locator("#prev2")
            next_pagination_btn.scroll_into_view_if_needed()
            next_pagination_btn.click()

            assert next_pagination_btn.is_disabled(), "Previous button is available"

        page = browser_page

        page.goto("https://demoblaze.com/")
        click_previous_pagination_button(page)

    @qase.id(116)
    @qase.title("Проверка редиректа после входа")
    def test_login_redirection_verification(self, browser_page: Page, get_userdata):
        @qase.step('Кликнуть на ссылку "Log in" и авторизоваться.')
        def click_on_log_in_and_authorise(page: Page):
            page.get_by_role("link", name="Log in").click()
            page.fill("#loginusername", value=get_userdata["valid_data"]["username"])
            page.fill("#loginpassword", value=get_userdata["valid_data"]["password"])
            page.get_by_role("button", name="Log in").click()

        @qase.step("Открыть главную страницу и обновить её.")
        def open_main_page_and_reload(page: Page):
            page.get_by_role("link", name="Home").click()
            page.reload()

        page = browser_page

        page.goto("https://demoblaze.com/")
        click_on_log_in_and_authorise(page)
        open_main_page_and_reload(page)


@pytest.mark.usefixtures("browser_page_with_slow_connection")
class TestMainPageInSlowInternet:

    @qase.id(112)
    @qase.title("Проверка работы при медленном интернете")
    def test_slow_internet_connection(self, browser_page_with_slow_connection: Page):
        @qase.step('Включить режим "медленный интернет" в DevTools.')
        def enable_slow_connection_mode(page: Page):
            page.goto("https://demoblaze.com/")

        @qase.step("Проверить загрузку изображений.")
        def check_download_content_on_site(page: Page):
            imgs = page.locator("//div[@class='card h-100']//img")
            imgs.first.wait_for(state="visible")
            assert imgs.first.is_visible(), "1st goods image not downloaded"

            some_image = imgs.nth(random.randint(2, 8))
            some_image.wait_for(state="visible")
            assert some_image.is_visible(), "some goods image from medium not downloaded"

            imgs.last.wait_for(state="visible")
            assert imgs.last.is_visible(), "last goods image not downloaded"

        page = browser_page_with_slow_connection

        enable_slow_connection_mode(page)
        check_download_content_on_site(page)