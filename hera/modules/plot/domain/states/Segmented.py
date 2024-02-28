# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Segmented(BasePlotState):
    """
    A piece in the segmented state is a piece that was previously skeletonized,
    but was segmented again.
    """

    __state__ = 'segmented'

    def mark_as_skeletonized(self) -> Result['BasePlotState']:
        """
        Returns a failure because a piece can't be skeletonized after segmented.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Skeletonized import Skeletonized
        self.context.transit_to(Skeletonized())
        return Result.ok(self)

    def mark_as_segmented(self) -> Result['BasePlotState']:
        """
        Returns a failure because a piece already in segmented state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
