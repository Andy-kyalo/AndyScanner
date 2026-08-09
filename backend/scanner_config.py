"""
scanner_config.py

Scanner configuration.

Author: Andrew Kyalo
Project: Andy Scanner
"""


from backend.timeframe_manager import TimeframeManager


class ScannerConfig:
    """
    Holds runtime scanner configuration.
    """

    def __init__(
        self,
        market,
        timeframe,
        data_source="CSV",
        provider_priority=None,
    ):

        self.market = market
        self.timeframe = TimeframeManager.validate(timeframe)

        # Default provider
        self.data_source = data_source.upper()

        # Provider failover order
        if provider_priority is None:

            self.provider_priority = [
                "CSV",
                "API",
                "MT5",
            ]

        else:

            self.provider_priority = [
                provider.upper()
                for provider in provider_priority
            ]