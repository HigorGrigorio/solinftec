# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.piece.domain import BasePieceState


class Segmented(BasePieceState):
    """
    After segmentation, the piece is in the Segmented state.
    """

    __state__ = 'segmented'

    def mark_as_segmented(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece can't be segmented twice.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_skeletonized(self) -> Result['BasePieceState']:
        """
        Mark the piece as skeleton

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Skeletonized import Skeletonized
        self.context.transit_to(Skeletonized())
        return Result.ok(self)
