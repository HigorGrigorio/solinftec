# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.piece.domain import BasePieceState


class Skeletonized(BasePieceState):
    """
    The skeletonized state of a piece.
    """

    __state__ = 'skeletonized'

    def mark_as_skeletonized(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in skeletonized state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_restored(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in skeletonized state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Restored import Restored
        self.context.transit_to(Restored())
        return Result.ok(self)
