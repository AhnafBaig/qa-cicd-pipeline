"""
Thin wrapper around requests.Session that:
  - Sets a base URL
  - Logs every request/response at DEBUG level
  - Raises on 5xx errors automatically
"""
import requests
from utils.config import Config
from utils.logger import get_logger

log = get_logger(__name__)


class APIClient:
    def __init__(self, base_url: str = Config.API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def get(self, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        log.debug(f"GET {url}")
        response = self.session.get(url, timeout=10, **kwargs)
        log.debug(f"→ {response.status_code}")
        return response

    def post(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        log.debug(f"POST {url}  body={payload}")
        response = self.session.post(url, json=payload, timeout=10, **kwargs)
        log.debug(f"→ {response.status_code}")
        return response

    def put(self, endpoint: str, payload: dict, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        log.debug(f"PUT {url}  body={payload}")
        response = self.session.put(url, json=payload, timeout=10, **kwargs)
        log.debug(f"→ {response.status_code}")
        return response

    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        log.debug(f"DELETE {url}")
        response = self.session.delete(url, timeout=10, **kwargs)
        log.debug(f"→ {response.status_code}")
        return response
