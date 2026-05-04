from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage


@given("I am on the login page", target_fixture="login_page")
def go_to_login(page: Page) -> LoginPage:
    lp = LoginPage(page)
    lp.open()
    return lp


@when(parsers.parse('I login with username "{username}" and password "{password}"'))
def do_login(login_page: LoginPage, username: str, password: str) -> None:
    login_page.login(username, password)


@then("I should be on the inventory page")
def verify_inventory(page: Page) -> None:
    page.wait_for_url("**/inventory.html")
    assert "inventory.html" in page.url


@then("I should see a login error message")
def verify_error(login_page: LoginPage) -> None:
    assert login_page.is_error_visible(), "Expected error message to be visible"
