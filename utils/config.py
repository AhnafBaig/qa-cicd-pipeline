import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    UI_BASE_URL: str  = os.getenv("UI_BASE_URL",  "https://www.saucedemo.com")
    API_BASE_URL: str = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    STANDARD_USER: str = os.getenv("STANDARD_USER", "standard_user")
    LOCKED_USER: str   = os.getenv("LOCKED_USER",   "locked_out_user")
    PASSWORD: str      = os.getenv("PASSWORD",      "secret_sauce")

    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() == "true"
    SLOW_MO: int   = int(os.getenv("SLOW_MO", "0"))
    TIMEOUT: int   = int(os.getenv("TIMEOUT", "10000"))
