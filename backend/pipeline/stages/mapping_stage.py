"""
mapping_stage.py

Mapping Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from backend.pipeline.pipeline_stage import PipelineStage
from backend.mapping.mapper_factory import MapperFactory


class MappingStage(PipelineStage):
    """
    Converts raw provider output into Candle objects.

    If the provider already returns Candle objects,
    mapping is skipped.
    """

    def __init__(self, mapper_type="json"):

        super().__init__("Mapping Stage")

        self.mapper_type = mapper_type

    def execute(self, context):

        # Provider already produced Candle objects.
        if context.candles is not None:

            context.set_metadata(
                "mapper",
                "SKIPPED",
            )

            context.set_metadata(
                "candles",
                len(context.candles),
            )

            return context

        # Otherwise map raw provider data.
        if context.raw_data is None:

            raise ValueError(
                "Mapping Stage received no raw market data."
            )

        mapper = MapperFactory.create(
            self.mapper_type
        )

        context.mapper = mapper

        context.candles = mapper.map(
            context.raw_data
        )

        context.set_metadata(
            "mapper",
            mapper.__class__.__name__,
        )

        context.set_metadata(
            "candles",
            len(context.candles),
        )

        return context
