class Candle:

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(self, time, open_price, high, low, close):

        if high < max(open_price, close):
            raise ValueError(
                f"Invalid candle at {time}: High cannot be below Open or Close."
            )

        if low > min(open_price, close):
            raise ValueError(
                f"Invalid candle at {time}: Low cannot be above Open or Close."
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

        if self.close > self.open:
            return "Bullish"

        elif self.close < self.open:
            return "Bearish"

        return "Doji"

    def is_bullish(self):
        return self.close > self.open

    def is_bearish(self):
        return self.close < self.open

    # ==========================================
    # Candle Measurements
    # ==========================================

    def body_size(self):
        return round(abs(self.close - self.open), 2)

    def range(self):
        return round(self.high - self.low, 2)

    def upper_wick(self):

        if self.is_bullish():
            return round(self.high - self.close, 2)

        return round(self.high - self.open, 2)

    def lower_wick(self):

        if self.is_bullish():
            return round(self.open - self.low, 2)

        return round(self.close - self.low, 2)

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