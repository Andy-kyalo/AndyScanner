"""
engine.py

High-level market-structure facade.

This class coordinates:

    SwingDetector
    SwingClassifier
    StructureEventEngine
    ProtectedLevelManager
    StructureInvalidationEngine

The public API intentionally mirrors the previous
MarketStructureEngine.
"""

from typing import List, Optional

from backend.candle import Candle

from .models import (
    StructurePoint,
    StructureEvent,
    STRUCTURE_BULLISH,
    STRUCTURE_BEARISH,
    STRUCTURE_UNDEFINED,
    EVENT_BOS,
    EVENT_CHOCH,
    EVENT_STRUCTURE_BREAK,
    EVENT_STRUCTURE_INVALIDATION,
)

from .swing_detector import SwingDetector
from .swing_classifier import SwingClassifier
from .event_engine import StructureEventEngine
from .protected_levels import ProtectedLevelManager
from .invalidation import StructureInvalidationEngine


class MarketStructureEngine:
    """
    Authoritative market-structure engine.
    """

    def __init__(
        self,
        candles: List[Candle],
        swing_strength: int = 1,
    ):
        if not candles:
            raise ValueError(
                "MarketStructureEngine requires candles."
            )

        if swing_strength < 1:
            raise ValueError(
                "swing_strength must be at least 1."
            )

        minimum = (
            swing_strength * 2
        ) + 1

        if len(candles) < minimum:
            raise ValueError(
                f"At least {minimum} candles are required "
                f"for swing_strength={swing_strength}."
            )

        self.candles = list(candles)
        self.swing_strength = swing_strength

        self._detector = SwingDetector(
            self.candles,
            swing_strength,
        )

        self._highs = None
        self._lows = None
        self._events = None

    # ========================================================
    # SWINGS
    # ========================================================

    def swing_highs(self) -> List[StructurePoint]:
        if self._highs is None:
            raw = self._detector.swing_highs()

            self._highs = (
                SwingClassifier.classify_highs(raw)
            )

        return list(self._highs)

    def swing_lows(self) -> List[StructurePoint]:
        if self._lows is None:
            raw = self._detector.swing_lows()

            self._lows = (
                SwingClassifier.classify_lows(raw)
            )

        return list(self._lows)

    # ========================================================
    # LATEST SWINGS
    # ========================================================

    def latest_swing_high(
        self,
    ) -> Optional[StructurePoint]:

        highs = self.swing_highs()

        return highs[-1] if highs else None

    def latest_swing_low(
        self,
    ) -> Optional[StructurePoint]:

        lows = self.swing_lows()

        return lows[-1] if lows else None

    # ========================================================
    # SWING COUNTS
    # ========================================================

    def swing_high_count(self) -> int:
        return len(self.swing_highs())

    def swing_low_count(self) -> int:
        return len(self.swing_lows())

    # ========================================================
    # EVENTS
    # ========================================================

    def _event_engine(self):
        return StructureEventEngine(
            candles=self.candles,
            highs=self.swing_highs(),
            lows=self.swing_lows(),
            swing_strength=self.swing_strength,
        )

    def _calculate_events(
        self,
    ) -> List[StructureEvent]:

        if self._events is None:
            self._events = (
                self._event_engine().calculate()
            )

        return list(self._events)

    def events(self) -> List[StructureEvent]:
        return list(
            self._calculate_events()
        )

    def current_event(
        self,
    ) -> Optional[StructureEvent]:

        events = self._calculate_events()

        if not events:
            return None

        return events[-1]

    # ========================================================
    # STRUCTURAL STATE
    # ========================================================

    def structural_state(self) -> str:
        """
        Determine current structural state.

        Event-driven once a structural event exists.

        Otherwise use HH/HL or LH/LL.
        """

        event = self.current_event()

        if event is not None:

            if event.direction == "BULLISH":
                return STRUCTURE_BULLISH

            if event.direction == "BEARISH":
                return STRUCTURE_BEARISH

        highs = self.swing_highs()
        lows = self.swing_lows()

        if len(highs) >= 2 and len(lows) >= 2:

            latest_high = highs[-1]
            latest_low = lows[-1]

            if (
                latest_high.label == "HH"
                and latest_low.label == "HL"
            ):
                return STRUCTURE_BULLISH

            if (
                latest_high.label == "LH"
                and latest_low.label == "LL"
            ):
                return STRUCTURE_BEARISH

        return STRUCTURE_UNDEFINED

    # ========================================================
    # STRUCTURE
    # ========================================================

    def structure(self) -> str:

        state = self.structural_state()

        if state == STRUCTURE_BULLISH:
            return "BULLISH_STRUCTURE"

        if state == STRUCTURE_BEARISH:
            return "BEARISH_STRUCTURE"

        return "NO_STRUCTURE"

    # ========================================================
    # TREND
    # ========================================================

    def trend(self) -> str:
        """
        Determine swing-based trend.

        HH + HL -> UPTREND
        LH + LL -> DOWNTREND
        otherwise SIDEWAYS
        """

        highs = self.swing_highs()
        lows = self.swing_lows()

        if len(highs) < 2 or len(lows) < 2:
            return "SIDEWAYS"

        latest_high = highs[-1]
        latest_low = lows[-1]

        if (
            latest_high.label == "HH"
            and latest_low.label == "HL"
        ):
            return "UPTREND"

        if (
            latest_high.label == "LH"
            and latest_low.label == "LL"
        ):
            return "DOWNTREND"

        return "SIDEWAYS"

    # ========================================================
    # PROTECTED LEVELS
    # ========================================================

    def protected_high(
        self,
    ) -> Optional[StructurePoint]:

        return (
            ProtectedLevelManager.protected_high(
                self.structural_state(),
                self.swing_highs(),
            )
        )

    def protected_low(
        self,
    ) -> Optional[StructurePoint]:

        return (
            ProtectedLevelManager.protected_low(
                self.structural_state(),
                self.swing_lows(),
            )
        )

    # ========================================================
    # BOS
    # ========================================================

    def bullish_bos(self) -> bool:

        event = self.current_event()

        if event is None:
            return False

        return (
            event.event == EVENT_BOS
            and event.direction == "BULLISH"
        )

    def bearish_bos(self) -> bool:

        event = self.current_event()

        if event is None:
            return False

        return (
            event.event == EVENT_BOS
            and event.direction == "BEARISH"
        )

    def last_bos(
        self,
    ) -> Optional[StructureEvent]:

        for event in reversed(
            self._calculate_events()
        ):
            if event.event == EVENT_BOS:
                return event

        return None

    # ========================================================
    # CHOCH
    # ========================================================

    def bullish_choch(self) -> bool:

        event = self.current_event()

        if event is None:
            return False

        return (
            event.event == EVENT_CHOCH
            and event.direction == "BULLISH"
        )

    def bearish_choch(self) -> bool:

        event = self.current_event()

        if event is None:
            return False

        return (
            event.event == EVENT_CHOCH
            and event.direction == "BEARISH"
        )

    def last_choch(
        self,
    ) -> Optional[StructureEvent]:

        for event in reversed(
            self._calculate_events()
        ):
            if event.event == EVENT_CHOCH:
                return event

        return None

    # ========================================================
    # STRUCTURE BREAK
    # ========================================================

    def last_structure_break(
        self,
    ) -> Optional[StructureEvent]:

        for event in reversed(
            self._calculate_events()
        ):
            if event.event == EVENT_STRUCTURE_BREAK:
                return event

        return None

    # ========================================================
    # INVALIDATION
    # ========================================================

    def _invalidation_event(
        self,
    ) -> Optional[StructureEvent]:
        """
        Detect structural invalidation chronologically.

        The protected level must exist before the candle that
        invalidates the structure.
        """

        events = self._calculate_events()

        if not events:
            return None

        # --------------------------------------------------------
        # Examine each structural event chronologically.
        # --------------------------------------------------------

        for event in events:

            # ----------------------------------------------------
            # Bearish event against previously bullish structure.
            # ----------------------------------------------------

            if (
                event.direction == "BEARISH"
                and event.event == EVENT_CHOCH
            ):
                bullish_levels = [
                    point
                    for point in self.swing_lows()
                    if (
                        point.label == "HL"
                        and point.index < event.index
                    )
                ]

                if not bullish_levels:
                    continue

                protected_low = bullish_levels[-1]

                manager = StructureInvalidationEngine(
                    candles=self.candles[
                        : event.index + 1
                    ],
                    state=STRUCTURE_BULLISH,
                    protected_high=None,
                    protected_low=protected_low,
                )

                invalidation = manager.latest()

                if invalidation is not None:
                    return invalidation

            # ----------------------------------------------------
            # Bullish event against previously bearish structure.
            # ----------------------------------------------------

            if (
                event.direction == "BULLISH"
                and event.event == EVENT_CHOCH
            ):
                bearish_levels = [
                    point
                    for point in self.swing_highs()
                    if (
                        point.label == "LH"
                        and point.index < event.index
                    )
                ]

                if not bearish_levels:
                    continue

                protected_high = bearish_levels[-1]

                manager = StructureInvalidationEngine(
                    candles=self.candles[
                        : event.index + 1
                    ],
                    state=STRUCTURE_BEARISH,
                    protected_high=protected_high,
                    protected_low=None,
                )

                invalidation = manager.latest()

                if invalidation is not None:
                    return invalidation

        return None

    def bullish_invalidation(self) -> bool:

        event = self._invalidation_event()

        if event is None:
            return False

        return (
            event.event
            == EVENT_STRUCTURE_INVALIDATION
            and event.direction == "BULLISH"
        )

    def bearish_invalidation(self) -> bool:

        event = self._invalidation_event()

        if event is None:
            return False

        return (
            event.event
            == EVENT_STRUCTURE_INVALIDATION
            and event.direction == "BEARISH"
        )

    def last_invalidation(
        self,
    ) -> Optional[StructureEvent]:

        return self._invalidation_event()

    # ========================================================
    # SERIALIZATION
    # ========================================================

    @staticmethod
    def _point_to_dict(
        point: Optional[StructurePoint],
    ):

        if point is None:
            return None

        return {
            "index": point.index,
            "time": point.time,
            "price": point.price,
            "kind": point.kind,
            "label": point.label,
        }

    @staticmethod
    def _event_to_dict(
        event: Optional[StructureEvent],
    ):

        if event is None:
            return None

        return {
            "event": event.event,
            "direction": event.direction,
            "index": event.index,
            "time": event.time,
            "level": event.level,
        }

    def snapshot(self) -> dict:
        """
        Return one authoritative serializable snapshot.
        """

        current_event = self.current_event()

        latest_high = (
            self.latest_swing_high()
        )

        latest_low = (
            self.latest_swing_low()
        )

        protected_high = (
            self.protected_high()
        )

        protected_low = (
            self.protected_low()
        )

        last_structure_break = (
            self.last_structure_break()
        )

        last_bos = self.last_bos()
        last_choch = self.last_choch()
        last_invalidation = (
            self.last_invalidation()
        )

        return {
            "trend": self.trend(),

            "structural_state":
                self.structural_state(),

            "structure":
                self.structure(),

            "current_event":
                self._event_to_dict(
                    current_event
                ),

            "bullish_bos":
                self.bullish_bos(),

            "bearish_bos":
                self.bearish_bos(),

            "bullish_choch":
                self.bullish_choch(),

            "bearish_choch":
                self.bearish_choch(),

            "bullish_invalidation":
                self.bullish_invalidation(),

            "bearish_invalidation":
                self.bearish_invalidation(),

            "swing_high_count":
                self.swing_high_count(),

            "swing_low_count":
                self.swing_low_count(),

            "latest_high":
                self._point_to_dict(
                    latest_high
                ),

            "latest_low":
                self._point_to_dict(
                    latest_low
                ),

            "protected_high":
                self._point_to_dict(
                    protected_high
                ),

            "protected_low":
                self._point_to_dict(
                    protected_low
                ),

            "last_structure_break":
                self._event_to_dict(
                    last_structure_break
                ),

            "last_bos":
                self._event_to_dict(
                    last_bos
                ),

            "last_choch":
                self._event_to_dict(
                    last_choch
                ),

            "last_invalidation":
                self._event_to_dict(
                    last_invalidation
                ),

            "event_count": len(self._calculate_events()),
        }