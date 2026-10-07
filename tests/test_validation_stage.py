from unittest import TestCase
from datetime import datetime, timedelta, timezone

from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.stages.validation_stage import ValidationStage


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


class TestValidationStage(TestCase):

    def create_context(self):
        base_time = datetime.now(timezone.utc) - timedelta(minutes=12)

        context = PipelineContext()

        context.start(
            "US30",
            "M5",
        )

        context.candles = [
            Candle(
                base_time.strftime("%Y-%m-%d %H:%M"),
                100,
                110,
                95,
                105,
            ),
            Candle(
                (base_time + timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M"),
                105,
                115,
                100,
                112,
            ),
            Candle(
                (base_time + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M"),
                112,
                118,
                110,
                117,
            ),
        ]

        return context

    def test_validation_stage_passes_valid_data(self):
        context = self.create_context()

        stage = ValidationStage()

        result = stage.run(context)

        self.assertIs(result, context)

        self.assertIsNotNone(
            context.validator
        )

        self.assertEqual(
            context.get_metadata("validation"),
            "PASSED",
        )

        self.assertEqual(
            context.get_metadata(
                "validation_message"
            ),
            "Market data validation passed.",
        )

    def test_validation_stage_rejects_invalid_timeframe(self):
        context = self.create_context()

        context.candles[1].time = "10:03"

        stage = ValidationStage()

        with self.assertRaises(ValueError):
            stage.run(context)


if __name__ == "__main__":
    import unittest

    unittest.main()
