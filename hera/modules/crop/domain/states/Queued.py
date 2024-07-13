# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.crop.domain import BaseCropState


class Queued(BaseCropState):
    """
    This class is initial state of Crop context
    """

    __state__ = 'queued'

    def mark_as_segmented(self) -> Result['BaseCropState']:
        """
        Mark the crop as segmented

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Segmented import Segmented
        self.context.transit_to(Segmented())
        return Result.ok(self)

    def mark_as_queued(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in queued state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
