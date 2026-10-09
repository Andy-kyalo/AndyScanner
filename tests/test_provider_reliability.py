"""
test_provider_reliability.py

Regression tests for provider retry, timeout, recovery,
and health-check reliability behavior.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import time
import unittest
from unittest.mock import patch

from backend.provider_exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderTimeoutError,
)
from backend.provider_health import ProviderHealth
from backend.provider_recovery import ProviderRecovery
from backend.provider_retry import ProviderRetry
from backend.provider_timeout import ProviderTimeout


class TestProviderRetry(unittest.TestCase):

    @patch("backend.provider_retry.time.sleep")
    def test_retries_retryable_error_and_succeeds(
        self,
        mock_sleep,
    ):
        operation = unittest.mock.Mock(
            side_effect=[
                ProviderConnectionError("connection failed"),
                ProviderTimeoutError("timeout"),
                "success",
            ]
        )

        retry = ProviderRetry(
            retries=3,
            delay=1.0,
        )

        result = retry.execute(operation)

        self.assertEqual(result, "success")
        self.assertEqual(operation.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("backend.provider_retry.time.sleep")
    def test_exhausted_retryable_error_is_raised(
        self,
        mock_sleep,
    ):
        error = ProviderConnectionError(
            "connection failed"
        )

        operation = unittest.mock.Mock(
            side_effect=error
        )

        retry = ProviderRetry(
            retries=3,
            delay=1.0,
        )

        with self.assertRaises(ProviderConnectionError):
            retry.execute(operation)

        self.assertEqual(operation.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("backend.provider_retry.time.sleep")
    def test_non_retryable_error_is_not_retried(
        self,
        mock_sleep,
    ):
        operation = unittest.mock.Mock(
            side_effect=ProviderAuthenticationError(
                "authentication failed"
            )
        )

        retry = ProviderRetry(
            retries=3,
            delay=1.0,
        )

        with self.assertRaises(ProviderAuthenticationError):
            retry.execute(operation)

        operation.assert_called_once()
        mock_sleep.assert_not_called()


class TestProviderTimeout(unittest.TestCase):

    def test_operation_within_timeout_succeeds(self):
        timeout = ProviderTimeout(
            timeout=1.0,
        )

        result = timeout.execute(
            lambda: "success"
        )

        self.assertEqual(result, "success")

    def test_operation_exceeding_timeout_raises(self):
        timeout = ProviderTimeout(
            timeout=0.05,
        )

        def slow_operation():
            time.sleep(0.2)
            return "late"

        with self.assertRaises(ProviderTimeoutError):
            timeout.execute(slow_operation)


class TestProviderRecovery(unittest.TestCase):

    def test_failure_enters_cooldown(self):
        recovery = ProviderRecovery(
            cooldown=60.0,
        )

        recovery.record_failure("TWELVEDATA")

        self.assertTrue(
            recovery.is_in_cooldown("TWELVEDATA")
        )

        self.assertEqual(
            recovery.status("TWELVEDATA"),
            "COOLDOWN",
        )

    def test_recovery_clears_cooldown(self):
        recovery = ProviderRecovery(
            cooldown=60.0,
        )

        recovery.record_failure("TWELVEDATA")
        recovery.record_recovery("TWELVEDATA")

        self.assertFalse(
            recovery.is_in_cooldown("TWELVEDATA")
        )

        self.assertEqual(
            recovery.status("TWELVEDATA"),
            "AVAILABLE",
        )

    def test_recovery_attempts_are_counted(self):
        recovery = ProviderRecovery(
            cooldown=60.0,
        )

        recovery.record_recovery_attempt("TWELVEDATA")
        recovery.record_recovery_attempt("TWELVEDATA")

        self.assertEqual(
            recovery.recovery_attempts("TWELVEDATA"),
            2,
        )


class TestProviderHealth(unittest.TestCase):

    class FakeProvider:

        name = "FAKE"

        def __init__(self, probe_result=True):
            self.probe_result = probe_result
            self.probe_error = None

        def load(self, symbol=None):
            return []

        def probe(self):
            return self.probe_result

    def test_failed_probe_redacts_credentials_from_health_info_and_log(self):
        secret = "SYNTHETIC_HEALTH_SECRET_789"
        provider = self.FakeProvider()
        provider.probe = unittest.mock.Mock(
            side_effect=RuntimeError(
                f"request failed?apikey={secret}"
            )
        )
        health = ProviderHealth(provider)

        with patch.object(health.logger, "error_log") as mock_error_log:
            self.assertFalse(health.check())

        info = health.info()
        self.assertNotIn(secret, info["last_error"])
        self.assertNotIn(secret, mock_error_log.call_args.args[0])
        self.assertIn("[REDACTED]", info["last_error"])

    def test_successful_probe_marks_provider_healthy(self):
        provider = self.FakeProvider()
        health = ProviderHealth(provider)

        self.assertTrue(health.check())
        self.assertEqual(health.status, "HEALTHY")
        self.assertEqual(health.total_checks, 1)
        self.assertEqual(health.successful_checks, 1)
        self.assertEqual(health.failed_checks, 0)
        self.assertEqual(health.consecutive_failures, 0)

    def test_failed_probe_marks_provider_unhealthy(self):
        provider = self.FakeProvider(probe_result=False)
        health = ProviderHealth(provider)

        self.assertFalse(health.check())
        self.assertEqual(health.status, "UNHEALTHY")
        self.assertEqual(health.total_checks, 1)
        self.assertEqual(health.successful_checks, 0)
        self.assertEqual(health.failed_checks, 1)
        self.assertEqual(health.consecutive_failures, 1)

    @patch("backend.provider_retry.time.sleep")
    def test_retryable_probe_failure_is_retried(
        self,
        mock_sleep,
    ):
        provider = self.FakeProvider()

        provider.probe = unittest.mock.Mock(
            side_effect=[
                ProviderConnectionError(
                    "temporary connection failure"
                ),
                True,
            ]
        )

        health = ProviderHealth(provider)

        self.assertTrue(health.check())

        self.assertEqual(
            provider.probe.call_count,
            2,
        )

        mock_sleep.assert_called_once_with(1.0)
        self.assertEqual(health.status, "HEALTHY")

    def test_non_retryable_probe_error_is_not_retried(self):
        provider = self.FakeProvider()

        provider.probe = unittest.mock.Mock(
            side_effect=ProviderAuthenticationError(
                "authentication failed"
            )
        )

        health = ProviderHealth(provider)

        self.assertFalse(health.check())
        provider.probe.assert_called_once()
        self.assertEqual(health.status, "UNHEALTHY")
        self.assertEqual(health.failed_checks, 1)

    @patch("backend.provider_health.ProviderTimeout")
    def test_probe_timeout_marks_provider_unhealthy(
        self,
        mock_timeout_class,
    ):
        provider = self.FakeProvider()

        mock_timeout = mock_timeout_class.return_value
        mock_timeout.execute.side_effect = ProviderTimeoutError(
            "probe timeout"
        )

        health = ProviderHealth(provider)

        self.assertFalse(health.check())

        mock_timeout_class.assert_called_once_with(
            timeout=10.0
        )

        self.assertEqual(health.status, "UNHEALTHY")
        self.assertEqual(health.failed_checks, 1)

    @patch("backend.provider_health.ProviderRetry")
    @patch("backend.provider_health.ProviderTimeout")
    def test_probe_uses_timeout_and_retry(
        self,
        mock_timeout_class,
        mock_retry_class,
    ):
        provider = self.FakeProvider()

        mock_timeout = mock_timeout_class.return_value
        mock_retry = mock_retry_class.return_value

        mock_timeout.execute.return_value = True
        mock_retry.execute.side_effect = (
            lambda operation: operation()
        )

        health = ProviderHealth(provider)

        self.assertTrue(health.check())

        mock_timeout_class.assert_called_once_with(
            timeout=10.0
        )

        mock_retry_class.assert_called_once_with(
            retries=3,
            delay=1.0,
        )

        mock_retry.execute.assert_called_once()

        mock_timeout.execute.assert_called_once_with(
            provider.probe
        )

        self.assertEqual(health.status, "HEALTHY")


if __name__ == "__main__":
    unittest.main()