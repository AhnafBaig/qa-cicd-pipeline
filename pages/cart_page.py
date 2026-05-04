from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS      = ".cart_item"
    CHECKOUT_BUTTON = "[data-test='checkout']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate("/cart.html")

    def get_item_names(self) -> list[str]:
        items = self.page.locator(".inventory_item_name")
        return [items.nth(i).inner_text() for i in range(items.count())]

    def get_item_count(self) -> int:
        return self.page.locator(self.CART_ITEMS).count()
