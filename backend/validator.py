"""
validator.py

System configuration validator for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from pathlib import Path

from config.config import Config


class Validator:
    """
    Validates the application's configuration and required resources.
    """

    @staticmethod
    def validate() -> tuple[bool, list[str]]:
        """
        Validate the application configuration.

        Returns:
            tuple:
                bool: True if validation passes.
                list[str]: List of validation errors.
        """

        errors = []

        # ==================================================
        # Configuration Validation
        # ==================================================

        if not Config.APP_NAME.strip():
            errors.append("APP_NAME is missing.")

        if not Config.APP_VERSION.strip():
            errors.append("APP_VERSION is missing.")

        if not Config.DEFAULT_MARKET.strip():
            errors.append("DEFAULT_MARKET is missing.")

        if not Config.DEFAULT_TIMEFRAME.strip():
            errors.append("DEFAULT_TIMEFRAME is missing.")

        if Config.SCAN_INTERVAL <= 0:
            errors.append("SCAN_INTERVAL must be greater than zero.")

        # ==================================================
        # Database Validation
        # ==================================================

        database_directory = Path(Config.DATABASE_PATH).parent

        if not database_directory.exists():
            errors.append(
                f"Database directory does not exist: {database_directory}"
            )

        # ==================================================
        # Data Directory Validation
        # ==================================================

        data_directory = Path(Config.DATA_DIRECTORY)

        if not data_directory.exists():
            errors.append(
                f"Data directory does not exist: {data_directory}"
            )
        elif not data_directory.is_dir():
            errors.append(
                f"Data path is not a directory: {data_directory}"
            )

        # ==================================================
        # Logs Directory Validation
        # ==================================================

        log_directory = Path("logs")

        if not log_directory.exists():
            errors.append("Logs directory does not exist.")
        elif not log_directory.is_dir():
            errors.append("Logs path is not a directory.")

        # ==================================================
        # Validation Result
        # ==================================================

        return len(errors) == 0, errors