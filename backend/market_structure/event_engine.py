"""
event_engine.py

Structural event engine.

Detects:

    STRUCTURE_BREAK
    BOS
    CHOCH

Rules:

    First directional break
        -> STRUCTURE_BREAK

    Same direction as established structure
        -> BOS

    Opposite direction
        -> CHOCH

Break confirmation requires candle CLOSE
to move strictly beyond the structural level.

Wicks do not confirm structural breaks.
Exact-level closes do not confirm structural breaks.
"""

from typing import List

from backend.candle import Candle

from .models import (
    StructureEvent,
    StructurePoint,
    STRUCTURE_BULLISH,
    STRUCTURE_BEARISH,
    STRUCTURE_UNDEFINED,
    EVENT_STRUCTURE_BREAK,
    EVENT_BOS,
    EVENT_CHOCH,
)


class StructureEventEngine:
    """
    Calculates chronological structural events.
    """

    def __init__(
        self,
        candles: List[Candle],
        highs: List[StructurePoint],
        lows: List[StructurePoint],
        swing_strength: int,
    ):
        self.candles = list(candles)
        self.highs = list(highs)
        self.lows = list(lows)
        self.swing_strength = swing_strength

        self._events = None

    # ========================================================
    # EVENTS
    # ========================================================

    def calculate(self) -> List[StructureEvent]:
        """
        Calculate structural events exactly once.
        """

        if self._events is not None:
            return list(self._events)

        structural_points = [
            *self.highs,
            *self.lows,
        ]

        if not structural_points:
            self._events = []
            return []

        structural_points.sort(
            key=lambda point: point.index
        )

        events = []

        active_high = None
        active_low = None

        established_direction = STRUCTURE_UNDEFINED

        broken_high_indices = set()
        broken_low_indices = set()

        point_cursor = 0

        for candle_index, candle in enumerate(
            self.candles
        ):

            # ------------------------------------------------
            # Activate confirmed swings.
            # ------------------------------------------------

            while (
                point_cursor < len(structural_points)
                and (
                    structural_points[
                        point_cursor
                    ].index
                    + self.swing_strength
                    <= candle_index
                )
            ):
                point = structural_points[
                    point_cursor
                ]

                if point.kind == "HIGH":
                    active_high = point
                else:
                    active_low = point

                point_cursor += 1

            # ------------------------------------------------
            # Bullish break
            # ------------------------------------------------

            bullish_break = (
                active_high is not None
                and candle_index > active_high.index
                and candle.close > active_high.price
                and active_high.index
                not in broken_high_indices
            )

            if bullish_break:

                event_type = self._classify_event(
                    established_direction,
                    STRUCTURE_BULLISH,
                )

                events.append(
                    StructureEvent(
                        event=event_type,
                        direction="BULLISH",
                        index=candle_index,
                        time=candle.time,
                        level=active_high.price,
                    )
                )

                broken_high_indices.add(
                    active_high.index
                )

                established_direction = (
                    STRUCTURE_BULLISH
                )

            # ------------------------------------------------
            # Bearish break
            # ------------------------------------------------

            bearish_break = (
                active_low is not None
                and candle_index > active_low.index
                and candle.close < active_low.price
                and active_low.index
                not in broken_low_indices
            )

            if bearish_break:

                event_type = self._classify_event(
                    established_direction,
                    STRUCTURE_BEARISH,
                )

                events.append(
                    StructureEvent(
                        event=event_type,
                        direction="BEARISH",
                        index=candle_index,
                        time=candle.time,
                        level=active_low.price,
                    )
                )

                broken_low_indices.add(
                    active_low.index
                )

                established_direction = (
                    STRUCTURE_BEARISH
                )

        self._events = sorted(
            events,
            key=lambda event: event.index,
        )

        return list(self._events)

    # ========================================================
    # CLASSIFICATION
    # ========================================================

    @staticmethod
    def _classify_event(
        established_direction: str,
        new_direction: str,
    ) -> str:

        if established_direction == (
            STRUCTURE_UNDEFINED
        ):
            return EVENT_STRUCTURE_BREAK

        if established_direction == new_direction:
            return EVENT_BOS

        return EVENT_CHOCH

    # ========================================================
    # ACCESSORS
    # ========================================================

    def current_event(self):
        events = self.calculate()

        if not events:
            return None

        return events[-1]

    def last_bos(self):
        for event in reversed(
            self.calculate()
        ):
            if event.event == EVENT_BOS:
                return event

        return None

    def last_choch(self):
        for event in reversed(
            self.calculate()
        ):
            if event.event == EVENT_CHOCH:
                return event

        return None

    def last_structure_break(self):
        for event in reversed(
            self.calculate()
        ):
            if event.event == EVENT_STRUCTURE_BREAK:
                return event

        return None
