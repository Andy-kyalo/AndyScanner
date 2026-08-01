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
    Converts provider output into Candle objects.

    If the provider already returns Candle objects,
    mapping is skipped.
    """

    def __init__(self, mapper_type="csv"):

        super().__init__("Mapping Stage")

        self.mapper_type = mapper_type

    def execute(self, context):

        # Provider already produced Candle objects
        if (
            hasattr(context, "candles")
            and context.candles
        ):

            context.set_metadata(
                "mapper",
                "SKIPPED",
            )

            context.set_metadata(
                "candles",
                len(context.candles),
            )

            return context

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