import json
import os
from time import sleep
from webbrowser import Chrome

import pytest
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Page, sync_playwright, BrowserType, BrowserContext


@pytest.fixture(scope="class", params=["chromium"]) # "firefox", "webkit"
def browser_page(request) -> Page:
    with sync_playwright() as p:
        browser_type = getattr(p, request.param)
        browser = browser_type.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        yield page

        # teardown
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="class", params=["chromium"]) # "firefox", "webkit"
def browser_page_with_slow_connection(request) -> Page:
    def slow_route(route):
        sleep(.95)
        route.continue_()

    with sync_playwright() as p:
        browser_type: BrowserType = getattr(p, request.param)
        browser = browser_type.launch(headless=False)
        context = browser.new_context()
        context.route("**/*", slow_route)
        page = context.new_page()

        yield page

        # teardown
        page.close()
        context.close()
        browser.close()


@pytest.fixture(scope="class", params=["chromium"]) # "firefox", "webkit"
def browser_context_with_unstable_internet_connection(request) -> Page:
    with sync_playwright() as p:
        browser_type: BrowserType = getattr(p, request.param)
        browser = browser_type.launch(headless=False)
        context: BrowserContext = browser.new_context()

        yield context

        # teardown
        context.close()
        browser.close()


@pytest.fixture
def get_userdata() -> dict:
    load_dotenv(".env")
    userdata: dict = json.loads(os.getenv("USERDATA"))

    return userdata


@pytest.fixture
def logout(browser_page: Page):
    yield

    # ⬇ Teardown: logout
    try:
        if browser_page.is_visible("a#logout2"):
            browser_page.click("a#logout2")
            browser_page.wait_for_selector("a#login2", timeout=2000)
    except Exception as e:
        print(f" ⚠️Logout skipped due to: {e}")
