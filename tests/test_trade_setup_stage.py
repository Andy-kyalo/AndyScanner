import unittest

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
from backend.signal import Signal


class TestTradeSetupStage(unittest.TestCase):

    def create_context(self):

        context = PipelineContext()

        context.start(
            "US30",
            "M5",
        )

        context.signal = Signal(
            market="US30",
            timeframe="M5",
            direction="BUY",
            confidence=80,
        )

        return context

    def test_trade_setup_stage_returns_context(self):

        context = self.create_context()

        result = TradeSetupStage().run(context)

        self.assertIs(
            result,
            context,
        )

    def test_trade_setup_is_created(self):

        context = self.create_context()

        TradeSetupStage().run(context)

        self.assertIsNotNone(
            context.trade_setup,
        )

    def test_trade_setup_contains_market(self):

        context = self.create_context()

        TradeSetupStage().run(context)

        self.assertEqual(
            context.trade_setup.market,
            "US30",
        )

    def test_trade_setup_contains_timeframe(self):

        context = self.create_context()

        TradeSetupStage().run(context)

        self.assertEqual(
            context.trade_setup.timeframe,
            "M5",
        )

    def test_trade_setup_contains_direction(self):

        context = self.create_context()

        TradeSetupStage().run(context)

        self.assertEqual(
            context.trade_setup.direction,
            "BUY",
        )


if __name__ == "__main__":
    unittest.main()
