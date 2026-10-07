import unittest

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
from backend.signal import Signal
from backend.analysis_result import AnalysisResult


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

        context.analysis = AnalysisResult()
        context.analysis.market = "US30"
        context.analysis.timeframe = "M5"

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


    def test_buy_uses_bullish_confirmation_high_and_protected_low(self):

        from backend.candle import Candle
        from backend.market_structure.models import StructurePoint

        context = self.create_context()

        confirmation = Candle(
            "10:30",
            104,
            110,
            103,
            109,
        )

        protected_low = StructurePoint(
            index=5,
            time="10:25",
            price=102,
            kind="LOW",
            label="HL",
        )

        context.analysis.bullish_confirmation_candle = confirmation
        context.analysis.protected_low = protected_low

        TradeSetupStage().run(context)

        self.assertEqual(
            context.trade_setup.entry,
            110,
        )

        self.assertEqual(
            context.trade_setup.stop_loss,
            102,
        )


    def test_sell_uses_bearish_confirmation_low_and_protected_high(self):

        from backend.candle import Candle
        from backend.market_structure.models import StructurePoint

        context = self.create_context()

        context.signal = Signal(
            market="US30",
            timeframe="M5",
            direction="SELL",
            confidence=80,
        )

        confirmation = Candle(
            "10:30",
            106,
            108,
            100,
            101,
        )

        protected_high = StructurePoint(
            index=5,
            time="10:25",
            price=110,
            kind="HIGH",
            label="LH",
        )

        context.analysis.bearish_confirmation_candle = confirmation
        context.analysis.protected_high = protected_high

        TradeSetupStage().run(context)

        self.assertEqual(
            context.trade_setup.entry,
            100,
        )

        self.assertEqual(
            context.trade_setup.stop_loss,
            110,
        )


    def test_buy_without_confirmation_candle_is_invalid(self):

        context = self.create_context()

        from backend.market_structure.models import StructurePoint

        context.analysis.protected_low = StructurePoint(
            index=5,
            time="10:25",
            price=102,
            kind="LOW",
            label="HL",
        )

        TradeSetupStage().run(context)

        self.assertFalse(
            context.trade_setup.valid,
        )

        self.assertIsNone(
            context.trade_setup.entry,
        )


    def test_buy_without_protected_low_is_invalid(self):

        from backend.candle import Candle

        context = self.create_context()

        context.analysis.bullish_confirmation_candle = Candle(
            "10:30",
            104,
            110,
            103,
            109,
        )

        TradeSetupStage().run(context)

        self.assertFalse(
            context.trade_setup.valid,
        )

        self.assertEqual(
            context.trade_setup.entry,
            110,
        )

        self.assertIsNone(
            context.trade_setup.stop_loss,
        )


    def test_sell_without_protected_high_is_invalid(self):

        from backend.candle import Candle

        context = self.create_context()

        context.signal = Signal(
            market="US30",
            timeframe="M5",
            direction="SELL",
            confidence=80,
        )

        context.analysis.bearish_confirmation_candle = Candle(
            "10:30",
            106,
            108,
            100,
            101,
        )

        TradeSetupStage().run(context)

        self.assertFalse(
            context.trade_setup.valid,
        )

        self.assertEqual(
            context.trade_setup.entry,
            100,
        )

        self.assertIsNone(
            context.trade_setup.stop_loss,
        )
    def test_valid_buy_setup_produces_buy_decision(self):

        from unittest.mock import patch
        from backend.trade_setup import TradeSetup

        context = self.create_context()

        setup = TradeSetup(
            market="US30",
            timeframe="M5",
            direction="BUY",
            entry=110,
            stop_loss=100,
            take_profit=130,
            risk_reward=2.0,
            valid=True,
                )
        with patch(
            "backend.pipeline.stages.trade_setup_stage.TradeSetupEngine.generate",
            return_value=setup,
        ):

            TradeSetupStage().run(context)

        self.assertIsNotNone(
            context.trade_setup_validation,
        )

        self.assertTrue(
            context.trade_setup_validation.valid,
        )

        self.assertIsNotNone(
            context.decision,
        )

        self.assertEqual(
            context.decision.direction,
            "BUY",
        )

        self.assertEqual(
            context.decision.reason,
            "ACCEPTED",
        )

        self.assertTrue(
            context.decision.risk_valid,
        )


    def test_wait_signal_produces_wait_decision(self):

        from unittest.mock import patch
        from backend.trade_setup import TradeSetup

        context = self.create_context()

        context.signal = Signal(
            market="US30",
            timeframe="M5",
            direction="WAIT",
            confidence=0,
        )

        setup = TradeSetup(
            market="US30",
            timeframe="M5",
            direction="WAIT",
            entry=None,
            stop_loss=None,
            take_profit=None,
            risk_reward=None,
            valid=False,
        )

        with patch(
            "backend.pipeline.stages.trade_setup_stage.TradeSetupEngine.generate",
            return_value=setup,
        ):

            TradeSetupStage().run(context)

        self.assertIsNotNone(
            context.decision,
        )

        self.assertEqual(
            context.decision.direction,
            "WAIT",
        )

        self.assertEqual(
            context.decision.signal_direction,
            "WAIT",
        )


    def test_risk_failure_produces_wait_decision(self):

        from unittest.mock import patch
        from backend.trade_setup import TradeSetup

        context = self.create_context()

        setup = TradeSetup(
            market="US30",
            timeframe="M5",
            direction="BUY",
            entry=110,
            stop_loss=100,
            take_profit=115,
            risk_reward=0.5,
            valid=True,
        )

        with patch(
            "backend.pipeline.stages.trade_setup_stage.TradeSetupEngine.generate",
            return_value=setup,
        ):

            TradeSetupStage().run(context)

        self.assertFalse(
            context.trade_setup_validation.valid,
        )

        self.assertEqual(
            context.trade_setup_validation.reason,
            "RISK_REWARD_BELOW_MINIMUM",
        )

        self.assertIsNotNone(
            context.decision,
        )

        self.assertEqual(
            context.decision.direction,
            "WAIT",
        )

        self.assertEqual(
            context.decision.reason,
            "RISK_REWARD_BELOW_MINIMUM",
        )

        self.assertFalse(
            context.decision.risk_valid,
        )


if __name__ == "__main__":
    unittest.main()
