# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Restored(BasePlotState):
    """
    A plot in the restored state is a plot that was previously segmented and
    skeletonized, but was restored to the segmented state.
    """

    __state__ = 'restored'

    def mark_as_rescaled(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be rescaled after restored.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Rescaled import Rescaled
        return self.context.transit_to(Rescaled()).bind(lambda: Result.ok(self))

    def mark_as_restored(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot already in restored state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
