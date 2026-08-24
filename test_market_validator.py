"""
test_market_validator.py

Market validation contract tests.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime, timezone, timedelta
from math import inf, nan

from backend.candle import Candle
from backend.validation.market_validator import MarketValidator


def make_candles(
    count=4,
    timeframe_minutes=5,
    age_minutes=5,
):
    """
    Create a valid candle sequence for validation tests.
    """

    now = datetime.now(
        timezone.utc
    ).replace(
        microsecond=0
    )

    latest = now - timedelta(
        minutes=age_minutes
    )

    candles = []

    for i in range(count):

        timestamp = (
            latest
            - timedelta(
                minutes=(
                    (count - 1 - i)
                    * timeframe_minutes
                )
            )
        )

        candles.append(
            Candle(
                time=timestamp,
                open_price=100.0 + i,
                high=105.0 + i,
                low=99.0 + i,
                close=104.0 + i,
            )
        )

    return candles


def assert_invalid_price(
    candles,
    expected_text,
):
    """
    Assert that invalid OHLC data is rejected.
    """

    validator = MarketValidator()

    valid, message = validator.validate(
        candles,
        "M5",
    )

    assert valid is False
    assert expected_text in message


# ==========================================================
# Valid Market Data
# ==========================================================

def test_valid_market_data():

    candles = make_candles()

    validator = MarketValidator()

    valid, message = validator.validate(
        candles,
        "M5",
    )

    assert valid is True
    assert message == (
        "Market data validation passed."
    )


# ==========================================================
# NaN
# ==========================================================

def test_nan_open():

    candles = make_candles()

    candles[2].open = nan

    assert_invalid_price(
        candles,
        "Invalid price",
    )


def test_nan_high():

    candles = make_candles()

    candles[2].high = nan

    assert_invalid_price(
        candles,
        "Invalid price",
    )


def test_nan_low():

    candles = make_candles()

    candles[2].low = nan

    assert_invalid_price(
        candles,
        "Invalid price",
    )


def test_nan_close():

    candles = make_candles()

    candles[2].close = nan

    assert_invalid_price(
        candles,
        "Invalid price",
    )


# ==========================================================
# Infinity
# ==========================================================

def test_positive_infinity():

    candles = make_candles()

    candles[2].high = inf

    assert_invalid_price(
        candles,
        "Invalid price",
    )


def test_negative_infinity():

    candles = make_candles()

    candles[2].low = -inf

    assert_invalid_price(
        candles,
        "Invalid price",
    )


# ==========================================================
# Existing OHLC Rules
# ==========================================================

def test_zero_price():

    candles = make_candles()

    candles[1].close = 0

    assert_invalid_price(
        candles,
        "Invalid price",
    )


def test_negative_price():

    candles = make_candles()

    candles[1].open = -1

    assert_invalid_price(
        candles,
        "Invalid price",
    )


def test_high_below_low():

    candles = make_candles()

    candles[1].high = 98
    candles[1].low = 99

    assert_invalid_price(
        candles,
        "High is below Low",
    )


def test_high_below_open():

    candles = make_candles()

    candles[1].high = 100
    candles[1].open = 101

    assert_invalid_price(
        candles,
        "High is below Open",
    )


def test_high_below_close():

    candles = make_candles()

    candles[1].high = 104
    candles[1].close = 105

    assert_invalid_price(
        candles,
        "High is below Close",
    )


def test_low_above_open():

    candles = make_candles()

    candles[1].low = 102
    candles[1].open = 101

    assert_invalid_price(
        candles,
        "Low is above Open",
    )


def test_low_above_close():

    candles = make_candles()

    candles[1].low = 102
    candles[1].close = 101
    candles[1].open = 103
    candles[1].high = 105

    assert_invalid_price(
        candles,
        "Low is above Close",
    )


# ==========================================================
# Test Runner
# ==========================================================

def test():

    tests = [
        test_valid_market_data,

        test_nan_open,
        test_nan_high,
        test_nan_low,
        test_nan_close,

        test_positive_infinity,
        test_negative_infinity,

        test_zero_price,
        test_negative_price,

        test_high_below_low,
        test_high_below_open,
        test_high_below_close,
        test_low_above_open,
        test_low_above_close,
    ]

    print(
        "\n=== MARKET VALIDATOR CONTRACT TEST ==="
    )

    passed = 0

    for test_case in tests:

        try:

            test_case()

            print(
                f"PASS: {test_case.__name__}"
            )

            passed += 1

        except Exception as error:

            print(
                f"FAIL: {test_case.__name__}"
            )

            print(
                f"      {type(error).__name__}: "
                f"{error}"
            )

            raise

    print(
        f"\nPASS: Market validation contract verified."
    )

    print(
        f"Tests passed: {passed}/{len(tests)}"
    )


if __name__ == "__main__":
    test()
