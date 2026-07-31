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
    Converts raw provider data into Candle objects.
    """

    def __init__(self, mapper_type="csv"):

        super().__init__("Mapping Stage")

        self.mapper_type = mapper_type

    def execute(self, context):

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
            len(context.candles)
        )

        return context