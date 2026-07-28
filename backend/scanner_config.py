"""
scanner_config.py

Scanner configuration object.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from dataclasses import dataclass, field

from config.config import Config


@dataclass
class ScannerConfig:
    """
    Runtime configuration for one scanner session.
    """

    # ==================================================
    # Market Configuration
    # ==================================================

    market: str = Config.DEFAULT_MARKET
    timeframe: str = Config.DEFAULT_TIMEFRAME

    # ==================================================
    # Provider Configuration
    # ==================================================

    provider: str = "CSV"

    data_source: str = Config.DATA_SOURCE
    data_directory: str = str(Config.DATA_DIRECTORY)

    # ==================================================
    # Database Configuration
    # ==================================================

    database_path: str = Config.DATABASE_PATH

    # ==================================================
    # Logging
    # ==================================================

    log_level: str = Config.LOG_LEVEL

    debug: bool = Config.DEBUG

    # ==================================================
    # Supported Providers
    # ==================================================

    supported_providers: tuple = field(
        default_factory=lambda: (
            "CSV",
            "MT5",
            "TRADINGVIEW",
            "BINANCE",
            "POLYGON",
            "MOCK",
        )
    )

    # ==================================================
    # Validation
    # ==================================================

    def validate(self):
        """
        Validate the scanner configuration.
        """

        if self.provider.upper() not in self.supported_providers:
            raise ValueError(
                f"Unsupported provider: {self.provider}"
            )

        return True