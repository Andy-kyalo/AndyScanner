"""
timeframe_validator.py

Validates candle timeframe consistency.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

from datetime import datetime


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

    # ==================================================
    # Validation
    # ==================================================

    def validate(self, candles, timeframe):
        """
        Validate candle spacing.

        Parameters
        ----------
        candles : list
        timeframe : str

        Returns
        -------
        tuple(bool, str)
        """

        timeframe = timeframe.upper()

        expected_gap = self.TIMEFRAME_MAP.get(timeframe)

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

        for i in range(1, len(candles)):

            previous = datetime.strptime(
                candles[i - 1].time,
                "%H:%M"
            )

            current = datetime.strptime(
                candles[i].time,
                "%H:%M"
            )

            gap = (current - previous).seconds

            if gap != expected_gap:
                return (
                    False,
                    f"Invalid timeframe gap between "
                    f"{candles[i - 1].time} and "
                    f"{candles[i].time}."
                )

        return (
            True,
            "Timeframe validation passed."
        )