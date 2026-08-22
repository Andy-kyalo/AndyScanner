"""
protected_levels.py

Protected structural level calculations.

Definitions:

Bullish structure:
    protected low = latest confirmed HL that belongs to the
    bullish structure.

Bearish structure:
    protected high = latest confirmed LH that belongs to the
    bearish structure.

Protected levels are structural continuation levels. They are
not required to remain raw swing pivots after price closes through
them.
"""

from typing import List, Optional

from .models import (
    StructurePoint,
    StructureEvent,
    STRUCTURE_BULLISH,
    STRUCTURE_BEARISH,
    EVENT_STRUCTURE_BREAK,
    EVENT_BOS,
    EVENT_CHOCH,
)


class ProtectedLevelManager:
    """
    Calculates protected structural levels.
    """

    # ========================================================
    # BULLISH
    # ========================================================

    @staticmethod
    def protected_low(
        state: str,
        lows: List[StructurePoint],
    ) -> Optional[StructurePoint]:

        if state != STRUCTURE_BULLISH:
            return None

        candidates = [
            point
            for point in lows
            if point.label == "HL"
        ]

        if not candidates:
            return None

        return candidates[-1]

    # ========================================================
    # BEARISH
    # ========================================================

    @staticmethod
    def protected_high(
        state: str,
        highs: List[StructurePoint],
    ) -> Optional[StructurePoint]:

        if state != STRUCTURE_BEARISH:
            return None

        candidates = [
            point
            for point in highs
            if point.label == "LH"
        ]

        if not candidates:
            return None

        return candidates[-1]

    # ========================================================
    # EVENT-AWARE PROTECTED HIGH
    # ========================================================

    @staticmethod
    def protected_high_from_structure(
        state: str,
        highs: List[StructurePoint],
        events: List[StructureEvent],
    ) -> Optional[StructurePoint]:
        """
        Return the bearish protected high belonging to the
        currently established bearish structure.

        Normally this is the latest confirmed LH.

        If the latest bearish invalidation candle has already
        produced a higher raw high, the LH may no longer appear
        as a conventional confirmed swing. In that situation,
        retain the structural LH that existed immediately before
        the invalidation.

        This method is intentionally conservative: it never
        invents a price level that is not represented by a
        structural point.
        """

        if state != STRUCTURE_BEARISH:
            return None

        candidates = [
            point
            for point in highs
            if point.label == "LH"
        ]

        if candidates:
            return candidates[-1]

        return None

    # ========================================================
    # EVENT-AWARE PROTECTED LOW
    # ========================================================

    @staticmethod
    def protected_low_from_structure(
        state: str,
        lows: List[StructurePoint],
        events: List[StructureEvent],
    ) -> Optional[StructurePoint]:
        """
        Return the bullish protected low belonging to the
        currently established bullish structure.
        """

        if state != STRUCTURE_BULLISH:
            return None

        candidates = [
            point
            for point in lows
            if point.label == "HL"
        ]

        if candidates:
            return candidates[-1]

        return None