"""
provider_health.py

Provider Health Checker.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime

from backend.logger import Logger


class ProviderHealth:

    def __init__(self, provider):

        self.provider = provider
        self.logger = Logger()

        self.status = "UNKNOWN"

        self.total_checks = 0
        self.successful_checks = 0
        self.failed_checks = 0
        self.consecutive_failures = 0

        self.last_success = None
        self.last_failure = None
        self.last_error = None

    # ==================================================
    # Health Check
    # ==================================================

    def check(self):

        self.total_checks += 1

        try:

            if self.provider is None:
                raise ValueError(
                    "Provider instance is None."
                )

            if not callable(
                getattr(self.provider, "load", None)
            ):
                raise ValueError(
                    "Provider does not implement load()."
                )

            if not callable(
                getattr(self.provider, "probe", None)
            ):
                raise ValueError(
                    "Provider does not implement probe()."
                )
            # Perform provider readiness probe.
            probe_result = self.provider.probe()

            if probe_result is not True:
                probe_error = getattr(
                    self.provider,
                    "probe_error",
                    None,
                )

                if probe_error:
                    raise RuntimeError(
                        f"Provider '{self.provider.name}' "
                        f"failed readiness probe: "
                        f"{probe_error}"
                    )

                raise RuntimeError(
                    f"Provider '{self.provider.name}' "
                    "failed readiness probe."
                )

            self.status = "HEALTHY"

            self.successful_checks += 1
            self.consecutive_failures = 0

            self.last_success = datetime.now()
            self.last_error = None

            self.logger.info(
                "Provider",
                f"{self.provider.name} is healthy."
            )

            return True

        except Exception as error:

            self.status = "UNHEALTHY"

            self.failed_checks += 1
            self.consecutive_failures += 1

            self.last_failure = datetime.now()
            self.last_error = str(error)

            self.logger.error_log(
                f"Provider Health Failed: {error}"
            )

            return False

    # ==================================================
    # Status
    # ==================================================

    def is_healthy(self):

        return self.status == "HEALTHY"

    @property
    def healthy(self):

        return self.is_healthy()

    # ==================================================
    # Information
    # ==================================================

    def info(self):

        return {
            "provider": self.provider.name,
            "status": self.status,
            "healthy": self.is_healthy(),
            "total_checks": self.total_checks,
            "successful_checks": self.successful_checks,
            "failed_checks": self.failed_checks,
            "consecutive_failures":
                self.consecutive_failures,
            "last_success": self.last_success,
            "last_failure": self.last_failure,
            "last_error": self.last_error,
        }

    # ==================================================
    # Report
    # ==================================================

    def report(self):
        """
        Backward-compatible alias for info().
        """

        return self.info()
