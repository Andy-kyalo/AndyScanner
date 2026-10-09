"""
Scanner Pipeline.

Orchestrates registered stages and records execution observability.
"""

from time import perf_counter

from backend.logger import logger
from backend.scanner.scanner_result import ScannerResult
from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.pipeline_result import PipelineResult
from backend.pipeline.pipeline_metrics import PipelineMetrics
from backend.log_redaction import redact_secrets


class ScannerPipeline:
    """Andy Scanner execution pipeline."""

    def __init__(self):
        self._stages = []
        self._metrics = PipelineMetrics()

    @property
    def metrics(self):
        """Return the pipeline execution metrics collector."""
        return self._metrics

    @staticmethod
    def _log(message, level="info"):
        """Logging must never interrupt pipeline execution."""
        try:
            if level == "error":
                logger.error_log(message)
            else:
                logger.info("Scanner", message)
        except Exception:
            pass

    def add_stage(self, stage):
        """Register a pipeline stage."""
        self._stages.append(stage)

    def remove_stage(self, stage_name):
        """Remove stages matching the supplied name."""
        self._stages = [
            stage for stage in self._stages
            if stage.name != stage_name
        ]

    def clear(self):
        """Remove all registered stages."""
        self._stages.clear()

    @property
    def stages(self):
        """Return a copy of registered stages."""
        return list(self._stages)

    def run(self, market, timeframe, metadata=None, provider_config=None):
        """Execute the pipeline while recording lifecycle metrics."""
        started = perf_counter()
        context = PipelineContext()
        context.provider_config = provider_config
        result = PipelineResult()

        if metadata:
            for key, value in metadata.items():
                context.set_metadata(key, value)

        failed_stage = None

        try:
            context.start(market, timeframe)

            for index, stage in enumerate(self._stages, start=1):
                failed_stage = stage.name

                context.set_metadata("current_stage", stage.name)
                context.set_metadata("stage_number", index)

                stage_started = perf_counter()
                self._log(
                    f"Pipeline stage started: {stage.name} "
                    f"({index}/{len(self._stages)})"
                )

                try:
                    context = stage.run(context)
                except Exception:
                    stage_duration = perf_counter() - stage_started
                    self._log(
                        f"Pipeline stage failed: {stage.name}; "
                        f"duration={stage_duration:.3f}s",
                        level="error",
                    )
                    raise

                stage_duration = perf_counter() - stage_started
                self._log(
                    f"Pipeline stage completed: {stage.name}; "
                    f"duration={stage_duration:.3f}s"
                )

            context.finish()
            result.set_success("Pipeline executed successfully.")

        except Exception as error:
            context.set_error(error)
            context.finish()

            self._log(
                f"Pipeline failed at stage {failed_stage or 'initialization'}",
                level="error",
            )
            result.set_failure(
                error,
                redact_secrets(
                    f"Pipeline failed during "
                    f"{context.get_metadata('current_stage')} : "
                    f"{error}"
                ),
            )

        duration = perf_counter() - started
        self._metrics.record(duration, success=result.success)

        self._log(
            f"Pipeline finished: status="
            f"{'SUCCESS' if result.success else 'FAILED'}; "
            f"duration={duration:.3f}s"
        )

        result.add_metadata("market", context.market)
        result.add_metadata("timeframe", context.timeframe)
        result.add_metadata("stages", len(self._stages))
        result.add_metadata("duration", round(duration, 3))

        if result.success:
            context.scan_result = ScannerResult(
                market=context.market,
                timeframe=context.timeframe,
                candles=context.candles,
                analyzer=context.analyzer,
                signal=context.signal,
                trade_setup=context.trade_setup,
                decision=context.decision,
                provider=context.get_metadata("selected_provider"),
                provider_symbol=context.get_metadata("provider_symbol"),
            )

            result.add_metadata("scan_result", context.scan_result)

        return result

    def summary(self):
        """Return pipeline structure and execution metrics."""
        return {
            "total_stages": len(self._stages),
            "stages": [stage.name for stage in self._stages],
            "metrics": self._metrics.summary(),
        }

    def __len__(self):
        return len(self._stages)

    def __repr__(self):
        return f"ScannerPipeline(stages={len(self)})"
