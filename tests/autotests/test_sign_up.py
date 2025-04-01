import json, os, random, string, pytest
from pathlib import Path
from dotenv import load_dotenv
from playwright.sync_api import Page, Dialog
from qase.pytest import qase

def get_userdata() -> dict:
    load_dotenv(".env")
    userdata: dict = json.loads(os.getenv("USERDATA"))

    return userdata

def save_(userdata: dict):
    env_path = ".env"

    load_dotenv(dotenv_path=env_path, override=True)
    existing_data = os.getenv("USERDATA")

    if existing_data:
        try:
            existing_data = json.loads(existing_data)
        except json.JSONDecodeError:
            existing_data = {}
    else:
        existing_data = {}

    existing_data.update(userdata)
    updated_userdata = json.dumps(existing_data)

    if env_path.exists():
        lines = env_path.read_text().splitlines()
    else:
        lines = []

    new_lines = []
    found = False
    for line in lines:
        if line.startswith("USERDATA="):
            new_lines.append(f"USERDATA={updated_userdata}")
            found = True
        else:
            new_lines.append(line)
    if not found:
        new_lines.append(f"USERDATA={updated_userdata}")

    env_path.write_text("\n".join(new_lines) + "\n")

def clear_userdata():
    env_path = ".env"

    if not env_path.exists():
        raise FileNotFoundError(f".env файл не найден по пути: {env_path}")

    lines = env_path.read_text().splitlines()
    new_lines = []

    for line in lines:
        if line.startswith("USERDATA="):
            new_lines.append(f"USERDATA={json.dumps({})}")
        else:
            new_lines.append(line)

    env_path.write_text("\n".join(new_lines))


alert_message: str = ""

def handle_dialog(alert: Dialog):
    global alert_message
    alert_message = alert.message
    alert.accept()

def pre_condition(page: Page):
    page.on("dialog", handle_dialog)
    page.goto("https://demoblaze.com/")

@qase.step('Кликнуть на "Sign up" в навбаре и открыть форму регистрации.')
def click_to_sign_up(page: Page):
    page.get_by_role("link", name="Sign up").click()


@qase.step('Нажать кнопку "Sign up".')
def click_sign_up_button(page: Page):
    page.get_by_role("button", name="Sign up").click()
    page.wait_for_event("dialog")


@qase.id(84)
@qase.title("Успешная регистрация с валидными данными")
def test_success_sign_up(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести корректное имя пользователя')
    def fill_username_field(page: Page) -> str:
        username = f"test_user_{random.randint(0, 200)}"
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести корректный пароль')
    def fill_password_field(page: Page) -> str:
        password = "password123"
        page.fill("#sign-password", value=password)

        return password

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)
    click_sign_up_button(page)

    if alert_message == "This user already exist.":
        page.reload()
        test_success_sign_up(page)

    assert "Sign up successful" in alert_message.capitalize(), "User cannot successfully sign up with valid data"
    userdata["valid_data"] = {"username": username, "password": password}
    save_(userdata)


class BlockedTestError(Exception):
    pass

@qase.id(85)
@qase.title("Проверка минимально допустимой длины имени пользователя и максимально допустимой длины пароля")
@pytest.mark.xfail(strict=True, reason="Невозможно зарегистрироваться в системе с одним символом")
def test_min_username_max_password_symbols():
    @qase.step("Ввести имя пользователя из минимально допустимого количества символов (например, a при минимуме 1 символ).")
    def step_1():
        raise BlockedTestError("Невозможно зарегистрироваться в системе с одним символом")

    @qase.step("Ввести валидный пароль.")
    def step_2():
        pass

    @qase.step('Нажать кнопку "Sign up".')
    def step_3():
        pass

    step_1()
    step_2()
    step_3()

    assert False, "User cannot sing up with one symbol in username field"


@qase.id(86)
@qase.title("Проверка максимально допустимой длины имени пользователя и минимально допустимой длины пароля")
def test_max_username_min_password_symbols(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести имя пользователя, содержащее максимально допустимое количество символов (например, 30 символов, если это ограничение).')
    def fill_username_field(page: Page) -> str:
        username = f"test_user_{''.join(random.choices(string.ascii_letters + string.digits, k=20))}"
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести валидный пароль (например, aB@123 при минимуме 6 символов).')
    def fill_password_field(page: Page) -> str:
        password = "aB@123"
        page.fill("#sign-password", value=password)

        return password

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)
    click_sign_up_button(page)

    if alert_message == "This user already exist.":
        page.reload()
        test_max_username_min_password_symbols(page)

    assert "Sign up successful" in alert_message.capitalize(), "User cannot sign up with max (corner) username and min (corner) password symbols"
    userdata["max_username_min_password_symbols"] = {"username": username, "password": password}
    save_(userdata)


@qase.id(87)
@qase.title("Проверка поддержки спецсимволов в имени пользователя")
def test_spec_symbol_in_username(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести имя пользователя, содержащее разрешенные спецсимволы')
    def fill_username_field(page: Page) -> str:
        username = f"test_user-{random.randint(0, 1000)}"
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести валидный пароль.')
    def fill_password_field(page: Page) -> str:
        password = "aB@123"
        page.fill("#sign-password", value=password)

        return password

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)
    click_sign_up_button(page)

    if alert_message == "This user already exist.":
        page.reload()
        test_spec_symbol_in_username(page)

    assert "Sign up successful" in alert_message.capitalize(), "User cannot sing up with special symbols in username"
    userdata["spec_symbol_in_username"] = {"username": username, "password": password}
    save_(userdata)


@qase.id(88)
@qase.title("Проверка ввода пароля с различными регистрами букв")
def test_password_with_different_case(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести корректное имя пользователя.')
    def fill_username_field(page: Page) -> str:
        username = f"test_user_{random.randint(0, 100)}"
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести пароль, содержащий строчные и заглавные буквы (например: PaSsWoRd123!).')
    def fill_password_field(page: Page) -> str:
        password = f"PaSsWoRd{random.randint(0, 1000)}!"
        page.fill("#sign-password", value=password)

        return password

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)
    click_sign_up_button(page)

    if alert_message == "This user already exist.":
        page.reload()
        test_password_with_different_case(page)

    assert "Sign up successful" in alert_message.capitalize(), "User cannot sign up with different case (upper / lower)"
    userdata["password_with_different_case"] = {"username": username, "password": password}
    save_(userdata)


@qase.id(89)
@qase.title("Попытка регистрации с пустыми полями.")
def test_sign_up_with_empty_fields(page: Page):
    @qase.step('Оставить поля "Username" и "Password" пустыми.')
    def stay_username_and_password_fields_empty(page: Page):
        page.fill("#sign-username", "")
        page.fill("#sign-password", "")

    @qase.step('Нажать кнопку "Sign up".')
    def click_sign_up_button_2(page: Page):
        page.get_by_role("button", name="Sign up").click()
        page.wait_for_timeout(500)

    pre_condition(page)
    click_to_sign_up(page)
    stay_username_and_password_fields_empty(page)
    click_sign_up_button_2(page)

    if alert_message == "This user already exist.":
        page.reload()
        test_sign_up_with_empty_fields(page)

    assert "Please fill out username and password" in alert_message.capitalize(), "User can sign up with empty fields"


@qase.id(90)
@qase.title("Попытка регистрации с уже занятым именем пользователя.")
def test_sign_up_with_exist_username(page: Page):
    @qase.step('Ввести имя пользователя, которое уже зарегистрировано в системе.')
    def fill_username_field(page: Page):
        page.fill("#sign-username", "Username-123")

    @qase.step('Ввести валидный пароль.')
    def fill_password_field(page: Page):
        page.fill("#sign-password", "secret")

    pre_condition(page)
    click_to_sign_up(page)
    fill_username_field(page)
    fill_password_field(page)
    click_sign_up_button(page)

    assert "This user already exist" in alert_message.capitalize(), "User wasn't registered"


@qase.id(91)
@qase.title("Попытка регистрации с именем пользователя, содержащим запрещенные символы.")
def test_sign_up_with_forbidden_characters_in_username(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести имя пользователя с запрещенными символами (например, user@name!).')
    def fill_username_field(page: Page) -> str:
        username = f"user{random.choice(string.punctuation)}name{random.choice(string.punctuation)}"
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести валидный пароль.')
    def fill_password_field(page: Page) -> str:
        password = "secret"
        page.fill("#sign-password", value=password)

        return password

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)
    click_sign_up_button(page)

    assert "Имя пользователя содержит недопустимые символы" in alert_message.capitalize(), "User can sing up with not allowed symbols"
    userdata["sign_up_with_forbidden_characters_in_username"] = {"username": username, "password": password}
    save_(userdata)


@qase.id(92)
@qase.title("Попытка регистрации с паролем, не соответствующим требованиям безопасности.")
def test_sign_up_with_unsafe_password(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести корректное имя пользователя.')
    def fill_username_field(page: Page) -> str:
        username = f"test_user_{random.randint(0, 100)}"
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести пароль, не содержащий заглавных букв или спецсимволов (например, password123).')
    def fill_password_field(page: Page) -> str:
        password = f"{''.join(random.choices(string.ascii_letters.lower() + string.digits, k=12))}"
        page.fill("#sign-password", value=password)

        return password

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)
    click_sign_up_button(page)

    assert "Пароль должен содержать минимум одну заглавную букву и один спецсимвол" in alert_message.capitalize(), \
        "User can sing up with weak password"
    userdata["weak password"] = {"username": username, "password": password}
    save_(userdata)


@qase.id(93)
@qase.title("Ввод пробелов в начале и конце имени пользователя (тестирование обрезки пробелов).")
def test_sign_up_with_spaces_on_both_side_the_username(page: Page):
    userdata = get_userdata()

    @qase.step('Ввести имя пользователя с пробелами в начале и в конце ( testuser ).')
    def fill_username_field(page: Page) -> str:
        username = f" testuser_{''.join(random.choices(string.ascii_letters.lower() + string.digits, k=3))} "
        page.fill("#sign-username", value=username)

        return username

    @qase.step('Ввести валидный пароль.')
    def fill_password_field(page: Page) -> str:
        password = "aB@123"
        page.fill("#sign-password", value=password)

        return password

    def is_target_request(request):
        return "signup" in request.url and request.method == "POST"

    pre_condition(page)
    click_to_sign_up(page)
    username = fill_username_field(page)
    password = fill_password_field(page)

    with page.expect_request(is_target_request) as request_info:
        click_sign_up_button(page)

        if alert_message == "This user already exist.":
            page.reload()
            test_sign_up_with_spaces_on_both_side_the_username(page)

    request = request_info.value
    body_dict = json.loads(request.post_data)

    assert body_dict["username"] == username.strip(), "User can sign up with spaces on both sides of the username"
    userdata["spaces_on_both_side_the_username"] = {"username": username, "password": password}
    save_(userdata)


@qase.id(94)
@qase.title("Попытка регистрации с паролем, содержащим только пробелы.")
def test_sign_up_with_only_spaces(page: Page):
    @qase.step('Ввести корректное имя пользователя.')
    def fill_username_field(page: Page):
        page.fill("#sign-username",f"test_user_{random.randint(100, 500)}")

    @qase.step('Ввести пароль, состоящий только из пробелов ( ).')
    def fill_password_field(page: Page):
        page.fill("#sign-password", "    ")

    pre_condition(page)
    click_to_sign_up(page)
    fill_username_field(page)
    fill_password_field(page)
    click_sign_up_button(page)

    assert "Пароль не может содержать только пробелы" in alert_message.capitalize(), "User can sing up with multiple spaces in password"
