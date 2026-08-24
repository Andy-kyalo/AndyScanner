"""
test_twelvedata_provider.py

Contract tests for TwelveDataProvider.

Andy Scanner
"""

from unittest.mock import Mock, patch

import requests

from backend.provider_exceptions import (
    ProviderAuthenticationError,
    ProviderConnectionError,
    ProviderDataError,
    ProviderMarketUnsupportedError,
    ProviderPlanRestrictedError,
    ProviderRateLimitError,
    ProviderTimeoutError,
    ProviderUnavailableError,
)
from backend.providers.twelvedata_provider import (
    TwelveDataProvider,
)
from backend.scanner_config import ScannerConfig


def make_config(
    market="EURUSD",
    timeframe="M5",
    api_key="TEST_KEY",
):
    config = ScannerConfig(
        market=market,
        timeframe=timeframe,
    )

    config.api_key = api_key

    return config


def make_provider(
    market="EURUSD",
    timeframe="M5",
    api_key="TEST_KEY",
):
    return TwelveDataProvider(
        make_config(
            market=market,
            timeframe=timeframe,
            api_key=api_key,
        )
    )


def fake_response(
    status_code=200,
    data=None,
):
    response = Mock()
    response.status_code = status_code
    response.json.return_value = data
    return response



# Timeframe


def test_timeframe_mapping():
    expected = {
        "M1": "1min",
        "M5": "5min",
        "M15": "15min",
        "M30": "30min",
        "H1": "1h",
        "H4": "4h",
        "D1": "1day",
    }

    for timeframe, interval in expected.items():
        provider = make_provider(
            timeframe=timeframe
        )

        assert provider._interval() == interval


def test_invalid_timeframe_rejected_by_scanner_config():
    try:
        make_config(
            timeframe="INVALID"
        )
    except ValueError as error:
        assert "Unsupported timeframe" in str(error)
    else:
        raise AssertionError(
            "ScannerConfig accepted an invalid timeframe."
        )



# Symbol Resolution


def test_eurusd_symbol_resolution():
    provider = make_provider(
        market="EURUSD"
    )

    assert provider._resolve_symbol() == "EUR/USD"


def test_explicit_provider_symbol():
    provider = make_provider()

    assert (
        provider._resolve_symbol(
            "CUSTOM/SYMBOL"
        )
        == "CUSTOM/SYMBOL"
    )


def test_unsupported_market():
    provider = make_provider(
        market="US30"
    )

    try:
        provider._resolve_symbol()
    except ProviderMarketUnsupportedError as error:
        assert "US30" in str(error)
    else:
        raise AssertionError(
            "Unsupported market was accepted."
        )



# Probe


def test_probe_success():
    provider = make_provider()

    assert provider.probe() is True
    assert provider.probe_error is None


def test_probe_missing_api_key():
    provider = make_provider(
        api_key=None
    )

    assert provider.probe() is False
    assert "API key" in provider.probe_error


def test_probe_unsupported_market():
    provider = make_provider(
        market="US30"
    )

    assert provider.probe() is False
    assert "US30" in provider.probe_error



# Request construction



@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_request_builds_expected_parameters(mock_get):

    mock_get.return_value = fake_response(
        data={
            "status": "ok",
            "values": [],
        }
    )

    provider = make_provider(
        market="EURUSD",
        timeframe="M5",
    )

    provider.request(
        limit=100
    )

    mock_get.assert_called_once()

    _, kwargs = mock_get.call_args

    params = kwargs["params"]

    assert params["symbol"] == "EUR/USD"
    assert params["interval"] == "5min"
    assert params["outputsize"] == 100
    assert params["apikey"] == "TEST_KEY"
    assert params["format"] == "JSON"
    assert params["timezone"] == "UTC"

    assert kwargs["timeout"] == provider.timeout


def test_request_invalid_limit():
    provider = make_provider()

    try:
        provider.request(limit=0)
    except ValueError as error:
        assert "greater than zero" in str(error)
    else:
        raise AssertionError(
            "Invalid candle limit was accepted."
        )



# Network failures


@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_request_timeout(mock_get):

    mock_get.side_effect = requests.Timeout()

    provider = make_provider()

    try:
        provider.request()
    except ProviderTimeoutError:
        pass
    else:
        raise AssertionError(
            "Timeout was not classified correctly."
        )


@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_request_connection_error(mock_get):

    mock_get.side_effect = requests.ConnectionError()

    provider = make_provider()

    try:
        provider.request()
    except ProviderConnectionError:
        pass
    else:
        raise AssertionError(
            "Connection failure was not classified correctly."
        )


@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_request_invalid_json(mock_get):

    response = Mock()
    response.status_code = 200
    response.json.side_effect = ValueError()

    mock_get.return_value = response

    provider = make_provider()

    try:
        provider.request()
    except ProviderDataError:
        pass
    else:
        raise AssertionError(
            "Invalid JSON was not classified correctly."
        )



# API error classification


def assert_api_error(
    status_code,
    data,
    expected_exception,
):
    provider = make_provider()

    try:
        provider._raise_api_error(
            status_code,
            data,
        )
    except expected_exception:
        pass
    else:
        raise AssertionError(
            f"Expected {expected_exception.__name__}."
        )


def test_authentication_error():
    assert_api_error(
        401,
        {"message": "Invalid API key"},
        ProviderAuthenticationError,
    )


def test_rate_limit_error():
    assert_api_error(
        429,
        {"message": "Too many requests"},
        ProviderRateLimitError,
    )


def test_plan_restriction_error():
    assert_api_error(
        403,
        {"message": "This feature is available starting with a paid plan"},
        ProviderAuthenticationError,
    )


def test_unsupported_symbol_error():
    assert_api_error(
        400,
        {"message": "Symbol not found"},
        ProviderMarketUnsupportedError,
    )


def test_server_error():
    assert_api_error(
        500,
        {"message": "Internal server error"},
        ProviderUnavailableError,
    )



# Candle Mapping


def test_map_candles():

    provider = make_provider()

    response = {
        "values": [
            {
                "datetime": "2026-08-23 18:10:00",
                "open": "100",
                "high": "110",
                "low": "90",
                "close": "105",
            },
            {
                "datetime": "2026-08-23 18:05:00",
                "open": "95",
                "high": "102",
                "low": "94",
                "close": "100",
            },
        ]
    }

    candles = provider.map_candles(response)

    assert len(candles) == 2

    assert candles[0].time == "2026-08-23 18:05:00"
    assert candles[1].time == "2026-08-23 18:10:00"

    assert candles[0].open == 95.0
    assert candles[0].high == 102.0
    assert candles[0].low == 94.0
    assert candles[0].close == 100.0


def test_map_candles_missing_values():

    provider = make_provider()

    try:
        provider.map_candles({})
    except ProviderDataError:
        pass
    else:
        raise AssertionError(
            "Missing candle values were accepted."
        )


def test_map_candles_invalid_data():

    provider = make_provider()

    response = {
        "values": [
            {
                "datetime": "2026-08-23 18:05:00",
                "open": "INVALID",
                "high": "102",
                "low": "94",
                "close": "100",
            }
        ]
    }

    try:
        provider.map_candles(response)
    except ProviderDataError:
        pass
    else:
        raise AssertionError(
            "Invalid candle data was accepted."
        )



# Load composition


@patch(
    "backend.providers.twelvedata_provider.requests.get"
)
def test_load_returns_candles(mock_get):

    mock_get.return_value = fake_response(
        data={
            "status": "ok",
            "values": [
                {
                    "datetime": "2026-08-23 18:10:00",
                    "open": "100",
                    "high": "110",
                    "low": "90",
                    "close": "105",
                }
            ],
        }
    )

    provider = make_provider()

    candles = provider.load()

    assert len(candles) == 1
    assert candles[0].close == 105.0


print(
    "TwelveDataProvider contract test module loaded."
)



# Test Runner


if __name__ == "__main__":

    tests = [
        test_timeframe_mapping,
        test_invalid_timeframe_rejected_by_scanner_config,
        test_eurusd_symbol_resolution,
        test_explicit_provider_symbol,
        test_unsupported_market,
        test_probe_success,
        test_probe_missing_api_key,
        test_probe_unsupported_market,
        test_request_builds_expected_parameters,
        test_request_invalid_limit,
        test_request_timeout,
        test_request_connection_error,
        test_request_invalid_json,
        test_authentication_error,
        test_rate_limit_error,
        test_plan_restriction_error,
        test_unsupported_symbol_error,
        test_server_error,
        test_map_candles,
        test_map_candles_missing_values,
        test_map_candles_invalid_data,
        test_load_returns_candles,
    ]

    passed = 0

    print(
        "\n=== TWELVE DATA PROVIDER CONTRACT TEST ==="
    )

    for test in tests:

        try:
            test()
            passed += 1

            print(
                f"PASS: {test.__name__}"
            )

        except Exception as error:

            print(
                f"FAIL: {test.__name__}"
            )
            print(
                f"      {type(error).__name__}: {error}"
            )

            raise

    print(
        "\nPASS: TwelveDataProvider contract verified."
    )

    print(
        f"Tests passed: {passed}/{len(tests)}"
    )
