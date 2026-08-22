"""
market_structure_engine.py

Compatibility facade for Andy Scanner.

The implementation lives inside:

    backend.market_structure

This module preserves the original public import:

    from backend.market_structure_engine import MarketStructureEngine
"""

from backend.market_structure.engine import MarketStructureEngine
from backend.market_structure.models import (
    StructurePoint,
    StructureEvent,
    STRUCTURE_BULLISH,
    STRUCTURE_BEARISH,
    STRUCTURE_UNDEFINED,
    EVENT_STRUCTURE_BREAK,
    EVENT_BOS,
    EVENT_CHOCH,
    EVENT_STRUCTURE_INVALIDATION,
)


__all__ = [
    "MarketStructureEngine",
    "StructurePoint",
    "StructureEvent",
    "STRUCTURE_BULLISH",
    "STRUCTURE_BEARISH",
    "STRUCTURE_UNDEFINED",
    "EVENT_STRUCTURE_BREAK",
    "EVENT_BOS",
    "EVENT_CHOCH",
    "EVENT_STRUCTURE_INVALIDATION",
]