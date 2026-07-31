"""
mt5_mapper.py

MetaTrader 5 market data mapper.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.mapping.base_mapper import BaseMapper
from backend.models.candle import Candle


class MT5Mapper(BaseMapper):
    """
    Converts MetaTrader 5 rates into
    Andy Scanner Candle objects.
    """

    def map(self, raw_data):
        """
        Convert MT5 rates into Candle objects.

        Expected MT5 rate structure:

        {
            "time": ...,
            "open": ...,
            "high": ...,
            "low": ...,
            "close": ...
        }
        """

        self.validate(raw_data)

        candles = []

        for rate in raw_data:

            candle = Candle(
                time=rate["time"],
                open=float(rate["open"]),
                high=float(rate["high"]),
                low=float(rate["low"]),
                close=float(rate["close"]),
            )

            candles.append(candle)

        return candles