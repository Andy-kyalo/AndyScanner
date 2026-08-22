"""
swing_detector.py

Confirmed swing-high and swing-low detection.

Design:
    - no look-ahead beyond configured confirmation strength
    - strict inequality
    - equal highs/lows are not structural pivots
"""

from typing import List

from backend.candle import Candle

from .models import StructurePoint


class SwingDetector:
    """
    Detects confirmed raw swing points.

    A swing requires `strength` candles on both sides.
    """

    def __init__(
        self,
        candles: List[Candle],
        strength: int = 1,
    ):
        if not candles:
            raise ValueError(
                "SwingDetector requires candles."
            )

        if strength < 1:
            raise ValueError(
                "strength must be at least 1."
            )

        minimum = (strength * 2) + 1

        if len(candles) < minimum:
            raise ValueError(
                f"At least {minimum} candles are required "
                f"for swing strength={strength}."
            )

        self.candles = list(candles)
        self.strength = strength

        self._highs = None
        self._lows = None

    # ========================================================
    # SWING HIGHS
    # ========================================================

    def swing_highs(self) -> List[StructurePoint]:
        """
        Return confirmed raw swing highs.
        """

        if self._highs is not None:
            return list(self._highs)

        points = []
        strength = self.strength

        for i in range(
            strength,
            len(self.candles) - strength,
        ):
            current = self.candles[i]

            left = self.candles[
                i - strength:i
            ]

            right = self.candles[
                i + 1:i + strength + 1
            ]

            if all(
                current.high > candle.high
                for candle in left + right
            ):
                points.append(
                    StructurePoint(
                        index=i,
                        time=current.time,
                        price=current.high,
                        kind="HIGH",
                    )
                )

        self._highs = list(points)

        return list(self._highs)

    # ========================================================
    # SWING LOWS
    # ========================================================

    def swing_lows(self) -> List[StructurePoint]:
        """
        Return confirmed raw swing lows.
        """

        if self._lows is not None:
            return list(self._lows)

        points = []
        strength = self.strength

        for i in range(
            strength,
            len(self.candles) - strength,
        ):
            current = self.candles[i]

            left = self.candles[
                i - strength:i
            ]

            right = self.candles[
                i + 1:i + strength + 1
            ]

            if all(
                current.low < candle.low
                for candle in left + right
            ):
                points.append(
                    StructurePoint(
                        index=i,
                        time=current.time,
                        price=current.low,
                        kind="LOW",
                    )
                )

        self._lows = list(points)

        return list(self._lows)
