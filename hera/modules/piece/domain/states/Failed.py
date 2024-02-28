# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.piece.domain import BasePieceState


class Failed(BasePieceState):
    """
    The failed state of a piece.
    """

    __state__ = 'failed'

    def mark_as_failed(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in failed state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_queued(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in failed state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Queued import Queued
        self.context.transit_to(Queued())
        return Result.ok(self)
