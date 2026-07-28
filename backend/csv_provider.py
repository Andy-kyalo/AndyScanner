"""
csv_provider.py

CSV market data provider.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import csv
from pathlib import Path

from backend.candle import Candle
from backend.data_provider import DataProvider


class CSVProvider(DataProvider):
    """
    Loads market data from a CSV file.
    """

    REQUIRED_COLUMNS = (
        "time",
        "open",
        "high",
        "low",
        "close",
    )

    def __init__(self, filename):
        self.filename = Path(filename)

    def load(self):
        """
        Load candles from a CSV file.

        Returns
        -------
        list[Candle]
        """

        if not self.filename.exists():
            raise FileNotFoundError(
                f"CSV file not found: {self.filename}"
            )

        candles = []

        with self.filename.open(
            mode="r",
            newline="",
            encoding="utf-8",
        ) as file:

            reader = csv.DictReader(file)

            if reader.fieldnames is None:
                raise ValueError(
                    "CSV file is empty."
                )

            missing = [
                column
                for column in self.REQUIRED_COLUMNS
                if column not in reader.fieldnames
            ]

            if missing:
                raise ValueError(
                    f"Missing CSV columns: {', '.join(missing)}"
                )

            for line_number, row in enumerate(reader, start=2):

                try:

                    candle = Candle(
                        time=row["time"].strip(),
                        open_price=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                    )

                    candles.append(candle)

                except Exception as error:
                    raise ValueError(
                        f"Invalid data on line "
                        f"{line_number}: {error}"
                    ) from error

        if not candles:
            raise ValueError(
                "No candle data found in CSV."
            )

        return candles