"""
invalid_prices.py

Detects invalid OHLC candle prices.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""


class InvalidPricesValidator:
    """
    Validates candle OHLC prices.
    """

    # ==================================================
    # Validation
    # ==================================================

    def validate(self, candles):
        """
        Validate candle prices.

        Returns
        -------
        tuple(bool, str)
        """

        for candle in candles:

            if (
                candle.open <= 0
                or candle.high <= 0
                or candle.low <= 0
                or candle.close <= 0
            ):
                return (
                    False,
                    f"Invalid price detected at {candle.time}."
                )

            if candle.high < candle.low:
                return (
                    False,
                    f"High is below Low at {candle.time}."
                )

            if candle.high < candle.open:
                return (
                    False,
                    f"High is below Open at {candle.time}."
                )

            if candle.high < candle.close:
                return (
                    False,
                    f"High is below Close at {candle.time}."
                )

            if candle.low > candle.open:
                return (
                    False,
                    f"Low is above Open at {candle.time}."
                )

            if candle.low > candle.close:
                return (
                    False,
                    f"Low is above Close at {candle.time}."
                )

        return (
            True,
            "Price validation passed."
        )