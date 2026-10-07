import unittest

from backend.decision_engine import DecisionEngine
from backend.signal import Signal
from backend.trade_setup import TradeSetup
from backend.trade_setup_validator import TradeSetupValidationResult


class TestDecisionEngine(unittest.TestCase):

    def create_signal(self, direction="BUY", confidence=80):
        return Signal(
            market="US30",
            timeframe="M5",
            direction=direction,
            confidence=confidence,
        )

    def create_setup(self, direction="BUY"):
        if direction in ("BUY", "STRONG BUY"):
            return TradeSetup(
                market="US30",
                timeframe="M5",
                direction=direction,
                entry=110,
                stop_loss=100,
                take_profit=130,
                risk_reward=2.0,
                valid=True,
            )

        return TradeSetup(
            market="US30",
            timeframe="M5",
            direction=direction,
            entry=100,
            stop_loss=110,
            take_profit=80,
            risk_reward=2.0,
            valid=True,
        )

    def create_valid_validation(self, rr=2.0):
        return TradeSetupValidationResult(
            valid=True,
            reason="ACCEPTED",
            risk_reward=rr,
        )

    # ==================================================
    # ACCEPTED TRADES
    # ==================================================

    def test_valid_buy_is_accepted(self):
        signal = self.create_signal("BUY")
        setup = self.create_setup("BUY")
        validation = self.create_valid_validation()

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(decision.direction, "BUY")
        self.assertTrue(decision.setup_valid)
        self.assertTrue(decision.risk_valid)
        self.assertEqual(decision.reason, "ACCEPTED")

    def test_valid_sell_is_accepted(self):
        signal = self.create_signal("SELL")
        setup = self.create_setup("SELL")
        validation = self.create_valid_validation()

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(decision.direction, "SELL")
        self.assertTrue(decision.setup_valid)
        self.assertTrue(decision.risk_valid)
        self.assertEqual(decision.reason, "ACCEPTED")

    # ==================================================
    # RILEY WAIT GATE
    # ==================================================

    def test_wait_signal_remains_wait(self):
        signal = self.create_signal("WAIT")
        setup = self.create_setup("BUY")
        validation = self.create_valid_validation()

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(decision.direction, "WAIT")
        self.assertEqual(decision.signal_direction, "WAIT")

    # ==================================================
    # MISSING SETUP
    # ==================================================

    def test_missing_setup_returns_wait(self):
        signal = self.create_signal("BUY")

        decision = DecisionEngine().generate(
            signal,
            None,
            None,
        )

        self.assertEqual(decision.direction, "WAIT")
        self.assertEqual(
            decision.reason,
            "TRADE_SETUP_MISSING",
        )

    # ==================================================
    # INVALID SETUP
    # ==================================================

    def test_invalid_setup_returns_wait(self):
        signal = self.create_signal("BUY")

        setup = TradeSetup(
            market="US30",
            timeframe="M5",
            direction="BUY",
            valid=False,
        )

        validation = TradeSetupValidationResult(
            valid=False,
            reason="STRUCTURALLY_INVALID",
            risk_reward=None,
        )

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(decision.direction, "WAIT")
        self.assertEqual(
            decision.reason,
            "STRUCTURALLY_INVALID",
        )

    # ==================================================
    # MISSING VALIDATION
    # ==================================================

    def test_missing_validation_returns_wait(self):
        signal = self.create_signal("BUY")
        setup = self.create_setup("BUY")

        decision = DecisionEngine().generate(
            signal,
            setup,
            None,
        )

        self.assertEqual(decision.direction, "WAIT")
        self.assertEqual(
            decision.reason,
            "RISK_VALIDATION_MISSING",
        )

    # ==================================================
    # FAILED RISK VALIDATION
    # ==================================================

    def test_failed_risk_validation_returns_wait(self):
        signal = self.create_signal("BUY")
        setup = self.create_setup("BUY")

        validation = TradeSetupValidationResult(
            valid=False,
            reason="RISK_REWARD_BELOW_MINIMUM",
            risk_reward=0.8,
        )

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(decision.direction, "WAIT")
        self.assertEqual(
            decision.reason,
            "RISK_REWARD_BELOW_MINIMUM",
        )
        self.assertEqual(
            decision.risk_reward,
            0.8,
        )

    # ==================================================
    # UNSUPPORTED SIGNAL
    # ==================================================

    def test_unsupported_signal_returns_wait(self):
        signal = self.create_signal("HOLD")
        setup = self.create_setup("HOLD")

        validation = self.create_valid_validation()

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(decision.direction, "WAIT")
        self.assertEqual(
            decision.reason,
            "UNSUPPORTED_DIRECTION",
        )

    # ==================================================
    # MISSING SIGNAL
    # ==================================================

    def test_missing_signal_returns_wait(self):
        decision = DecisionEngine().generate(
            None,
            None,
            None,
        )

        self.assertEqual(
            decision.direction,
            "WAIT",
        )

        self.assertEqual(
            decision.reason,
            "SIGNAL_MISSING",
        )
    def test_buy_signal_with_sell_setup_returns_wait(self):
        signal = self.create_signal("BUY")
        setup = self.create_setup("SELL")
        validation = self.create_valid_validation()

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(
            decision.direction,
            "WAIT",
        )

        self.assertEqual(
            decision.reason,
            "SIGNAL_SETUP_DIRECTION_MISMATCH",
        )

    def test_sell_signal_with_buy_setup_returns_wait(self):
        signal = self.create_signal("SELL")
        setup = self.create_setup("BUY")
        validation = self.create_valid_validation()

        decision = DecisionEngine().generate(
            signal,
            setup,
            validation,
        )

        self.assertEqual(
            decision.direction,
            "WAIT",
        )

        self.assertEqual(
            decision.reason,
            "SIGNAL_SETUP_DIRECTION_MISMATCH",
        )


if __name__ == "__main__":
    unittest.main()
