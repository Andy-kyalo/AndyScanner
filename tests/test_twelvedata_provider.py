import unittest
from unittest.mock import Mock, patch

import requests

from backend.providers.twelvedata_provider import TwelveDataProvider
from backend.provider_exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderDataError,
    ProviderPlanRestrictedError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from backend.scanner_config import ScannerConfig


class TestTwelveDataProvider(unittest.TestCase):
    SECRET = "SYNTHETIC_TEST_KEY_12345"

    def setUp(self):
        self.config = ScannerConfig(
            market="EURUSD",
            timeframe="M5",
            data_source="TWELVEDATA",
            api_key=self.SECRET,
        )
        self.provider = TwelveDataProvider(self.config)

    @staticmethod
    def response(status_code=200, data=None):
        mock_response = Mock()
        mock_response.status_code = status_code
        mock_response.json.return_value = (
            {} if data is None else data
        )
        return mock_response

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_request_uses_expected_parameters_and_timeout(
        self, mock_get
    ):
        mock_get.return_value = self.response(
            data={"values": []}
        )

        result = self.provider.request(limit=20)

        self.assertEqual(result, {"values": []})
        mock_get.assert_called_once()

        args, kwargs = mock_get.call_args
        self.assertEqual(
            args[0],
            TwelveDataProvider.BASE_URL,
        )
        self.assertEqual(kwargs["params"]["symbol"], "EUR/USD")
        self.assertEqual(kwargs["params"]["interval"], "5min")
        self.assertEqual(kwargs["params"]["outputsize"], 20)
        self.assertEqual(kwargs["params"]["apikey"], self.SECRET)
        self.assertEqual(kwargs["params"]["timezone"], "UTC")
        self.assertEqual(kwargs["timeout"], 15)

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_missing_api_key_fails_before_http_request(
        self, mock_get
    ):
        config = ScannerConfig(
            market="EURUSD",
            timeframe="M5",
            data_source="TWELVEDATA",
            api_key=None,
        )
        provider = TwelveDataProvider(config)

        with self.assertRaises(ProviderAuthenticationError):
            provider.request()

        mock_get.assert_not_called()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_non_positive_limit_fails_before_http_request(
        self, mock_get
    ):
        for limit in (0, -1):
            with self.subTest(limit=limit):
                with self.assertRaises(ValueError):
                    self.provider.request(limit=limit)

        mock_get.assert_not_called()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_http_authentication_error_is_classified(
        self, mock_get
    ):
        mock_get.return_value = self.response(
            status_code=401,
            data={"message": "Invalid API key"},
        )

        with self.assertRaises(ProviderAuthenticationError):
            self.provider.request()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_api_rate_limit_error_is_classified(
        self, mock_get
    ):
        mock_get.return_value = self.response(
            data={
                "status": "error",
                "code": 429,
                "message": "API credits exhausted",
            }
        )

        with self.assertRaises(ProviderRateLimitError):
            self.provider.request()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_plan_restriction_is_classified(
        self, mock_get
    ):
        mock_get.return_value = self.response(
            data={
                "status": "error",
                "code": 403,
                "message": "This endpoint requires an upgrade",
            }
        )

        with self.assertRaises(ProviderPlanRestrictedError):
            self.provider.request()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_http_403_authentication_error_is_classified(
        self, mock_get
    ):
        mock_get.return_value = self.response(
            status_code=403,
            data={"message": "Invalid API key"},
        )

        with self.assertRaises(ProviderAuthenticationError):
            self.provider.request()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_plan_restriction_message_does_not_leak_raw_response(
        self, mock_get
    ):
        sensitive_detail = "SYNTHETIC_PROVIDER_DETAIL_123"

        mock_get.return_value = self.response(
            status_code=403,
            data={
                "message": (
                    "Endpoint requires an upgrade. "
                    + sensitive_detail
                )
            },
        )

        with self.assertRaises(ProviderPlanRestrictedError) as caught:
            self.provider.request()

        self.assertNotIn(
            sensitive_detail,
            str(caught.exception),
        )

    def test_malformed_candle_does_not_leak_raw_contents(self):
        sensitive_detail = "SYNTHETIC_CANDLE_DETAIL_456"

        response = {
            "values": [
                {
                    "datetime": "2026-10-10 10:05:00",
                    "open": sensitive_detail,
                    "high": "1.1020",
                    "low": "1.1000",
                    "close": "1.1015",
                }
            ]
        }

        with self.assertRaises(ProviderDataError) as caught:
            self.provider.map_candles(response)

        self.assertNotIn(
            sensitive_detail,
            str(caught.exception),
        )

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_server_error_is_classified(
        self, mock_get
    ):
        mock_get.return_value = self.response(
            status_code=503,
            data={"message": "Service unavailable"},
        )

        with self.assertRaises(ProviderUnavailableError):
            self.provider.request()

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_timeout_is_classified_without_echoing_request_url(
        self, mock_get
    ):
        mock_get.side_effect = requests.Timeout(
            f"timed out for https://example.invalid/?apikey={self.SECRET}"
        )

        with self.assertRaises(ProviderTimeoutError) as caught:
            self.provider.request()

        self.assertNotIn(self.SECRET, str(caught.exception))

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_connection_error_is_classified_without_echoing_secret(
        self, mock_get
    ):
        mock_get.side_effect = requests.ConnectionError(
            f"failed for https://example.invalid/?apikey={self.SECRET}"
        )

        with self.assertRaises(ProviderConnectionError) as caught:
            self.provider.request()

        self.assertNotIn(self.SECRET, str(caught.exception))

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_generic_request_error_is_classified_without_secret(
        self, mock_get
    ):
        mock_get.side_effect = requests.RequestException(
            f"request failed?apikey={self.SECRET}"
        )

        with self.assertRaises(ProviderConnectionError) as caught:
            self.provider.request()

        self.assertNotIn(self.SECRET, str(caught.exception))

    @patch("backend.providers.twelvedata_provider.requests.get")
    def test_invalid_json_is_classified(
        self, mock_get
    ):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError(
            "invalid JSON"
        )
        mock_get.return_value = mock_response

        with self.assertRaises(ProviderDataError):
            self.provider.request()

    def test_newest_first_values_are_mapped_chronologically(self):
        response = {
            "values": [
                {
                    "datetime": "2026-10-10 10:10:00",
                    "open": "1.1020",
                    "high": "1.1030",
                    "low": "1.1010",
                    "close": "1.1025",
                },
                {
                    "datetime": "2026-10-10 10:05:00",
                    "open": "1.1010",
                    "high": "1.1020",
                    "low": "1.1000",
                    "close": "1.1015",
                },
            ]
        }

        candles = self.provider.map_candles(response)

        self.assertEqual(
            [candle.time for candle in candles],
            [
                "2026-10-10 10:05:00",
                "2026-10-10 10:10:00",
            ],
        )
        self.assertEqual(candles[0].open, 1.1010)
        self.assertEqual(candles[1].close, 1.1025)

    def test_non_dictionary_response_is_rejected(self):
        with self.assertRaises(ProviderDataError):
            self.provider.map_candles([])

    def test_empty_values_are_rejected(self):
        with self.assertRaises(ProviderDataError):
            self.provider.map_candles({"values": []})

    def test_missing_candle_field_is_rejected(self):
        response = {
            "values": [
                {
                    "datetime": "2026-10-10 10:05:00",
                    "open": "1.1010",
                    "high": "1.1020",
                    "low": "1.1000",
                }
            ]
        }

        with self.assertRaises(ProviderDataError):
            self.provider.map_candles(response)

    def test_invalid_candle_price_is_rejected(self):
        response = {
            "values": [
                {
                    "datetime": "2026-10-10 10:05:00",
                    "open": "not-a-number",
                    "high": "1.1020",
                    "low": "1.1000",
                    "close": "1.1015",
                }
            ]
        }

        with self.assertRaises(ProviderDataError):
            self.provider.map_candles(response)


if __name__ == "__main__":
    unittest.main()
