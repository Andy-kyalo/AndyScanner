from datetime import datetime, timedelta, timezone

from backend.candle import Candle
from backend.validation.validators.timeframe_validator import (
    TimeframeValidator,
)


def make_candles(
    count=4,
    timeframe_seconds=300,
    start=None,
):
    if start is None:
        start = datetime(
            2026,
            8,
            24,
            10,
            0,
            0,
            tzinfo=timezone.utc,
        )

    candles = []

    for i in range(count):
        timestamp = start + timedelta(
            seconds=i * timeframe_seconds
        )

        candles.append(
            Candle(
                time=timestamp,
                open_price=100 + i,
                high=105 + i,
                low=99 + i,
                close=104 + i,
            )
        )

    return candles


def assert_pass(candles, timeframe):
    valid, message = TimeframeValidator().validate(
        candles,
        timeframe,
    )

    assert valid is True, message


def assert_fail(candles, timeframe, expected_text):
    valid, message = TimeframeValidator().validate(
        candles,
        timeframe,
    )

    assert valid is False
    assert expected_text in message


# ==========================================================
# Valid data
# ==========================================================

def test_valid_m5():
    candles = make_candles(
        timeframe_seconds=300,
    )

    assert_pass(
        candles,
        "M5",
    )


def test_valid_m1():
    candles = make_candles(
        timeframe_seconds=60,
    )

    assert_pass(
        candles,
        "M1",
    )


def test_valid_h1():
    candles = make_candles(
        timeframe_seconds=3600,
    )

    assert_pass(
        candles,
        "H1",
    )


# ==========================================================
# Insufficient data
# ==========================================================

def test_single_candle():

    candles = make_candles(
        count=1,
    )

    assert_pass(
        candles,
        "M5",
    )


# ==========================================================
# Invalid timeframe
# ==========================================================

def test_invalid_timeframe():

    candles = make_candles()

    assert_fail(
        candles,
        "INVALID",
        "Unsupported timeframe",
    )


# ==========================================================
# Invalid spacing
# ==========================================================

def test_gap_too_large():

    candles = make_candles()

    candles[2].time = (
        candles[1].time
        + timedelta(minutes=10)
    )

    assert_fail(
        candles,
        "M5",
        "Invalid timeframe gap",
    )


def test_gap_too_small():

    candles = make_candles()

    candles[2].time = (
        candles[1].time
        + timedelta(minutes=2)
    )

    assert_fail(
        candles,
        "M5",
        "Invalid timeframe gap",
    )


# ==========================================================
# Duplicate timestamp
# ==========================================================

def test_duplicate_timestamp():

    candles = make_candles()

    candles[2].time = candles[1].time

    assert_fail(
        candles,
        "M5",
        "Invalid timeframe gap",
    )


# ==========================================================
# Reverse ordering
# ==========================================================

def test_reverse_timestamp():

    candles = make_candles()

    candles[2].time = (
        candles[1].time
        - timedelta(minutes=5)
    )

    assert_fail(
        candles,
        "M5",
        "Invalid timeframe gap",
    )


# ==========================================================
# Timestamp parsing
# ==========================================================

def test_string_timestamp():

    candles = make_candles()

    for candle in candles:
        candle.time = candle.time.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    assert_pass(
        candles,
        "M5",
    )


def test_iso_timestamp():

    candles = make_candles()

    for candle in candles:
        candle.time = candle.time.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    assert_pass(
        candles,
        "M5",
    )


def test_invalid_timestamp():

    candles = make_candles()

    candles[1].time = "NOT-A-TIMESTAMP"

    assert_fail(
        candles,
        "M5",
        "Unsupported candle timestamp format",
    )
# ==========================================================
# Timezone normalization
# ==========================================================

def test_naive_datetime_is_treated_as_utc():

    candles = make_candles()

    for candle in candles:
        candle.time = candle.time.replace(
            tzinfo=None
        )

    assert_pass(
        candles,
        "M5",
    )


def test_mixed_timezone_datetimes():

    start = datetime(
        2026,
        8,
        24,
        10,
        0,
        0,
        tzinfo=timezone.utc,
    )

    candles = [
        Candle(
            time=start,
            open_price=100.0,
            high=105.0,
            low=99.0,
            close=104.0,
        ),
        Candle(
            time=(
                start.astimezone(
                    timezone(timedelta(hours=3))
                )
                + timedelta(minutes=5)
            ),
            open_price=101.0,
            high=106.0,
            low=100.0,
            close=105.0,
        ),
    ]

    assert_pass(
        candles,
        "M5",
    )

# ==========================================================
# Test runner
# ==========================================================

def test():

    tests = [
        test_valid_m5,
        test_valid_m1,
        test_valid_h1,
        test_single_candle,
        test_invalid_timeframe,
        test_gap_too_large,
        test_gap_too_small,
        test_duplicate_timestamp,
        test_reverse_timestamp,
        test_string_timestamp,
        test_iso_timestamp,
        test_invalid_timestamp,
        test_naive_datetime_is_treated_as_utc,
        test_mixed_timezone_datetimes,
    ]

    print()
    print("=== TIMEFRAME VALIDATOR CONTRACT TEST ===")

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

    print()
    print(
        "PASS: Timeframe validation contract verified."
    )

    print(
        f"Tests passed: {passed}/{len(tests)}"
    )


if __name__ == "__main__":
    test()
