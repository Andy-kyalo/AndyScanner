"""
loader.py

Loads and validates market data from CSV files.

Author: Andrew Kyalo
Project: Andy Scanner
"""

import csv
import os

from backend.candle import Candle


class Loader:
    """
    Loads candle data from a CSV file.
    """

    REQUIRED_COLUMNS = (
        "time",
        "open",
        "high",
        "low",
        "close",
    )

    # ==========================================================
    # Constructor
    # ==========================================================

    def __init__(self, filename):
        self.filename = filename

    # ==========================================================
    # Load Candles
    # ==========================================================

    def load(self):
        """
        Load and validate candle data.

        Returns:
            list[Candle]
        """

        if not os.path.exists(self.filename):
            raise FileNotFoundError(
                f"CSV file not found: {self.filename}"
            )

        candles = []

        with open(
            self.filename,
            "r",
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
                    f"Missing required CSV columns: {', '.join(missing)}"
                )

            for line_number, row in enumerate(reader, start=2):

                if not any(row.values()):
                    continue

                try:
                    candle = Candle(
                        time=row["time"].strip(),
                        open_price=float(row["open"]),
                        high=float(row["high"]),
                        low=float(row["low"]),
                        close=float(row["close"]),
                    )

                except ValueError as error:
                    raise ValueError(
                        f"Invalid data on line {line_number}: {error}"
                    ) from error

                candles.append(candle)

        if not candles:
            raise ValueError(
                "No candle data found in the CSV file."
            )

        return candles
        return candles
