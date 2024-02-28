# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Queued(BasePlotState):
    """
    The queued state of a plot. This states represents a plot that is waiting to be processed
    in kafka queue.
    """

    __state__ = 'queued'

    def mark_as_queued(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be queued after queued.

        -------
        Returns
        -------
            Result[State]: The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_cropped(self) -> Result['BasePlotState']:
        """
        Mark the plot as cropped

        -------
        Returns
        -------
            Result[State]: The result of operation.
        """
        from .Cropped import Cropped
        self.context.transit_to(Cropped())
        return Result.ok(self)
