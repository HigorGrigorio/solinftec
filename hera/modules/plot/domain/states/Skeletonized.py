# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Skeletonized(BasePlotState):
    """
    When the skeleton algorithm is applied to all crops of the plot, as well as
    the plot itself.
    """

    __state__ = 'skeletonized'

    def mark_as_restored(self) -> 'Result[BasePlotState]':
        """
        Returns a failure because a plot can't be restored after skeletonized.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Restored import Restored
        return self.context.transit_to(Restored()).bind(lambda: Result.ok(self))

    def mark_as_skeletonized(self) -> 'BasePlotState':
        """
        Returns a failure because a plot already in skeletonized state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
