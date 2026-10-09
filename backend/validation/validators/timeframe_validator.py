"""
timeframe_validator.py

Validates candle timeframe consistency and chronological order.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from datetime import datetime, timezone


class TimeframeValidator:
    """
    Validates chronological order and candle spacing.
    """

    TIMEFRAME_MAP = {
        "M1": 60,
        "M5": 300,
        "M15": 900,
        "M30": 1800,
        "H1": 3600,
        "H4": 14400,
        "D1": 86400,
    }

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

    def validate(self, candles, timeframe):
        """
        Validate chronological order and expected timeframe spacing.

        Returns
        -------
        tuple(bool, str)
        """

        if not isinstance(timeframe, str):
            return False, "Timeframe must be a string."

        timeframe = timeframe.upper()
        expected_gap = self.TIMEFRAME_MAP.get(timeframe)

        if expected_gap is None:
            return (
                False,
                f"Unsupported timeframe '{timeframe}'.",
            )

        if len(candles) < 2:
            return (
                True,
                "Not enough candles to validate timeframe.",
            )

        previous = None

        try:
            for candle in candles:
                current = self._parse_timestamp(candle.time)

                if previous is not None:
                    gap = (current - previous).total_seconds()

                    if gap <= 0:
                        return (
                            False,
                            "Candles are not in strictly "
                            "chronological order: "
                            f"{candle.time}.",
                        )

                    if gap != expected_gap:
                        return (
                            False,
                            f"Invalid timeframe gap between "
                            f"{previous.isoformat()} and "
                            f"{current.isoformat()}. "
                            f"Expected {expected_gap} seconds, "
                            f"got {gap} seconds.",
                        )

                previous = current

        except (ValueError, TypeError, AttributeError) as error:
            return False, str(error)

        return True, "Timeframe validation passed."