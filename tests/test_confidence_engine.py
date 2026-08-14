import unittest

from backend.analysis_result import AnalysisResult
from backend.confidence_engine import ConfidenceEngine


class TestConfidenceEngine(unittest.TestCase):

    def create_analysis(self, trend="SIDEWAYS"):

        analysis = AnalysisResult()
        analysis.market = "US30"
        analysis.timeframe = "M5"
        analysis.trend = trend

        return analysis

    # ==================================================
    # SIDEWAYS
    # ==================================================

    def test_sideways_market_has_zero_confidence(self):

        analysis = self.create_analysis("SIDEWAYS")

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            0,
        )

    # ==================================================
    # BULLISH SCORING
    # ==================================================

    def test_bullish_base_confidence(self):

        analysis = self.create_analysis("UPTREND")

        engine = ConfidenceEngine(analysis)

        # Base bullish confidence = 5
        self.assertEqual(
            engine.calculate(),
            5,
        )

    def test_bullish_bos_adds_25(self):

        analysis = self.create_analysis("UPTREND")
        analysis.bullish_bos = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            30,
        )

    def test_bullish_choch_adds_20(self):

        analysis = self.create_analysis("UPTREND")
        analysis.bullish_choch = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            25,
        )

    def test_bullish_order_block_adds_15(self):

        analysis = self.create_analysis("UPTREND")
        analysis.bullish_order_block = object()

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            20,
        )

    def test_bullish_fvg_adds_15(self):

        analysis = self.create_analysis("UPTREND")
        analysis.bullish_fvg = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            20,
        )

    def test_buy_side_liquidity_adds_10(self):

        analysis = self.create_analysis("UPTREND")
        analysis.buy_side_liquidity = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            15,
        )

    def test_bullish_engulfing_adds_10(self):

        analysis = self.create_analysis("UPTREND")
        analysis.bullish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            15,
        )

    # ==================================================
    # BEARISH SCORING
    # ==================================================

    def test_bearish_base_confidence(self):

        analysis = self.create_analysis("DOWNTREND")

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            5,
        )

    def test_bearish_bos_adds_25(self):

        analysis = self.create_analysis("DOWNTREND")
        analysis.bearish_bos = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            30,
        )

    def test_bearish_choch_adds_20(self):

        analysis = self.create_analysis("DOWNTREND")
        analysis.bearish_choch = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            25,
        )

    def test_bearish_order_block_adds_15(self):

        analysis = self.create_analysis("DOWNTREND")
        analysis.bearish_order_block = object()

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            20,
        )

    def test_bearish_fvg_adds_15(self):

        analysis = self.create_analysis("DOWNTREND")
        analysis.bearish_fvg = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            20,
        )

    def test_sell_side_liquidity_adds_10(self):

        analysis = self.create_analysis("DOWNTREND")
        analysis.sell_side_liquidity = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            15,
        )

    def test_bearish_engulfing_adds_10(self):

        analysis = self.create_analysis("DOWNTREND")
        analysis.bearish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            15,
        )

    # ==================================================
    # MAXIMUM SCORE
    # ==================================================

    def test_bullish_confidence_cannot_exceed_100(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_fvg = [object()]
        analysis.buy_side_liquidity = [object()]
        analysis.bullish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            100,
        )

    def test_bearish_confidence_cannot_exceed_100(self):

        analysis = self.create_analysis("DOWNTREND")

        analysis.bearish_bos = True
        analysis.bearish_choch = True
        analysis.bearish_order_block = object()
        analysis.bearish_fvg = [object()]
        analysis.sell_side_liquidity = [object()]
        analysis.bearish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.calculate(),
            100,
        )

    # ==================================================
    # GRADES
    # ==================================================

    def test_grade_a_plus(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_fvg = [object()]
        analysis.buy_side_liquidity = [object()]
        analysis.bullish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "A+",
        )

    def test_grade_a(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "A",
        )

    def test_grade_b(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "B",
        )

    def test_grade_c(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_fvg = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "C",
        )

    def test_grade_d(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "D",
        )
        # ==================================================
    # GRADES
    # ==================================================

        # ==================================================
    # GRADES
    # ==================================================

    def test_grade_a_plus(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_fvg = [object()]
        analysis.buy_side_liquidity = [object()]
        analysis.bullish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "A+",
        )

    def test_grade_a(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_fvg = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "A",
        )

    def test_grade_b(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()
        analysis.bullish_engulfing = [object()]

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "B",
        )

    def test_grade_c(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True
        analysis.bullish_order_block = object()

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "C",
        )

    def test_grade_d(self):

        analysis = self.create_analysis("UPTREND")

        analysis.bullish_bos = True
        analysis.bullish_choch = True

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "D",
        )

    def test_grade_f_for_low_confidence(self):

        analysis = self.create_analysis("UPTREND")

        engine = ConfidenceEngine(analysis)

        self.assertEqual(
            engine.grade(),
            "F",
        )


if __name__ == "__main__":
    unittest.main()