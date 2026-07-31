"""
csv_mapper.py

CSV market data mapper.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.mapping.base_mapper import BaseMapper
from backend.models.candle import Candle


class CSVMapper(BaseMapper):
    """
    Converts CSV rows into Candle objects.
    """

    def map(self, raw_data):
        """
        Convert CSV records into Candle objects.

        Expected CSV row format:

        {
            "time": "...",
            "open": ...,
            "high": ...,
            "low": ...,
            "close": ...
        }
        """

        self.validate(raw_data)

        candles = []

        for row in raw_data:

            candle = Candle(
                time=row["time"],
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
            )

            candles.append(candle)

        return candles