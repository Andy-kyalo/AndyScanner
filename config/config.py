"""
config.py

Loads environment variables for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env
load_dotenv(BASE_DIR / ".env")


class Config:
    """
    Central configuration class.
    """

    APP_NAME = os.getenv("APP_NAME", "Andy Scanner")
    APP_VERSION = os.getenv("APP_VERSION", "0.5.0")

    DEFAULT_MARKET = os.getenv("DEFAULT_MARKET", "US30")
    DEFAULT_TIMEFRAME = os.getenv("DEFAULT_TIMEFRAME", "M5")

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        str(BASE_DIR / "database" / "scanner.db"),
    )

    DATA_DIRECTORY = Path(
        os.getenv(
            "DATA_DIRECTORY",
            BASE_DIR / "data",
        )
       )

    MARKET_FILE = DATA_DIRECTORY / f"{DEFAULT_MARKET.lower()}.csv"

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    SCAN_INTERVAL = int(
        os.getenv("SCAN_INTERVAL", "60")
    )

    DEBUG = (
        os.getenv("DEBUG", "False").lower() == "true"
    )

    API_KEY = os.getenv("API_KEY", "")

    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        "",
    )

    TELEGRAM_CHAT_ID = os.getenv(
        "TELEGRAM_CHAT_ID",
        "",
    )