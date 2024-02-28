# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors.InvalidStateTransition import InvalidStateTransition
from modules.plot.domain import BasePlotState


class Canceled(BasePlotState):
    """
    Represents the canceled state of the plot.
    """

    __state__ = 'canceled'

    def _cannot_be(self, state: str):
        """
        Return a failure with a PlotAlreadyFinished exception.

        -------
        Returns
        -------
            Result[State]: The result of operation.
        """
        return Result.fail(InvalidStateTransition(self.context.id, self.__state__, state))

    def mark_as_queued(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be queued after canceled.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Queued import Queued
        self.context.transit_to(Queued())
        return Result.ok(self)
