from pytest_bdd import given, when, then, parsers
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.config import Config


@given("I am logged in as a standard user", target_fixture="inventory_page")
def login_standard(page: Page) -> InventoryPage:
    lp = LoginPage(page)
    lp.open()
    lp.login(Config.STANDARD_USER, Config.PASSWORD)
    page.wait_for_url("**/inventory.html")
    return InventoryPage(page)


@when(parsers.parse('I add "{item}" to the cart'))
def add_item(inventory_page: InventoryPage, item: str) -> None:
    inventory_page.add_item_to_cart(item)


@when(parsers.parse('I remove "{item}" from the cart'))
def remove_item(inventory_page: InventoryPage, item: str) -> None:
    inventory_page.remove_item_from_cart(item)


@when("I navigate to the cart page")
def go_to_cart(page: Page) -> None:
    page.click(".shopping_cart_link")


@then(parsers.parse('the cart count should be "{expected}"'))
def check_count(inventory_page: InventoryPage, expected: str) -> None:
    assert inventory_page.get_cart_count() == expected


@then(parsers.parse('I should see "{item}" in the cart'))
def check_item_in_cart(page: Page, item: str) -> None:
    cart = CartPage(page)
    assert item in cart.get_item_names(), f"'{item}' not found in cart"
