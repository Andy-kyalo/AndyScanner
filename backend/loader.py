"""
loader.py

Loads market data from CSV files.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import csv

from backend.candle import Candle


class Loader:

    # ==========================================
    # Constructor
    # ==========================================

    def __init__(self, filename):
        self.filename = filename

    # ==========================================
    # Load Candles
    # ==========================================

    def load(self):

        candles = []

        with open(self.filename, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                candle = Candle(
                    time=row["time"],
                    open_price=float(row["open"]),
                    high=float(row["high"]),
                    low=float(row["low"]),
                    close=float(row["close"])
                )

                candles.append(candle)

        return candles
