"""
provider_stage.py

Provider Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage

from backend.provider_factory import ProviderFactory
from backend.provider_retry import ProviderRetry
from backend.provider_timeout import ProviderTimeout

from backend.register_providers import register_providers
from backend.scanner_config import ScannerConfig


class ProviderStage(PipelineStage):
    """
    Responsible for obtaining market data
    from the configured provider.
    """

    def __init__(self):

        super().__init__("Provider Stage")

    def execute(self, context):

        provider_manager = register_providers()

        config = ScannerConfig(
            market=context.market,
            timeframe=context.timeframe,
        )

        factory = ProviderFactory(provider_manager)

        provider = factory.create(config)

        provider_manager.record_success()

        timeout = ProviderTimeout(
            timeout=10.0,
        )

        retry = ProviderRetry(
            retries=3,
            delay=1.0,
        )

        candles = retry.execute(
            lambda: timeout.execute(
                provider.load
            )
        )

        context.provider = provider

        context.provider_manager = provider_manager

        context.candles = candles

        context.set_metadata(
            "provider",
            provider.name,
        )

        context.set_metadata(
            "candles",
            len(candles),
        )

        return context