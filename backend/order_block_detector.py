"""
order_block_detector.py

Order Block detector.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from typing import List, Optional

from backend.candle import Candle
from backend.bos_detector import BOSDetector


class OrderBlockDetector:
    """
    Detects Bullish and Bearish Order Blocks.
    """

    def __init__(self, candles: List[Candle]):

        if len(candles) < 3:
            raise ValueError(
                "At least 3 candles are required."
            )

        self.candles = candles
        self.bos = BOSDetector(candles)

    # ==========================================
    # Bullish Order Block
    # ==========================================

    def bullish_order_block(self) -> Optional[Candle]:

        if not self.bos.bullish_bos():
            return None

        for i in range(len(self.candles) - 2, -1, -1):

            candle = self.candles[i]
            next_candle = self.candles[i + 1]

            if (
                candle.is_bearish()
                and next_candle.is_bullish()
                and next_candle.close > candle.high
            ):
                return candle

        return None

    # ==========================================
    # Bearish Order Block
    # ==========================================

    def bearish_order_block(self) -> Optional[Candle]:

        if not self.bos.bearish_bos():
            return None

        for i in range(len(self.candles) - 2, -1, -1):

            candle = self.candles[i]
            next_candle = self.candles[i + 1]

            if (
                candle.is_bullish()
                and next_candle.is_bearish()
                and next_candle.close < candle.low
            ):
                return candle

        return None

    # ==========================================
    # Availability
    # ==========================================

    def has_bullish_order_block(self) -> bool:

        return self.bullish_order_block() is not None

    def has_bearish_order_block(self) -> bool:

        return self.bearish_order_block() is not None

    # ==========================================
    # Order Block Levels
    # ==========================================

    def bullish_order_block_high(self):

        block = self.bullish_order_block()

        return block.high if block else None

    def bullish_order_block_low(self):

        block = self.bullish_order_block()

        return block.low if block else None

    def bearish_order_block_high(self):

        block = self.bearish_order_block()

        return block.high if block else None

    def bearish_order_block_low(self):

        block = self.bearish_order_block()

        return block.low if block else None