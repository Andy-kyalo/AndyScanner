"""
config_validator.py

Configuration validation for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from config.config import Config


def validate_config():
    """
    Validate the application's configuration.

    Raises
    ------
    RuntimeError
        If one or more required configuration values
        are missing.
    """

    required = {
        "APP_NAME": Config.APP_NAME,
        "APP_VERSION": Config.APP_VERSION,
        "DEFAULT_MARKET": Config.DEFAULT_MARKET,
        "DEFAULT_TIMEFRAME": Config.DEFAULT_TIMEFRAME,
        "DATABASE_PATH": Config.DATABASE_PATH,
    }

    missing = [
        key
        for key, value in required.items()
        if not str(value).strip()
    ]

    print("\n========== CONFIGURATION ==========")

    if missing:
        print("Status : INVALID")
        print()

        print("Missing Configuration:")

        for item in missing:
            print(f" • {item}")

        print("===================================")

        raise RuntimeError(
            "Configuration validation failed."
        )

    print("Status : VALID")
    print("===================================")