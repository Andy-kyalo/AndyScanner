"""
test_scanner_pipeline.py

Integration tests for the Andy Scanner execution pipeline.

Author: Andrew Kyalo
Project: Andy Scanner
Version: 0.5.0
"""

import unittest
from datetime import datetime
from unittest.mock import patch

from backend.pipeline.scanner_pipeline import ScannerPipeline
from backend.pipeline.pipeline_stage import PipelineStage


class RecordingStage(PipelineStage):

    def __init__(self, name, execution_log):
        super().__init__(name)
        self.execution_log = execution_log

    def execute(self, context):
        self.execution_log.append(
            (
                self.name,
                context.get_metadata("stage_number"),
            )
        )
        return context


class TestScannerPipeline(unittest.TestCase):

    def test_stages_execute_in_registered_order(self):

        execution_log = []

        pipeline = ScannerPipeline()

        stage_names = [
            "Stage One",
            "Stage Two",
            "Stage Three",
        ]

        for name in stage_names:
            pipeline.add_stage(
                RecordingStage(
                    name,
                    execution_log,
                )
            )

        result = pipeline.run(
            "TEST",
            "M1",
        )

        self.assertTrue(
            result.success,
            result.message,
        )

        self.assertEqual(
            execution_log,
            [
                ("Stage One", 1),
                ("Stage Two", 2),
                ("Stage Three", 3),
            ],
        )

    def test_pipeline_preserves_stage_count(self):

        execution_log = []

        pipeline = ScannerPipeline()

        for name in [
            "Stage One",
            "Stage Two",
            "Stage Three",
        ]:
            pipeline.add_stage(
                RecordingStage(
                    name,
                    execution_log,
                )
            )

        result = pipeline.run(
            "TEST",
            "M1",
        )

        self.assertEqual(
            result.metadata["stages"],
            3,
        )

    def test_pipeline_failure_records_error(self):

        class FailingStage(PipelineStage):

            def __init__(self):
                super().__init__("Failing Stage")

            def execute(self, context):
                raise RuntimeError(
                    "Intentional pipeline test failure"
                )

        pipeline = ScannerPipeline()

        pipeline.add_stage(
            FailingStage()
        )

        result = pipeline.run(
            "TEST",
            "M1",
        )

        self.assertFalse(
            result.success
        )

        self.assertIsNotNone(
            result.error
        )

        self.assertIn(
            "Failing Stage",
            result.message,
        )


class DeterministicProviderStage(PipelineStage):

    def __init__(self, candles):
        super().__init__("Provider Stage")
        self.candles = candles

    def execute(self, context):

        context.candles = list(
            self.candles
        )

        context.set_metadata(
            "selected_provider",
            "TEST",
        )

        context.set_metadata(
            "provider_symbol",
            context.market,
        )

        context.set_metadata(
            "now",
            datetime.fromisoformat(
                "2026-01-01 00:13:00"
            ),
        )

        return context


class DeterministicSellProviderStage(
    DeterministicProviderStage
):

    def execute(self, context):

        context = super().execute(
            context
        )

        context.set_metadata(
            "now",
            datetime.fromisoformat(
                "2026-01-01 00:18:00"
            ),
        )

        return context


class TestDeterministicFullPipeline(unittest.TestCase):

    def test_analysis_to_decision_executes_through_production_stages(self):

        from backend.pipeline.stages.mapping_stage import MappingStage
        from backend.pipeline.stages.validation_stage import ValidationStage
        from backend.pipeline.stages.analysis_stage import AnalysisStage
        from backend.pipeline.stages.signal_stage import SignalStage
        from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
        from backend.pipeline.stages.database_stage import DatabaseStage
        from backend.pipeline.stages.report_stage import ReportStage

        class Candle:

            def __init__(
                self,
                time,
                open_,
                high,
                low,
                close,
            ):
                self.time = time
                self.open = open_
                self.high = high
                self.low = low
                self.close = close

            def is_bullish(self):
                return self.close > self.open

            def is_bearish(self):
                return self.close < self.open

            def body_size(self):
                return abs(
                    self.close - self.open
                )

        candles = [

            # 0
            Candle(
                "2026-01-01 00:00:00",
                100,
                100,
                99,
                100,
            ),

            # 1 - INITIAL HIGH
            Candle(
                "2026-01-01 00:01:00",
                100,
                106,
                99,
                105,
            ),

            # 2 - INITIAL LOW
            Candle(
                "2026-01-01 00:02:00",
                105,
                105,
                90,
                92,
            ),

            # 3 - LH
            Candle(
                "2026-01-01 00:03:00",
                92,
                106,
                91,
                100,
            ),

            # 4 - LL
            Candle(
                "2026-01-01 00:04:00",
                100,
                101,
                85,
                95,
            ),

            # 5 - confirms LL
            Candle(
                "2026-01-01 00:05:00",
                95,
                100,
                86,
                90,
            ),

            # 6 - bearish STRUCTURE_BREAK
            Candle(
                "2026-01-01 00:06:00",
                90,
                92,
                78,
                80,
            ),

            # 7 - bullish CHOCH
            # Low must remain above the future HL at candle 8.
            Candle(
                "2026-01-01 00:07:00",
                90,
                130,
                89,
                110,
            ),

            # 8 - protected HL
            # 85 < 88 < 89
            Candle(
                "2026-01-01 00:08:00",
                110,
                112,
                88,
                100,
            ),

            # 9 - bearish candle before confirmation
            # Low remains above the HL at candle 8.
            Candle(
                "2026-01-01 00:09:00",
                102,
                103,
                90,
                98,
            ),

            # 10 - bullish engulfing confirmation
            Candle(
                "2026-01-01 00:10:00",
                97,
                106,
                96,
                105,
            ),

            # 11 - final LL
            # Low creates LL, but close remains above the
            # active protected low (88), preventing a later
            # bearish structure break / CHOCH.
            Candle(
                "2026-01-01 00:11:00",
                105,
                105,
                75,
                95,
            ),

            # 12 - confirms final LL
            Candle(
                "2026-01-01 00:12:00",
                95,
                105,
                76,
                100,
            ),
        ]

        pipeline = ScannerPipeline()

        pipeline.add_stage(
            DeterministicProviderStage(
                candles
            )
        )

        pipeline.add_stage(
            MappingStage()
        )

        pipeline.add_stage(
            ValidationStage()
        )

        pipeline.add_stage(
            AnalysisStage()
        )

        pipeline.add_stage(
            SignalStage()
        )

        pipeline.add_stage(
            TradeSetupStage()
        )

        with patch(
            "backend.pipeline.stages.database_stage.DatabaseManager"
        ) as database_manager, patch(
            "backend.validation.market_validator.FreshnessValidator.validate"
        ) as freshness_validate:

            freshness_validate.return_value = (
                True,
                "Market data freshness validation passed.",
            )

            database = (
                database_manager
                .return_value
                .__enter__
                .return_value
            )

            database.scan_exists.return_value = False

            pipeline.add_stage(
                DatabaseStage()
            )

            pipeline.add_stage(
                ReportStage()
            )

            result = pipeline.run(
                "EUR/USD",
                "M1",
            )

        self.assertTrue(
            result.success,
            result.message,
        )

        scan = result.metadata[
            "scan_result"
        ]

        self.assertIsNotNone(
            scan.signal
        )

        self.assertIsNotNone(
            scan.trade_setup
        )

        self.assertIsNotNone(
            scan.decision
        )

        analyzer = scan.analyzer

        print(
            "\n"
            "===== DETERMINISTIC PIPELINE DIAGNOSTIC ====="
        )

        print(
            "Signal:",
            scan.signal.direction,
        )

        print(
            "Signal confidence:",
            scan.signal.confidence,
        )

        print(
            "Analyzer trend:",
            analyzer.trend(),
        )

        print(
            "Analyzer structural state:",
            analyzer.structural_state(),
        )

        print(
            "Analyzer bullish CHOCH:",
            analyzer.bullish_choch(),
        )

        print(
            "Analyzer bearish CHOCH:",
            analyzer.bearish_choch(),
        )

        print(
            "Analyzer protected low:",
            analyzer.protected_low(),
        )

        print(
            "Analyzer protected high:",
            analyzer.protected_high(),
        )

        print(
            "Trade setup:",
            scan.trade_setup,
        )

        print(
            "Trade setup attributes:",
            {
                name: getattr(
                    scan.trade_setup,
                    name,
                )
                for name in dir(scan.trade_setup)
                if not name.startswith("_")
                and not callable(
                    getattr(
                        scan.trade_setup,
                        name,
                    )
                )
            },
        )

        print(
            "Decision:",
            scan.decision,
        )

        print(
            "Decision attributes:",
            {
                name: getattr(
                    scan.decision,
                    name,
                )
                for name in dir(scan.decision)
                if not name.startswith("_")
                and not callable(
                    getattr(
                        scan.decision,
                        name,
                    )
                )
            },
        )

        print(
            "ScannerResult attributes:",
            sorted(
                name
                for name in dir(scan)
                if not name.startswith("_")
            ),
        )

        print(
            "ScannerResult metadata:",
            result.metadata,
        )

        print(
            "=============================================="
        )

        self.assertEqual(
            scan.signal.direction,
            "BUY",
        )

        self.assertEqual(
            scan.trade_setup.direction,
            "BUY",
        )

        self.assertTrue(
            scan.trade_setup.valid,
        )

        self.assertGreaterEqual(
            scan.trade_setup.risk_reward,
            1.0,
        )

        self.assertEqual(
            scan.decision.direction,
            "BUY",
        )

        self.assertTrue(
            scan.decision.setup_valid,
        )

        self.assertTrue(
            scan.decision.risk_valid,
        )

        self.assertEqual(
            scan.decision.reason,
            "ACCEPTED",
        )

        self.assertEqual(
            result.metadata["stages"],
            8,
        )

        self.assertEqual(
            database.scan_exists.call_count,
            1,
        )

        database.save_signal.assert_called_once()

        database.save_scan.assert_called_once()

    def test_analysis_to_decision_executes_sell_through_production_stages(self):

        from backend.pipeline.stages.mapping_stage import MappingStage
        from backend.pipeline.stages.validation_stage import ValidationStage
        from backend.pipeline.stages.analysis_stage import AnalysisStage
        from backend.pipeline.stages.signal_stage import SignalStage
        from backend.pipeline.stages.trade_setup_stage import TradeSetupStage
        from backend.pipeline.stages.database_stage import DatabaseStage
        from backend.pipeline.stages.report_stage import ReportStage

        class Candle:

            def __init__(
                self,
                time,
                open_,
                high,
                low,
                close,
            ):
                self.time = time
                self.open = open_
                self.high = high
                self.low = low
                self.close = close

            def is_bullish(self):
                return self.close > self.open

            def is_bearish(self):
                return self.close < self.open

            def body_size(self):
                return abs(
                    self.close - self.open
                )

        candles = [

            # 0
            Candle(
                "2026-01-01 00:00:00",
                100,
                100,
                99,
                100,
            ),

            # 1 - INITIAL HIGH
            Candle(
                "2026-01-01 00:01:00",
                100,
                105,
                99,
                103,
            ),

            # 2 - INITIAL LOW
            Candle(
                "2026-01-01 00:02:00",
                103,
                104,
                90,
                92,
            ),

            # 3 - HH
            Candle(
                "2026-01-01 00:03:00",
                108,
                110,
                96,
                100,
            ),

            # 4 - HL
            Candle(
                "2026-01-01 00:04:00",
                108,
                109,
                95,
                100,
            ),

            # 5 - confirms HL
            Candle(
                "2026-01-01 00:05:00",
                100,
                105,
                96,
                102,
            ),

            # 6 - bullish BOS
            Candle(
                "2026-01-01 00:06:00",
                102,
                115,
                98,
                112,
            ),

            # 7 - bearish CHOCH
            Candle(
                "2026-01-01 00:07:00",
                112,
                118,
                94,
                94,
            ),

            # 8 - previous structural low
            # Lower than the future HL at candle 13.
            Candle(
                "2026-01-01 00:08:00",
                94,
                105,
                70,
                102,
            ),

            # 9 - bullish candle before confirmation
            Candle(
                "2026-01-01 00:09:00",
                101,
                104,
                91,
                103,
            ),

            # 10 - bullish candle before confirmation
            Candle(
                "2026-01-01 00:10:00",
                104,
                106,
                90,
                105,
            ),

            # 11 - structural candle
            # Does not create a later break because its close
            # remains below the active high.
            Candle(
                "2026-01-01 00:11:00",
                100,
                119,
                90,
                110,
            ),

            # 12 - lower-high preparation
            # Kept below candle 13 high.
            Candle(
                "2026-01-01 00:12:00",
                90,
                94,
                89,
                93,
            ),

            # 13 - protected LH + HL
            # High 95 is lower than the previous HH 119.
            # Low 80 is higher than the previous structural
            # low 70, making it an HL.
            Candle(
                "2026-01-01 00:13:00",
                90,
                95,
                80,
                93,
            ),

            # 14 - bearish engulfing confirmation
            # Previous candle is bullish:
            #   open 90 -> close 93
            #
            # Current candle:
            #   open 94 > previous close 93
            #   close 89 < previous open 90
            #
            # Entry = 90.
            Candle(
                "2026-01-01 00:14:00",
                94,
                94,
                89,
                89,
            ),

            # 15 - post-confirmation structure
            # Does not break the protected low.
            Candle(
                "2026-01-01 00:15:00",
                90,
                94,
                89,
                92,
            ),

            # 16 - final HH
            # High 96 > protected LH 95.
            # Close remains below 95, so this does not create
            # a bullish structural break.
            Candle(
                "2026-01-01 00:16:00",
                92,
                120,
                90,
                93,
            ),

            # 17 - confirms final HH
            Candle(
                "2026-01-01 00:17:00",
                93,
                94,
                91,
                92,
            ),
        ]

        pipeline = ScannerPipeline()

        pipeline.add_stage(
            DeterministicSellProviderStage(
                candles
            )
        )

        pipeline.add_stage(
            MappingStage()
        )

        pipeline.add_stage(
            ValidationStage()
        )

        pipeline.add_stage(
            AnalysisStage()
        )

        pipeline.add_stage(
            SignalStage()
        )

        pipeline.add_stage(
            TradeSetupStage()
        )

        with patch(
            "backend.pipeline.stages.database_stage.DatabaseManager"
        ) as database_manager, patch(
            "backend.validation.market_validator.FreshnessValidator.validate"
        ) as freshness_validate:

            freshness_validate.return_value = (
                True,
                "Market data freshness validation passed.",
            )

            database = (
                database_manager
                .return_value
                .__enter__
                .return_value
            )

            database.scan_exists.return_value = False

            pipeline.add_stage(
                DatabaseStage()
            )

            pipeline.add_stage(
                ReportStage()
            )

            result = pipeline.run(
                "EUR/USD",
                "M1",
            )

        self.assertTrue(
            result.success,
            result.message,
        )

        scan = result.metadata[
            "scan_result"
        ]

        self.assertIsNotNone(
            scan.signal
        )

        self.assertIsNotNone(
            scan.trade_setup
        )

        self.assertIsNotNone(
            scan.decision
        )

        self.assertEqual(
            scan.signal.direction,
            "SELL",
        )

        self.assertEqual(
            scan.trade_setup.direction,
            "SELL",
        )

        self.assertTrue(
            scan.trade_setup.valid,
        )

        self.assertGreaterEqual(
            scan.trade_setup.risk_reward,
            1.0,
        )

        self.assertIsNotNone(
            scan.analyzer.protected_high()
        )

        self.assertEqual(
            scan.analyzer.protected_high().label,
            "LH",
        )

        self.assertEqual(
            scan.decision.direction,
            "SELL",
        )

        self.assertTrue(
            scan.decision.setup_valid,
        )

        self.assertTrue(
            scan.decision.risk_valid,
        )

        self.assertEqual(
            scan.decision.reason,
            "ACCEPTED",
        )

        self.assertEqual(
            result.metadata["stages"],
            8,
        )

        self.assertEqual(
            database.scan_exists.call_count,
            1,
        )

        database.save_signal.assert_called_once()

        database.save_scan.assert_called_once()


if __name__ == "__main__":
    unittest.main()
