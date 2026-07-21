"""
config_validator.py

Configuration validation.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from config.config import Config


def validate_config():
    """
    Validate application configuration.
    """

    required = {
        "APP_NAME": Config.APP_NAME,
        "APP_VERSION": Config.APP_VERSION,
        "DEFAULT_MARKET": Config.DEFAULT_MARKET,
        "DEFAULT_TIMEFRAME": Config.DEFAULT_TIMEFRAME,
        "DATABASE_PATH": Config.DATABASE_PATH,
    }

    missing = []

    for key, value in required.items():
        if value is None or str(value).strip() == "":
            missing.append(key)

    print("\n========== CONFIGURATION ==========")

    if missing:
        print("Status : INVALID")
        print("Missing Configuration:")

        for item in missing:
            print(f" - {item}")

        print("===================================")
        raise RuntimeError("Configuration validation failed.")

    print("Status : VALID")
    print("===================================")