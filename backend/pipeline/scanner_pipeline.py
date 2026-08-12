"""
scanner_pipeline.py

Scanner Pipeline.

Author: Andrew Kyalo
Project: Andy Scanner
"""
from backend.scanner.scanner_result import ScannerResult
from backend.pipeline.pipeline_context import PipelineContext
from backend.pipeline.pipeline_result import PipelineResult



class ScannerPipeline:
    """
    Andy Scanner execution pipeline.

    Responsible for orchestrating all
    registered pipeline stages.
    """

    def __init__(self):

        self._stages = []

    # ==================================================
    # Stage Management
    # ==================================================

    def add_stage(
        self,
        stage,
    ):
        """
        Register a pipeline stage.
        """

        self._stages.append(stage)

    def remove_stage(
        self,
        stage_name,
    ):
        """
        Remove stage by name.
        """

        self._stages = [

            stage

            for stage in self._stages

            if stage.name != stage_name

        ]

    def clear(self):
        """
        Remove all stages.
        """

        self._stages.clear()

    @property
    def stages(self):
        """
        Returns registered stages.
        """

        return list(self._stages)

    # ==================================================
    # Execute Pipeline
    # ==================================================
    
    def run(
        self,
        market,
        timeframe,
        ):
        """
        Execute the complete scanner pipeline.
        """

        context = PipelineContext()

        result = PipelineResult()

        try:

            context.start(
                market,
                timeframe,
           )

            for index, stage in enumerate(self._stages, start=1):

                context.set_metadata(
                    "current_stage",
                    stage.name,
                )

                context.set_metadata(
                    "stage_number",
                    index,
                )

                context = stage.run(context)

            context.finish()

            result.set_success(
                "Pipeline executed successfully."
            )

        except Exception as error:

            context.set_error(error)

            context.finish()

            result.set_failure(
                error,
                (
                    f"Pipeline failed during "
                    f"{context.get_metadata('current_stage')} : "
                    f"{error}"
                ),
               )

        result.add_metadata(
            "market",
            context.market,
        )

        result.add_metadata(
            "timeframe",
            context.timeframe,
        )

        result.add_metadata(
            "stages",
            len(self._stages),
        )

        context.scan_result = ScannerResult(
            market=context.market,
            timeframe=context.timeframe,
            candles=context.candles,
            analyzer=context.analyzer,
            signal=context.signal,
            trade_setup=context.trade_setup,
       )

        result.add_metadata(

            "scan_result",

            context.scan_result,

            )
        return result
    

    
          

    # ==================================================
    # Information
    # ==================================================

    def summary(self):
        """
        Pipeline summary.
        """

        return {

            "total_stages": len(self._stages),

            "stages": [

                stage.name

                for stage in self._stages

            ],

        }

    def __len__(self):

        return len(self._stages)

    def __repr__(self):

        return (

            f"ScannerPipeline("

            f"stages={len(self)})"

        )
