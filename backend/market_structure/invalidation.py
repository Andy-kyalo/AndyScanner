"""
invalidation.py

Structural invalidation logic.

A bullish structure is invalidated when price CLOSES strictly
below its protected low.

A bearish structure is invalidated when price CLOSES strictly
above its protected high.

Wicks do not invalidate structure.
Exact-level closes do not invalidate structure.

The protected level must belong to the structure that existed
before the invalidating candle.
"""

from typing import List, Optional

from backend.candle import Candle

from .models import (
    StructureEvent,
    StructurePoint,
    STRUCTURE_BULLISH,
    STRUCTURE_BEARISH,
    EVENT_STRUCTURE_INVALIDATION,
)


class StructureInvalidationEngine:
    """
    Detects confirmed structural invalidation.

    This engine evaluates the protected level against the
    structural state supplied to it. It does not derive a new
    state from the candles.
    """

    def __init__(
        self,
        candles: List[Candle],
        state: str,
        protected_high: Optional[StructurePoint],
        protected_low: Optional[StructurePoint],
    ):
        self.candles = list(candles)
        self.state = state
        self.protected_high = protected_high
        self.protected_low = protected_low

    # ========================================================
    # LATEST INVALIDATION
    # ========================================================

    def latest(self) -> Optional[StructureEvent]:
        """
        Return the first confirmed invalidation of the supplied
        structural state.

        Bullish:
            close < protected_low

        Bearish:
            close > protected_high
        """

        # ----------------------------------------------------
        # BULLISH STRUCTURE
        # ----------------------------------------------------

        if self.state == STRUCTURE_BULLISH:

            if self.protected_low is None:
                return None

            level = self.protected_low

            for index in range(
                level.index + 1,
                len(self.candles),
            ):
                candle = self.candles[index]

                # Strict close-through only.
                if candle.close < level.price:
                    return StructureEvent(
                        event=EVENT_STRUCTURE_INVALIDATION,
                        direction="BEARISH",
                        index=index,
                        time=candle.time,
                        level=level.price,
                    )

            return None

        # ----------------------------------------------------
        # BEARISH STRUCTURE
        # ----------------------------------------------------

        if self.state == STRUCTURE_BEARISH:

            if self.protected_high is None:
                return None

            level = self.protected_high

            for index in range(
                level.index + 1,
                len(self.candles),
            ):
                candle = self.candles[index]

                # Strict close-through only.
                if candle.close > level.price:
                    return StructureEvent(
                        event=EVENT_STRUCTURE_INVALIDATION,
                        direction="BULLISH",
                        index=index,
                        time=candle.time,
                        level=level.price,
                    )

            return None

        return None