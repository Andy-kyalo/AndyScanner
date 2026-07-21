"""
validator.py

System configuration validator.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from pathlib import Path

from config.config import Config


class Validator:
    """
    Validates the application's configuration.
    """

    @staticmethod
    def validate():
        """
        Validate all required resources.

        Returns
        -------
        tuple(bool, list)
        """

        errors = []

        if not Config.APP_NAME:
            errors.append("APP_NAME is missing.")

        if not Config.DEFAULT_MARKET:
            errors.append("DEFAULT_MARKET is missing.")

        if not Config.DEFAULT_TIMEFRAME:
            errors.append("DEFAULT_TIMEFRAME is missing.")

        if Config.SCAN_INTERVAL <= 0:
            errors.append("SCAN_INTERVAL must be greater than zero.")

        db_path = Path(Config.DATABASE_PATH)

        if not db_path.parent.exists():
            errors.append(
                f"Database directory not found: {db_path.parent}"
            )

        data_dir = Path(Config.DATA_DIRECTORY)

        if not data_dir.exists():
            errors.append(
                f"Data directory not found: {data_dir}"
            )

        log_dir = Path("logs")

        if not log_dir.exists():
            errors.append(
                "Logs directory not found."
            )

        return len(errors) == 0, errors