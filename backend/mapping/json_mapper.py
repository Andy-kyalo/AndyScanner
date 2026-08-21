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

    Supports the canonical AndyScanner JSON format:

        {
            "time": "...",
            "open": ...,
            "high": ...,
            "low": ...,
            "close": ...
        }

    Also supports provider-specific datetime fields such as
    Twelve Data's:

        {
            "datetime": "...",
            "open": ...,
            "high": ...,
            "low": ...,
            "close": ...
        }
    """

    def map(self, raw_data):
        """
        Convert JSON records into Candle objects.

        Accepted time fields:
            - time
            - datetime

        Price fields:
            - open
            - high
            - low
            - close

        Returns:
            list[Candle]
        """

        self.validate(raw_data)

        candles = []

        for item in raw_data:

            if not isinstance(item, dict):
                raise TypeError(
                    "JSON candle record must be a dictionary."
                )

            # --------------------------------------------------
            # Time
            # --------------------------------------------------

            time = item.get("time")

            if time is None:
                time = item.get("datetime")

            if time is None:
                raise KeyError(
                    "JSON candle record contains neither "
                    "'time' nor 'datetime'."
                )

            # --------------------------------------------------
            # OHLC
            # --------------------------------------------------

            candles.append(
                Candle(
                    time=time,
                    open_price=float(item["open"]),
                    high=float(item["high"]),
                    low=float(item["low"]),
                    close=float(item["close"]),
                )
            )

        return candles