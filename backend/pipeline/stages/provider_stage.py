"""
provider_stage.py

Provider Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.provider.provider_factory import ProviderFactory


class ProviderStage(PipelineStage):
    """
    Loads market data from the configured provider.
    """

    def __init__(self, provider_type="csv"):

        super().__init__("Provider Stage")

        self.provider_type = provider_type

    def execute(self, context):

        provider = ProviderFactory.create(
            self.provider_type
        )

        context.provider = provider

        context.raw_data = provider.load(
            context.market,
            context.timeframe,
        )

        context.set_metadata(
            "provider",
            provider.__class__.__name__,
        )

        return context