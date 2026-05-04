"""
Root conftest.py
Registers all BDD step modules and provides Playwright fixtures.
"""
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from utils.config import Config

# Register BDD step definitions globally
from steps.ui import login_steps, cart_steps   # noqa: F401
from steps.api import posts_steps               # noqa: F401


# ── Playwright session fixtures ───────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=Config.HEADLESS, slow_mo=Config.SLOW_MO)
        yield b
        b.close()


@pytest.fixture
def context(browser: Browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 720})
    ctx.set_default_timeout(Config.TIMEOUT)
    yield ctx
    ctx.close()


@pytest.fixture
def page(context: BrowserContext) -> Page:
    pg = context.new_page()
    yield pg
    pg.close()
