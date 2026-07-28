"""
provider_diagnostics.py

Provider Diagnostics.

Collects diagnostic information about the active
market data provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime


class ProviderDiagnostics:
    """
    Collects provider diagnostics.
    """

    def __init__(self, provider):
        self.provider = provider

    # ==================================================
    # Diagnostics
    # ==================================================

    def report(self) -> dict:
        """
        Generate a provider diagnostic report.
        """

        return {
            "provider": self.provider.name,
            "market": self.provider.config.market,
            "timeframe": self.provider.config.timeframe,
            "source": self.provider.config.data_source,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }

    # ==================================================
    # Display
    # ==================================================

    def print_report(self):
        """
        Print diagnostics.
        """

        report = self.report()

        print("\n========== PROVIDER ==========")

        for key, value in report.items():
            print(f"{key.capitalize():12}: {value}")

        print("==============================")