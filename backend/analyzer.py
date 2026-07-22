"""
analyzer.py

Market analysis engine for Andy Scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.signal import Signal


class Analyzer:
    """
    Performs all market analysis operations.
    """

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(self, candles):
        self.candles = candles

    # ==========================================
    # Basic Market Analysis
    # ==========================================

    def highest_high(self):
        """Return the highest high."""

        if not self.candles:
            return None

        highest = self.candles[0].high

        for candle in self.candles:
            if candle.high > highest:
                highest = candle.high

        return highest

    def lowest_low(self):
        """Return the lowest low."""

        if not self.candles:
            return None

        lowest = self.candles[0].low

        for candle in self.candles:
            if candle.low < lowest:
                lowest = candle.low

        return lowest

    def trend(self):
        """Determine market trend."""

        if not self.candles:
            return "UNKNOWN"

        first_close = self.candles[0].close
        last_close = self.candles[-1].close

        if last_close > first_close:
            return "UPTREND"

        if last_close < first_close:
            return "DOWNTREND"

        return "SIDEWAYS"

    # ==========================================
    # Candle Analysis
    # ==========================================

    def strongest_candle(self):
        """Return candle with largest body."""

        if not self.candles:
            return None

        largest = self.candles[0]

        for candle in self.candles:
            if candle.body_size() > largest.body_size():
                largest = candle

        return largest

    # ==========================================
    # Swing Detection
    # ==========================================

    def swing_highs(self):
        """Return detected swing highs."""

        swings = []

        for i in range(1, len(self.candles) - 1):

            previous = self.candles[i - 1]
            current = self.candles[i]
            next_candle = self.candles[i + 1]

            if (
                current.high > previous.high
                and current.high > next_candle.high
            ):
                swings.append(current)

        return swings

    def swing_lows(self):
        """Return detected swing lows."""

        swings = []

        for i in range(1, len(self.candles) - 1):

            previous = self.candles[i - 1]
            current = self.candles[i]
            next_candle = self.candles[i + 1]

            if (
                current.low < previous.low
                and current.low < next_candle.low
            ):
                swings.append(current)

        return swings

    # ==========================================
    # Break of Structure (BOS)
    # ==========================================

    def bullish_bos(self):
        """Detect bullish BOS."""

        highs = self.swing_highs()

        if not highs:
            return False

        return self.candles[-1].close > highs[-1].high

    def bearish_bos(self):
        """Detect bearish BOS."""

        lows = self.swing_lows()

        if not lows:
            return False

        return self.candles[-1].close < lows[-1].low

    # ==========================================
    # Fair Value Gap (FVG)
    # ==========================================

    def bullish_fvg(self):
        """Return bullish Fair Value Gaps."""

        fvgs = []

        for i in range(len(self.candles) - 2):

            first = self.candles[i]
            third = self.candles[i + 2]

            if third.low > first.high:
                fvgs.append((first, third))

        return fvgs

    # ==========================================
    # Change of Character (CHoCH)
    # ==========================================

    def bullish_choch(self):
        """Detect bullish CHoCH."""

        return (
            self.trend() == "DOWNTREND"
            and self.bullish_bos()
        )

    def bearish_choch(self):
        """Detect bearish CHoCH."""

        return (
            self.trend() == "UPTREND"
            and self.bearish_bos()
        )

    # ==========================================
    # Liquidity
    # ==========================================

    def buy_side_liquidity(self):
        """Return buy-side liquidity."""

        return self.swing_highs()

    def sell_side_liquidity(self):
        """Return sell-side liquidity."""

        return self.swing_lows()

    # ==========================================
    # Order Blocks
    # ==========================================

    def bullish_order_block(self):
        """Return bullish order block."""

        if not self.bullish_bos():
            return None

        for candle in reversed(self.candles[:-1]):

            if candle.is_bearish():
                return candle

        return None

    # ==========================================
    # Engulfing Patterns
    # ==========================================

    def bullish_engulfing(self):
        """Return bullish engulfing candles."""

        patterns = []

        for i in range(1, len(self.candles)):

            previous = self.candles[i - 1]
            current = self.candles[i]

            if (
                previous.is_bearish()
                and current.is_bullish()
                and current.open < previous.close
                and current.close > previous.open
            ):
                patterns.append(current)

        return patterns

    def bearish_engulfing(self):
        """Return bearish engulfing candles."""

        patterns = []

        for i in range(1, len(self.candles)):

            previous = self.candles[i - 1]
            current = self.candles[i]

            if (
                previous.is_bullish()
                and current.is_bearish()
                and current.open > previous.close
                and current.close < previous.open
            ):
                patterns.append(current)

        return patterns

    # ==========================================
    # Trading Signal
    # ==========================================

    def generate_signal(self):
        """
        Generate trading signal.
        """

        confidence = 0

        if self.bullish_bos():
            confidence += 40

        if self.bullish_fvg():
            confidence += 30

        if self.trend() == "UPTREND":
            confidence += 30

        if confidence >= 70:
            direction = "BUY"

        elif self.bearish_bos():
            direction = "SELL"

        else:
            direction = "WAIT"

        return Signal(
            market="US30",
            timeframe="M5",
            direction=direction,
            confidence=confidence,
        )