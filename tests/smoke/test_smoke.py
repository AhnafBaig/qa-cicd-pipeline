"""
Smoke Tests
-----------
These run on EVERY push and pull request.
They are fast, focused checks that the system is alive:
  - API base URL responds
  - UI login succeeds

If any smoke test fails, the PR is blocked and the team is alerted
before the full regression suite wastes time on a broken build.
"""
import pytest
import requests
from playwright.sync_api import Page

from utils.config import Config
from pages.login_page import LoginPage


@pytest.mark.smoke
@pytest.mark.api
class TestAPISmoke:
    """Verify core API endpoints are reachable and responding correctly."""

    def test_api_is_up(self):
        """The API base URL must respond with HTTP 200."""
        response = requests.get(f"{Config.API_BASE_URL}/posts", timeout=10)
        assert response.status_code == 200, (
            f"API smoke failed: expected 200, got {response.status_code}"
        )

    def test_api_returns_json(self):
        """Response must be valid JSON."""
        response = requests.get(f"{Config.API_BASE_URL}/posts/1", timeout=10)
        data = response.json()
        assert isinstance(data, dict), "Expected a JSON object"
        assert "id" in data, "Expected 'id' field in response"

    def test_api_post_create(self):
        """POST to /posts must return 201 and echo the payload."""
        payload = {"title": "Smoke Test", "body": "CI check", "userId": 1}
        response = requests.post(
            f"{Config.API_BASE_URL}/posts", json=payload, timeout=10
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Smoke Test"


@pytest.mark.smoke
@pytest.mark.ui
class TestUISmoke:
    """Verify the UI is up and the critical login path works."""

    def test_login_page_loads(self, page: Page):
        """Login page must load without errors."""
        lp = LoginPage(page)
        lp.open()
        assert page.is_visible("#login-button"), "Login button not found on page"

    def test_successful_login(self, page: Page):
        """Standard user must be able to log in successfully."""
        lp = LoginPage(page)
        lp.open()
        lp.login(Config.STANDARD_USER, Config.PASSWORD)
        page.wait_for_url("**/inventory.html")
        assert "inventory.html" in page.url, (
            f"Login smoke failed — landed on: {page.url}"
        )
