"""
timeframe_validator.py

Validates candle timeframe consistency.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from datetime import datetime, timezone

class TimeframeValidator:
    """
    Validates that candles follow the expected timeframe.
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

    # ==================================================
    # Timestamp Parsing
    # ==================================================

    @classmethod
    def _parse_timestamp(cls, value):
        """
        Parse and normalize a candle timestamp to UTC.

        Naive timestamps are interpreted as UTC.
        Timezone-aware timestamps are converted to UTC.
        """

        if isinstance(value, datetime):
            if value.tzinfo is None:
                return value.replace(tzinfo=timezone.utc)
            return value.astimezone(timezone.utc)

        if not isinstance(value, str):
            raise ValueError(
                f"Unsupported candle timestamp type: "
                f"{type(value).__name__}"
            )

        value = value.strip()

        for timestamp_format in cls.TIMESTAMP_FORMATS:
            try:
                parsed = datetime.strptime(value, timestamp_format)
                return parsed.replace(tzinfo=timezone.utc)
            except ValueError:
                continue

        raise ValueError(
            f"Unsupported candle timestamp format: "
            f"{value}"
        )

    # ==================================================
    # Validation
    # ==================================================

    def validate(self, candles, timeframe):
        """
        Validate candle spacing against the requested timeframe.

        Returns
        -------
        tuple(bool, str)
        """

        timeframe = timeframe.upper()

        expected_gap = self.TIMEFRAME_MAP.get(
            timeframe
        )

        if expected_gap is None:
            return (
                False,
                f"Unsupported timeframe '{timeframe}'."
            )

        if len(candles) < 2:
            return (
                True,
                "Not enough candles to validate timeframe."
            )

        try:

            for i in range(1, len(candles)):

                previous = self._parse_timestamp(
                    candles[i - 1].time
                )

                current = self._parse_timestamp(
                    candles[i].time
                )

                gap = (
                    current - previous
                ).total_seconds()

                if gap != expected_gap:

                    return (
                        False,
                        f"Invalid timeframe gap between "
                        f"{candles[i - 1].time} and "
                        f"{candles[i].time}. "
                        f"Expected {expected_gap} seconds, "
                        f"got {gap} seconds."
                    )

        except ValueError as error:

            return (
                False,
                str(error),
            )

        return (
            True,
            "Timeframe validation passed."
        )
