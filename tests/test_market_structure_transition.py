import unittest

from backend.candle import Candle
from backend.market_structure_engine import MarketStructureEngine


class TestMarketStructureTransition(unittest.TestCase):

    def test_bullish_choch_can_coexist_with_swing_based_downtrend(self):
        candles = [
            Candle("2026-04-07 00:00:00", 100, 101, 99, 100),
            Candle("2026-04-07 00:05:00", 100, 106, 99, 104),
            Candle("2026-04-07 00:10:00", 104, 105, 97, 99),
            Candle("2026-04-07 00:15:00", 99, 102, 98, 101),
            Candle("2026-04-07 00:20:00", 101, 102, 95, 96),
            Candle("2026-04-07 00:25:00", 96, 101, 95, 100),
            Candle("2026-04-07 00:30:00", 100, 103, 98, 99),
            Candle("2026-04-07 00:35:00", 99, 101, 97, 100),
            Candle("2026-04-07 00:40:00", 100, 106, 99, 104),
        ]

        engine = MarketStructureEngine(
            candles,
            swing_strength=1,
        )

        self.assertEqual(engine.trend(), "DOWNTREND")
        self.assertEqual(engine.structural_state(), "BULLISH")

        event = engine.current_event()

        self.assertIsNotNone(event)
        self.assertEqual(event.event, "CHOCH")
        self.assertEqual(event.direction, "BULLISH")
        self.assertEqual(event.index, 8)
        self.assertEqual(event.level, 103)


if __name__ == "__main__":
    unittest.main()
