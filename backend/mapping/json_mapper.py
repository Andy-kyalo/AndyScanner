"""
json_mapper.py

JSON market data mapper.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.mapping.base_mapper import BaseMapper
from backend.candle import Candle


class JSONMapper(BaseMapper):
    """
    Converts JSON market data into Candle objects.
    """

    def map(self, raw_data):
        """
        Convert JSON records into Candle objects.

        Expected format:

        [
            {
                "time": "...",
                "open": ...,
                "high": ...,
                "low": ...,
                "close": ...
            }
        ]
        """

        self.validate(raw_data)

        candles = []

        for item in raw_data:

            candles.append(
                Candle(
                    time=item["time"],
                    open=float(item["open"]),
                    high=float(item["high"]),
                    low=float(item["low"]),
                    close=float(item["close"]),
                )
            )

        return candles