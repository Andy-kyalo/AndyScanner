"""
config.py

Central configuration for Andy Scanner.

Loads environment variables from the .env file and exposes
them through the Config class.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ==========================================================
# Project Root
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv(BASE_DIR / ".env")


class Config:
    """
    Central configuration class for Andy Scanner.
    """

    # ======================================================
    # Application
    # ======================================================

    APP_NAME = os.getenv("APP_NAME", "Andy Scanner")
    APP_VERSION = os.getenv("APP_VERSION", "0.5.0")

    # ======================================================
    # Default Scanner Settings
    # ======================================================

    DEFAULT_MARKET = os.getenv("DEFAULT_MARKET", "US30")
    DEFAULT_TIMEFRAME = os.getenv("DEFAULT_TIMEFRAME", "M5")
    
    DATA_SOURCE = os.getenv(
        "DATA_SOURCE",
        "csv",
    )

    SCAN_INTERVAL = int(
        os.getenv("SCAN_INTERVAL", "60")
    )

    DEBUG = (
        os.getenv("DEBUG", "False").strip().lower()
        == "true"
    )

    LOG_LEVEL = os.getenv(
        "LOG_LEVEL",
        "INFO"
    ).upper()

    # ======================================================
    # Directories
    # ======================================================

    DATA_DIRECTORY = Path(
        os.getenv(
            "DATA_DIRECTORY",
            str(BASE_DIR / "data"),
        )
    )

    DATABASE_PATH = str(
        Path(
            os.getenv(
                "DATABASE_PATH",
                str(BASE_DIR / "database" / "scanner.db"),
            )
        )
    )

    MARKET_FILE = (
        DATA_DIRECTORY /
        f"{DEFAULT_MARKET.lower()}.csv"
    )

    # ======================================================
    # API Configuration
    # ======================================================

    API_KEY = os.getenv(
        "API_KEY",
        ""
    )

    TELEGRAM_BOT_TOKEN = os.getenv(
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    TELEGRAM_CHAT_ID = os.getenv(
        "TELEGRAM_CHAT_ID",
        ""
    )