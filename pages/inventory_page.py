from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    INVENTORY_CONTAINER = "#inventory_container"
    CART_BADGE          = ".shopping_cart_badge"
    CART_ICON           = ".shopping_cart_link"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def is_loaded(self) -> bool:
        return self.page.is_visible(self.INVENTORY_CONTAINER)

    def get_cart_count(self) -> str:
        if self.page.is_visible(self.CART_BADGE):
            return self.page.inner_text(self.CART_BADGE)
        return "0"

    def add_item_to_cart(self, item_name: str) -> None:
        slug = item_name.lower().replace(" ", "-")
        self.page.click(f"[data-test='add-to-cart-{slug}']")

    def remove_item_from_cart(self, item_name: str) -> None:
        slug = item_name.lower().replace(" ", "-")
        self.page.click(f"[data-test='remove-{slug}']")

    def go_to_cart(self) -> None:
        self.page.click(self.CART_ICON)
