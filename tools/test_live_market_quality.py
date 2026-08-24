"""
test_live_market_quality.py

Live market-data quality gate for Andy Scanner.

Priority markets:
    EURUSD
    GBPUSD
    USDJPY
    XAUUSD
"""

from datetime import datetime, timezone

from backend.register_providers import register_providers
from backend.pipeline.pipeline_factory import PipelineFactory


MARKETS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "XAUUSD",
]

TIMEFRAME = "M5"


def check_chronological(candles):
    for index in range(1, len(candles)):
        previous = candles[index - 1].time
        current = candles[index].time

        if current <= previous:
            return False, (
                f"Non-chronological candles: "
                f"{previous} -> {current}"
            )

    return True, "Chronological order OK."


def check_duplicates(candles):
    timestamps = [
        candle.time
        for candle in candles
    ]

    if len(timestamps) != len(set(timestamps)):
        return False, "Duplicate candle timestamps detected."

    return True, "No duplicate timestamps."


def check_ohlc(candles):
    for candle in candles:

        if candle.high < max(
            candle.open,
            candle.close,
        ):
            return False, (
                f"Invalid high at {candle.time}"
            )

        if candle.low > min(
            candle.open,
            candle.close,
        ):
            return False, (
                f"Invalid low at {candle.time}"
            )

        if candle.high < candle.low:
            return False, (
                f"High below low at {candle.time}"
            )

    return True, "OHLC integrity OK."


def check_m5_spacing(candles):
    if len(candles) < 2:
        return False, "Not enough candles."

    for index in range(1, len(candles)):

        previous = datetime.fromisoformat(
            candles[index - 1].time
        )

        current = datetime.fromisoformat(
            candles[index].time
        )

        gap = (
            current - previous
        ).total_seconds()

        if gap != 300:
            return False, (
                f"Invalid M5 gap: "
                f"{candles[index - 1].time} -> "
                f"{candles[index].time} "
                f"({gap} seconds)"
            )

    return True, "M5 spacing OK."


def check_freshness(candles):
    if not candles:
        return False, "No candles."

    latest = datetime.fromisoformat(
        candles[-1].time
    )

    if latest.tzinfo is None:
        latest = latest.replace(
            tzinfo=timezone.utc
        )

    now = datetime.now(timezone.utc)

    age = (
        now - latest
    ).total_seconds()

    maximum_age = 600

    if age > maximum_age:
        return False, (
            f"Latest candle is stale: "
            f"{candles[-1].time}; "
            f"age={round(age, 1)}s"
        )

    return True, (
        f"Freshness OK: age={round(age, 1)}s."
    )


def main():

    register_providers()

    pipeline = PipelineFactory.create()

    overall_success = True

    print()
    print("=" * 78)
    print("ANDY SCANNER — LIVE MARKET DATA QUALITY GATE")
    print("=" * 78)

    for market in MARKETS:

        print()
        print("-" * 78)
        print(f"MARKET: {market}")
        print("-" * 78)

        result = pipeline.run(
            market=market,
            timeframe=TIMEFRAME,
        )

        if not result.success:

            overall_success = False

            print("PIPELINE: FAIL")
            print(
                "ERROR TYPE:",
                type(result.error).__name__,
            )
            print(
                "ERROR:",
                result.error,
            )

            continue

        scan = result.metadata[
            "scan_result"
        ]

        candles = scan.candles

        print("PIPELINE: PASS")
        print(
            "PROVIDER:",
            scan.provider,
        )
        print(
            "SYMBOL:",
            scan.provider_symbol,
        )
        print(
            "CANDLES:",
            len(candles),
        )

        checks = [
            (
                "COUNT",
                len(candles) >= 3,
                "Minimum candle count satisfied.",
            ),
            (
                "CHRONOLOGY",
                *check_chronological(candles),
            ),
            (
                "DUPLICATES",
                *check_duplicates(candles),
            ),
            (
                "OHLC",
                *check_ohlc(candles),
            ),
            (
                "M5 SPACING",
                *check_m5_spacing(candles),
            ),
            (
                "FRESHNESS",
                *check_freshness(candles),
            ),
        ]

        for name, passed, message in checks:

            status = "PASS" if passed else "FAIL"

            print(
                f"{name:12}: {status} - {message}"
            )

            if not passed:
                overall_success = False

        print()
        print("LATEST CANDLE:", candles[-1].time)

        print(
            "TREND:",
            scan.analyzer.trend(),
        )

        print(
            "SIGNAL:",
            scan.signal.direction,
        )

        print(
            "CONFIDENCE:",
            scan.signal.confidence,
        )

    print()
    print("=" * 78)

    if overall_success:
        print(
            "FINAL RESULT: LIVE DATA QUALITY GATE PASSED"
        )
    else:
        print(
            "FINAL RESULT: LIVE DATA QUALITY GATE FAILED"
        )

    print("=" * 78)


if __name__ == "__main__":
    main()
