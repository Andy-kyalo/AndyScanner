"""
market_validator.py

Validates market data before analysis.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.candle import Candle


class MarketValidator:

    MINIMUM_CANDLES = 4

    def __init__(self, candles):
        self.candles = candles

    def validate(self):

        if self.candles is None:
            raise ValueError("No candle data was provided.")

        if not isinstance(self.candles, list):
            raise ValueError("Candles must be a list.")

        if len(self.candles) == 0:
            raise ValueError("No candle data loaded.")

        if len(self.candles) < self.MINIMUM_CANDLES:
            raise ValueError(
                f"At least {self.MINIMUM_CANDLES} candles are required."
            )

        for index, candle in enumerate(self.candles, start=1):

            if not isinstance(candle, Candle):
                raise ValueError(
                    f"Item {index} is not a Candle object."
                )

            if candle.high < candle.low:
                raise ValueError(
                    f"Invalid candle {index}: High < Low."
                )

            if candle.high < max(candle.open, candle.close):
                raise ValueError(
                    f"Invalid candle {index}: High below Open/Close."
                )

            if candle.low > min(candle.open, candle.close):
                raise ValueError(
                    f"Invalid candle {index}: Low above Open/Close."
                )

        return True