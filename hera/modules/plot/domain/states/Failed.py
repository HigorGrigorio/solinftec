# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.core.domain.errors.InvalidStateTransition import InvalidStateTransition
from modules.crop.domain.states import Queued
from modules.plot.domain import BasePlotState


class Failed(BasePlotState):
    """
    When an error occurs during the plot processing, the plot is marked as failed. From this state, the plot can only
    be marked as cropped or cancelled. Any other operation will result in an error.
    """

    __state__ = 'failed'

    def mark_as_queued(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be queued after failed.

        -------
        Returns
        -------
            Result[State]: The result of operation.
        """
        from .Queued import Queued
        self.context.transit_to(Queued())
        return Result.ok(self)

    def mark_as_failed(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be failed after failed.

        -------
        Returns
        -------
            Result[State]: The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
