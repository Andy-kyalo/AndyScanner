"""
candle.py

Represents a single market candle and provides
analysis utilities for price action.

Author: Andrew Kyalo
Project: Andy Scanner
"""


class Candle:
    """
    Represents one OHLC candle.
    """

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(self, time, open_price, high, low, close):
        """
        Initialize a candle.
        """

        if high < max(open_price, close):
            raise ValueError(
                f"{time}: High cannot be below Open or Close."
            )

        if low > min(open_price, close):
            raise ValueError(
                f"{time}: Low cannot be above Open or Close."
            )

        self.time = time
        self.open = open_price
        self.high = high
        self.low = low
        self.close = close

    # ==========================================
    # Candle Classification
    # ==========================================

    def get_type(self):
        """Return Bullish, Bearish or Doji."""

        if self.close > self.open:
            return "Bullish"

        if self.close < self.open:
            return "Bearish"

        return "Doji"

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.close < self.open

    # ==========================================
    # Measurements
    # ==========================================

    def body_size(self):
        return round(abs(self.close - self.open), 2)

    def range(self):
        return round(self.high - self.low, 2)

    def upper_wick(self):
        if self.is_bullish():
            wick = self.high - self.close
        else:
            wick = self.high - self.open

        return round(wick, 2)

    def lower_wick(self):
        if self.is_bullish():
            wick = self.open - self.low
        else:
            wick = self.close - self.low

        return round(wick, 2)

    def midpoint(self):
        return round((self.high + self.low) / 2, 2)

    # ==========================================
    # Candle Patterns
    # ==========================================

    def is_doji(self):
        return self.body_size() <= self.range() * 0.10

    def is_marubozu(self):
        return (
            self.upper_wick() <= self.range() * 0.05
            and self.lower_wick() <= self.range() * 0.05
        )

    def is_hammer(self):
        return (
            self.lower_wick() >= self.body_size() * 2
            and self.upper_wick() <= self.body_size()
        )

    def is_shooting_star(self):
        return (
            self.upper_wick() >= self.body_size() * 2
            and self.lower_wick() <= self.body_size()
        )

    # ==========================================
    # Display
    # ==========================================

    def show(self):
        """
        Print candle information.
        """

        print("========== Candle ==========")
        print(f"Time        : {self.time}")
        print(f"Open        : {self.open}")
        print(f"High        : {self.high}")
        print(f"Low         : {self.low}")
        print(f"Close       : {self.close}")
        print(f"Type        : {self.get_type()}")
        print(f"Body Size   : {self.body_size()}")
        print(f"Range       : {self.range()}")
        print(f"Upper Wick  : {self.upper_wick()}")
        print(f"Lower Wick  : {self.lower_wick()}")
        print(f"Midpoint    : {self.midpoint()}")
        print(f"Doji        : {'YES' if self.is_doji() else 'NO'}")
        print(f"Marubozu    : {'YES' if self.is_marubozu() else 'NO'}")
        print(f"Hammer      : {'YES' if self.is_hammer() else 'NO'}")
        print(f"ShootingStar: {'YES' if self.is_shooting_star() else 'NO'}")
        print("============================")