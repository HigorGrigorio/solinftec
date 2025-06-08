# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Segmented(BasePlotState):
    """
    A crop in the segmented state is a crop that was previously skeletonized,
    but was segmented again.
    """

    __state__ = 'segmented'

    def mark_as_skeletonized(self) -> Result['BasePlotState']:
        """
        Returns a failure because a crop can't be skeletonized after segmented.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Skeletonized import Skeletonized
        return self.context.transit_to(Skeletonized()).bind(lambda: Result.ok(self))

    def mark_as_segmented(self) -> Result['BasePlotState']:
        """
        Returns a failure because a crop already in segmented state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
