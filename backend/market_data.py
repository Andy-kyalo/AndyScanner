"""
market_data.py

Standard market data model used throughout Andy Scanner.

Every market provider (MT5, TradingView, Binance,
Polygon, CSV, Simulation, etc.) must convert its
raw data into this format before passing it to the
scanner.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MarketData:
    """
    Represents one OHLCV market candle.
    """

    symbol: str
    timeframe: str

    time: str

    open: float
    high: float
    low: float
    close: float

    volume: float = 0.0

    @property
    def bullish(self):
        return self.close > self.open

    @property
    def bearish(self):
        return self.close < self.open

    @property
    def body(self):
        return abs(self.close - self.open)

    @property
    def range(self):
        return self.high - self.low

    def to_dict(self):
        """
        Convert candle to dictionary.
        """

        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "time": self.time,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume,
        }

    def __str__(self):

        return (
            f"{self.symbol} "
            f"{self.timeframe} "
            f"{self.time} "
            f"O:{self.open} "
            f"H:{self.high} "
            f"L:{self.low} "
            f"C:{self.close}"
        )