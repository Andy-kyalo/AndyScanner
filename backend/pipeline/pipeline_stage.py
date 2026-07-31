"""
pipeline_stage.py

Base Pipeline Stage.

Author: Andrew Kyalo
Project: Andy Scanner
"""

from abc import ABC, abstractmethod


class PipelineStage(ABC):
    """
    Base class for every scanner pipeline stage.
    """

    def __init__(self, name=None):

        self._name = name or self.__class__.__name__

    @property
    def name(self):
        """
        Stage name.
        """
        return self._name

    @abstractmethod
    def execute(self, context):
        """
        Execute the pipeline stage.

        Parameters
        ----------
        context : PipelineContext

        Returns
        -------
        PipelineContext
        """
        raise NotImplementedError(
            f"{self.name} must implement execute()."
        )

    def before_execute(self, context):
        """
        Hook executed before execute().

        Override when necessary.
        """
        return context

    def after_execute(self, context):
        """
        Hook executed after execute().

        Override when necessary.
        """
        return context

    def run(self, context):
        """
        Complete execution lifecycle.
        """

        context = self.before_execute(context)

        context = self.execute(context)

        context = self.after_execute(context)

        return context

    def __repr__(self):

        return f"{self.__class__.__name__}(name='{self.name}')"