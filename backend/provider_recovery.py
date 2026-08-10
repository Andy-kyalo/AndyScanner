"""
provider_recovery.py

Provider Recovery and Cooldown Manager.

Temporarily prevents unhealthy providers from being
used repeatedly and allows them to recover automatically.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime, timedelta


class ProviderRecovery:

    def __init__(
        self,
        cooldown: float = 60.0,
    ):
        """
        Create the provider recovery manager.

        Args:
            cooldown: Number of seconds a failed provider
                      remains in cooldown.
        """

        self.cooldown = cooldown

        self._failures = {}
        self._recovery_attempts = {}

    # ==================================================
    # Record Failure
    # ==================================================

    def record_failure(self, provider_name):

        provider_name = provider_name.upper()

        now = datetime.now()

        self._failures[provider_name] = now

    # ==================================================
    # Record Recovery
    # ==================================================

    def record_recovery(self, provider_name):

        provider_name = provider_name.upper()

        self._failures.pop(
            provider_name,
            None,
        )

        self._recovery_attempts.pop(
            provider_name,
            None,
        )

    # ==================================================
    # Is In Cooldown
    # ==================================================

    def is_in_cooldown(self, provider_name):

        provider_name = provider_name.upper()

        failure_time = self._failures.get(
            provider_name
        )

        if failure_time is None:
            return False

        elapsed = (
            datetime.now() - failure_time
        ).total_seconds()

        if elapsed >= self.cooldown:

            self._failures.pop(
                provider_name,
                None,
            )

            return False

        return True

    # ==================================================
    # Can Attempt Recovery
    # ==================================================

    def can_attempt_recovery(self, provider_name):

        return not self.is_in_cooldown(
            provider_name
        )

    # ==================================================
    # Record Recovery Attempt
    # ==================================================

    def record_recovery_attempt(
        self,
        provider_name,
    ):

        provider_name = provider_name.upper()

        current = self._recovery_attempts.get(
            provider_name,
            0,
        )

        self._recovery_attempts[
            provider_name
        ] = current + 1

    # ==================================================
    # Recovery Attempts
    # ==================================================

    def recovery_attempts(
        self,
        provider_name,
    ):

        provider_name = provider_name.upper()

        return self._recovery_attempts.get(
            provider_name,
            0,
        )

    # ==================================================
    # Failure Time
    # ==================================================

    def failure_time(
        self,
        provider_name,
    ):

        provider_name = provider_name.upper()

        return self._failures.get(
            provider_name
        )

    # ==================================================
    # Cooldown Remaining
    # ==================================================

    def cooldown_remaining(
        self,
        provider_name,
    ):

        provider_name = provider_name.upper()

        failure_time = self._failures.get(
            provider_name
        )

        if failure_time is None:
            return 0.0

        elapsed = (
            datetime.now() - failure_time
        ).total_seconds()

        remaining = (
            self.cooldown - elapsed
        )

        if remaining <= 0:
            self._failures.pop(
                provider_name,
                None,
            )

            return 0.0

        return round(
            remaining,
            2,
        )

    # ==================================================
    # Status
    # ==================================================

    def status(self, provider_name):

        provider_name = provider_name.upper()

        if self.is_in_cooldown(
            provider_name
        ):

            return "COOLDOWN"

        return "AVAILABLE"

    # ==================================================
    # Information
    # ==================================================

    def info(self, provider_name):

        provider_name = provider_name.upper()

        return {
            "provider": provider_name,
            "status": self.status(
                provider_name
            ),
            "cooldown": self.cooldown,
            "cooldown_remaining":
                self.cooldown_remaining(
                    provider_name
                ),
            "failure_time":
                self.failure_time(
                    provider_name
                ),
            "recovery_attempts":
                self.recovery_attempts(
                    provider_name
                ),
        }

    # ==================================================
    # Report
    # ==================================================

    def report(self):

        providers = set(
            self._failures.keys()
        ) | set(
            self._recovery_attempts.keys()
        )

        return {
            provider: self.info(provider)
            for provider in sorted(providers)
        }
