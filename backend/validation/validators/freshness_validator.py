"""
freshness_validator.py

Validates that the latest market candle is sufficiently
recent for live market scanning.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from datetime import datetime, timezone


class FreshnessValidator:
    """
    Validates live market-data freshness.

    The validator compares the timestamp of the latest
    candle against the current UTC time.
    """

    TIMEFRAME_SECONDS = {
        "M1": 60,
        "M5": 300,
        "M15": 900,
        "M30": 1800,
        "H1": 3600,
        "H4": 14400,
        "D1": 86400,
    }

    # Allow the latest candle to be older than one exact
    # timeframe interval because providers may publish
    # candles with a small reporting delay.
    DEFAULT_MULTIPLIER = 2

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
        Convert a candle timestamp into a datetime.
        """

        if isinstance(value, datetime):

            if value.tzinfo is None:
                return value.replace(
                    tzinfo=timezone.utc
                )

            return value.astimezone(
                timezone.utc
            )

        if not isinstance(value, str):
            raise ValueError(
                "Candle timestamp must be a string "
                "or datetime."
            )

        value = value.strip()

        for timestamp_format in cls.TIMESTAMP_FORMATS:

            try:

                parsed = datetime.strptime(
                    value,
                    timestamp_format,
                )

                return parsed.replace(
                    tzinfo=timezone.utc
                )

            except ValueError:
                continue

        raise ValueError(
            f"Unsupported candle timestamp format: "
            f"{value}"
        )

    # ==================================================
    # Validation
    # ==================================================

    def validate(
        self,
        candles,
        timeframe,
        now=None,
        multiplier=None,
    ):
        """
        Validate the freshness of the latest candle.

        Parameters
        ----------
        candles:
            List of Candle objects.

        timeframe:
            AndyScanner timeframe.

        now:
            Optional current UTC datetime. Mainly useful
            for deterministic testing.

        multiplier:
            Maximum number of timeframe intervals allowed
            before the data is considered stale.

        Returns
        -------
        tuple(bool, str)
        """

        if not candles:

            return (
                False,
                "Cannot validate freshness: "
                "no candles available.",
            )

        timeframe = timeframe.upper()

        interval_seconds = self.TIMEFRAME_SECONDS.get(
            timeframe
        )

        if interval_seconds is None:

            return (
                False,
                f"Unsupported timeframe '{timeframe}'.",
            )

        if multiplier is None:
            multiplier = self.DEFAULT_MULTIPLIER

        if multiplier <= 0:

            return (
                False,
                "Freshness multiplier must be greater "
                "than zero.",
            )

        try:

            latest = self._parse_timestamp(
                candles[-1].time
            )

        except ValueError as error:

            return (
                False,
                str(error),
            )

        if now is None:

            current = datetime.now(
                timezone.utc
            )

        else:

            current = self._parse_timestamp(now)

        age_seconds = (
            current - latest
        ).total_seconds()

        # Future timestamps are invalid for live scanning.
        if age_seconds < 0:

            return (
                False,
                f"Latest candle timestamp "
                f"{candles[-1].time} is in the future.",
            )

        maximum_age = (
            interval_seconds * multiplier
        )

        if age_seconds > maximum_age:

            return (
                False,
                f"Market data is stale. "
                f"Latest candle: {candles[-1].time}; "
                f"age: {round(age_seconds, 1)} seconds; "
                f"maximum allowed: {maximum_age} seconds.",
            )

        return (
            True,
            "Market data freshness validation passed.",
        )
