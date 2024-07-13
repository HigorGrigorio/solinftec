# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.crop.domain import BaseCropState


class Segmented(BaseCropState):
    """
    After segmentation, the crop is in the Segmented state.
    """

    __state__ = 'segmented'

    def mark_as_segmented(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop can't be segmented twice.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_skeletonized(self) -> Result['BaseCropState']:
        """
        Mark the crop as skeleton

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Skeletonized import Skeletonized
        self.context.transit_to(Skeletonized())
        return Result.ok(self)
