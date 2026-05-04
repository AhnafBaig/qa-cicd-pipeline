import json
import pytest
from pytest_bdd import when, then, parsers
from utils.api_client import APIClient


@pytest.fixture
def api_ctx() -> dict:
    """Carries the HTTP response between steps within one scenario."""
    return {}


@pytest.fixture
def client() -> APIClient:
    return APIClient()


# ── WHEN ──────────────────────────────────────────────────────────────────────

@when(parsers.parse('I send GET "{endpoint}"'))
def get_request(api_ctx: dict, client: APIClient, endpoint: str) -> None:
    api_ctx["response"] = client.get(endpoint)


@when(parsers.parse('I POST to "{endpoint}" with body:\n{body}'))
def post_request(api_ctx: dict, client: APIClient, endpoint: str, body: str) -> None:
    api_ctx["response"] = client.post(endpoint, json.loads(body.strip()))


@when(parsers.parse('I PUT to "{endpoint}" with body:\n{body}'))
def put_request(api_ctx: dict, client: APIClient, endpoint: str, body: str) -> None:
    api_ctx["response"] = client.put(endpoint, json.loads(body.strip()))


@when(parsers.parse('I DELETE "{endpoint}"'))
def delete_request(api_ctx: dict, client: APIClient, endpoint: str) -> None:
    api_ctx["response"] = client.delete(endpoint)


# ── THEN ──────────────────────────────────────────────────────────────────────

@then(parsers.parse("status code is {code:d}"))
def check_status(api_ctx: dict, code: int) -> None:
    actual = api_ctx["response"].status_code
    assert actual == code, f"Expected {code}, got {actual}"


@then("response is a non-empty list")
def check_list(api_ctx: dict) -> None:
    data = api_ctx["response"].json()
    assert isinstance(data, list) and len(data) > 0


@then(parsers.parse('field "{field}" equals "{value}"'))
def check_field(api_ctx: dict, field: str, value: str) -> None:
    data = api_ctx["response"].json()
    assert str(data[field]) == value, f"Field {field}: expected '{value}', got '{data[field]}'"


@then(parsers.parse('content-type contains "{expected}"'))
def check_content_type(api_ctx: dict, expected: str) -> None:
    ct = api_ctx["response"].headers.get("Content-Type", "")
    assert expected in ct, f"Expected '{expected}' in Content-Type, got '{ct}'"
