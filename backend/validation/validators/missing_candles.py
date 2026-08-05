"""
missing_candles.py

Detects missing candle data.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class MissingCandlesValidator:
    """
    Validates that candle data exists and contains
    the minimum number of candles required for analysis.
    """

    def __init__(self, minimum_candles=3):
        self.minimum_candles = minimum_candles

    # ==================================================
    # Validation
    # ==================================================

    def validate(self, candles):
        """
        Validate candle availability.

        Returns
        -------
        tuple(bool, str)
        """

        if candles is None:
            return (
                False,
                "No candle data received."
            )

        if len(candles) == 0:
            return (
                False,
                "Empty candle dataset."
            )

        if len(candles) < self.minimum_candles:
            return (
                False,
                f"Only {len(candles)} candles available "
                f"(minimum {self.minimum_candles} required)."
            )

        return (
            True,
            "Missing candle validation passed."
        )