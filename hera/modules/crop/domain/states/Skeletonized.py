# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.crop.domain import BaseCropState


class Skeletonized(BaseCropState):
    """
    The skeletonized state of a crop.
    """

    __state__ = 'skeletonized'

    def mark_as_skeletonized(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in skeletonized state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_restored(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in skeletonized state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Restored import Restored
        self.context.transit_to(Restored())
        return Result.ok(self)
