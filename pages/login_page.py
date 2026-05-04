from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT  = "#user-name"
    PASSWORD_INPUT  = "#password"
    LOGIN_BUTTON    = "#login-button"
    ERROR_MESSAGE   = "[data-test='error']"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate()

    def login(self, username: str, password: str) -> None:
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.page.inner_text(self.ERROR_MESSAGE)

    def is_error_visible(self) -> bool:
        return self.page.is_visible(self.ERROR_MESSAGE)
