"""
models.py

Core immutable market-structure data models.

Andy Scanner
"""

from dataclasses import dataclass


# ============================================================
# STRUCTURAL STATE
# ============================================================

STRUCTURE_BULLISH = "BULLISH"
STRUCTURE_BEARISH = "BEARISH"
STRUCTURE_UNDEFINED = "UNDEFINED"


# ============================================================
# EVENT TYPES
# ============================================================

EVENT_STRUCTURE_BREAK = "STRUCTURE_BREAK"
EVENT_BOS = "BOS"
EVENT_CHOCH = "CHOCH"
EVENT_STRUCTURE_INVALIDATION = "STRUCTURE_INVALIDATION"


# ============================================================
# STRUCTURE POINT
# ============================================================

@dataclass(frozen=True)
class StructurePoint:
    """
    Confirmed structural swing point.
    """

    index: int
    time: str
    price: float
    kind: str
    label: str = "INITIAL"


# ============================================================
# STRUCTURE EVENT
# ============================================================

@dataclass(frozen=True)
class StructureEvent:
    """
    Confirmed structural event.

    event:
        STRUCTURE_BREAK
        BOS
        CHOCH
        STRUCTURE_INVALIDATION

    direction:
        BULLISH
        BEARISH

    index:
        Candle index that confirmed the event.

    time:
        Candle timestamp.

    level:
        Structural price that was broken.
    """

    event: str
    direction: str
    index: int
    time: str
    level: float
