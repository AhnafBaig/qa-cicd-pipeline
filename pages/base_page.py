from playwright.sync_api import Page
from utils.config import Config
from utils.logger import get_logger

log = get_logger(__name__)


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.base_url = Config.UI_BASE_URL

    def navigate(self, path: str = "") -> None:
        url = f"{self.base_url}{path}"
        log.info(f"Navigating to {url}")
        self.page.goto(url)

    def get_title(self) -> str:
        return self.page.title()

    def get_current_url(self) -> str:
        return self.page.url

    def wait_for_url(self, fragment: str) -> None:
        self.page.wait_for_url(f"**{fragment}**")
