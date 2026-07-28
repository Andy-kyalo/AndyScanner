"""
provider_health.py

Provider Health Checker.

Verifies that the selected market data provider
is operational before a scan begins.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.logger import Logger


class ProviderHealth:
    """
    Performs provider health checks.
    """

    def __init__(self, provider):
        self.provider = provider
        self.logger = Logger()

    # ==================================================
    # Health Check
    # ==================================================

    def check(self) -> bool:
        """
        Verify provider readiness.
        """

        try:
            self.provider.load()

            self.logger.info(
                "Provider",
                f"{self.provider.name} is healthy."
            )

            return True

        except Exception as error:

            self.logger.error_log(
                f"Provider Health Failed: {error}"
            )

            return False

    # ==================================================
    # Provider Information
    # ==================================================

    def info(self):
        """
        Return provider information.
        """

        return {
            "provider": self.provider.name,
            "healthy": self.check(),
        }