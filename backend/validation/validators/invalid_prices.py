"""
invalid_prices.py

Detects invalid OHLC candle prices.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

import math


class InvalidPricesValidator:
    """
    Validates candle OHLC prices.
    """

    # ==================================================
    # Validation
    # ==================================================

    def validate(self, candles):
        """
        Validate candle OHLC prices.

        Rejects:

        - non-numeric prices
        - NaN values
        - positive infinity
        - negative infinity
        - zero prices
        - negative prices
        - impossible OHLC relationships

        Returns
        -------
        tuple(bool, str)
        """

        for candle in candles:

            prices = {
                "open": candle.open,
                "high": candle.high,
                "low": candle.low,
                "close": candle.close,
            }

            # --------------------------------------------------
            # Numeric / finite validation
            # --------------------------------------------------

            for price_name, price in prices.items():

                if not isinstance(
                    price,
                    (int, float),
                ):

                    return (
                        False,
                        f"Invalid price detected at "
                        f"{candle.time}.",
                    )

                if not math.isfinite(price):

                    return (
                        False,
                        f"Invalid price detected at "
                        f"{candle.time}.",
                    )

                if price <= 0:

                    return (
                        False,
                        f"Invalid price detected at "
                        f"{candle.time}.",
                    )

            # --------------------------------------------------
            # OHLC relationship validation
            # --------------------------------------------------

            if candle.high < candle.low:

                return (
                    False,
                    f"High is below Low at {candle.time}.",
                )

            if candle.high < candle.open:

                return (
                    False,
                    f"High is below Open at {candle.time}.",
                )

            if candle.high < candle.close:

                return (
                    False,
                    f"High is below Close at {candle.time}.",
                )

            if candle.low > candle.open:

                return (
                    False,
                    f"Low is above Open at {candle.time}.",
                )

            if candle.low > candle.close:

                return (
                    False,
                    f"Low is above Close at {candle.time}.",
                )

        return (
            True,
            "Price validation passed.",
        )