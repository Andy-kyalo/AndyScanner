"""
duplicate_candles.py

Detects duplicate candles.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class DuplicateCandlesValidator:
    """
    Detects duplicate candle timestamps.
    """

    # ==================================================
    # Validation
    # ==================================================

    def validate(self, candles):
        """
        Validate duplicate candle timestamps.

        Returns
        -------
        tuple(bool, str)
        """

        timestamps = set()

        for candle in candles:

            if candle.time in timestamps:

                return (
                    False,
                    f"Duplicate candle detected at {candle.time}."
                )

            timestamps.add(candle.time)

        return (
            True,
            "Duplicate candle validation passed."
        )