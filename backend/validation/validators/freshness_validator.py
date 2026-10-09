"""
freshness_validator.py

Validates live market-data freshness and chronological order.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime, timezone


class FreshnessValidator:
    """Validates ordering and freshness of the latest market candle."""

    TIMEFRAME_SECONDS = {
        "M1": 60,
        "M5": 300,
        "M15": 900,
        "M30": 1800,
        "H1": 3600,
        "H4": 14400,
        "D1": 86400,
    }

    DEFAULT_MULTIPLIER = 2

    TIMESTAMP_FORMATS = (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%S.%f",
    )

    @classmethod
    def _parse_timestamp(cls, value):
        """Parse supported timestamps and normalize them to UTC."""

        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc)

        if not isinstance(value, str):
            raise ValueError(
                "Unsupported candle timestamp type: "
                f"{type(value).__name__}"
            )

        value = value.strip()

        # Support ISO-8601 strings, including Z and UTC offsets.
        iso_value = (
            value[:-1] + "+00:00"
            if value.endswith(("Z", "z"))
            else value
        )

        try:
            parsed = datetime.fromisoformat(iso_value)
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=timezone.utc)
            return parsed.astimezone(timezone.utc)
        except ValueError:
            pass

        # Preserve support for the existing legacy formats.
        for timestamp_format in cls.TIMESTAMP_FORMATS:
            try:
                parsed = datetime.strptime(
                    value,
                    timestamp_format,
                )
                return parsed.replace(tzinfo=timezone.utc)
            except ValueError:
                continue

        raise ValueError(
            f"Unsupported candle timestamp format: {value}"
        )

    def validate(
        self,
        candles,
        timeframe,
        now=None,
        multiplier=None,
    ):
        """Validate chronological order and latest-candle freshness."""

        if not candles:
            return (
                False,
                "Cannot validate freshness: no candles available.",
            )

        if not isinstance(timeframe, str):
            return False, "Timeframe must be a string."

        timeframe = timeframe.upper()
        interval_seconds = self.TIMEFRAME_SECONDS.get(timeframe)

        if interval_seconds is None:
            return False, f"Unsupported timeframe '{timeframe}'."

        if multiplier is None:
            multiplier = self.DEFAULT_MULTIPLIER

        if (
            isinstance(multiplier, bool)
            or not isinstance(multiplier, (int, float))
            or multiplier <= 0
        ):
            return (
                False,
                "Freshness multiplier must be a positive number.",
            )

        try:
            parsed_candles = [
                self._parse_timestamp(candle.time)
                for candle in candles
            ]
        except (ValueError, TypeError, AttributeError) as error:
            return False, str(error)

        for previous, current in zip(
            parsed_candles,
            parsed_candles[1:],
        ):
            if current <= previous:
                return (
                    False,
                    "Candles are not in strictly chronological order.",
                )

        latest = parsed_candles[-1]

        if now is None:
            current_time = datetime.now(timezone.utc)
        else:
            try:
                current_time = self._parse_timestamp(now)
            except (ValueError, TypeError) as error:
                return False, str(error)

        age_seconds = (current_time - latest).total_seconds()

        if age_seconds < 0:
            return (
                False,
                f"Latest candle timestamp {candles[-1].time} "
                "is in the future.",
            )

        maximum_age = interval_seconds * multiplier

        if age_seconds > maximum_age:
            return (
                False,
                f"Market data is stale. "
                f"Latest candle: {candles[-1].time}; "
                f"age: {round(age_seconds, 1)} seconds; "
                f"maximum allowed: {maximum_age} seconds.",
            )

        return True, "Market data freshness validation passed."