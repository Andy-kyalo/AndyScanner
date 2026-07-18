
from backend.signal import Signal


class Analyzer:

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(self, candles):
        self.candles = candles

    # ==========================================
    # Basic Market Analysis
    # ==========================================

    def highest_high(self):

        highest = self.candles[0].high

        for candle in self.candles:
            if candle.high > highest:
                highest = candle.high

        return highest

    def lowest_low(self):

        lowest = self.candles[0].low

        for candle in self.candles:
            if candle.low < lowest:
                lowest = candle.low

        return lowest

    def trend(self):

        first_close = self.candles[0].close
        last_close = self.candles[-1].close

        if last_close > first_close:
            return "UPTREND"

        elif last_close < first_close:
            return "DOWNTREND"

        else:
            return "SIDEWAYS"

    # ==========================================
    # Candle Analysis
    # ==========================================

    def strongest_candle(self):

        largest = self.candles[0]

        for candle in self.candles:
            if candle.body_size() > largest.body_size():
                largest = candle

        return largest
        
        # ==========================================
    # Trading Signal
    # ==========================================

    def generate_signal(self):

        confidence = 0

        if self.bullish_bos():
            confidence += 40

        if len(self.bullish_fvg()) > 0:
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
            "US30",
            "M5",
            direction,
            confidence
        )

    # ==========================================
    # Swing Detection
    # ==========================================

    def swing_highs(self):

        swing_highs = []

        for i in range(1, len(self.candles) - 1):

            previous = self.candles[i - 1]
            current = self.candles[i]
            next_candle = self.candles[i + 1]

            if current.high > previous.high and current.high > next_candle.high:
                swing_highs.append(current)

        return swing_highs

    def swing_lows(self):

        swing_lows = []

        for i in range(1, len(self.candles) - 1):

            previous = self.candles[i - 1]
            current = self.candles[i]
            next_candle = self.candles[i + 1]

            if current.low < previous.low and current.low < next_candle.low:
                swing_lows.append(current)

        return swing_lows

    # ==========================================
    # Break of Structure (BOS)
    # ==========================================

    def bullish_bos(self):

        swing_highs = self.swing_highs()

        if len(swing_highs) == 0:
            return False

        last_swing_high = swing_highs[-1]
        last_candle = self.candles[-1]

        return last_candle.close > last_swing_high.high

    def bearish_bos(self):

        swing_lows = self.swing_lows()

        if len(swing_lows) == 0:
            return False

        last_swing_low = swing_lows[-1]
        last_candle = self.candles[-1]

        return last_candle.close < last_swing_low.low

    # ==========================================
    # Fair Value Gap (FVG)
    # ==========================================

    def bullish_fvg(self):

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

        return (
            self.trend() == "DOWNTREND"
            and self.bullish_bos()
        )

    def bearish_choch(self):

        return (
            self.trend() == "UPTREND"
            and self.bearish_bos()
        )
        
    from backend.signal import Signal
        
            # ==========================================
    # Liquidity Detection
    # ==========================================
    
    def buy_side_liquidity(self):

        liquidity = []

        highs = self.swing_highs()

        for candle in highs:
            liquidity.append(candle)

        return liquidity
        
        
    def sell_side_liquidity(self):

        liquidity = []

        lows = self.swing_lows()

        for candle in lows:
            liquidity.append(candle)

        return liquidity
        
        # ==========================================
       # Order Blocks
# ==========================================

    def bullish_order_block(self):

        if not self.bullish_bos():
            return None

        for i in range(len(self.candles) - 2, -1, -1):

            candle = self.candles[i]

            if candle.get_type() == "Bearish":
                return candle

        return None
    
    
    def bullish_engulfing(self):

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
    