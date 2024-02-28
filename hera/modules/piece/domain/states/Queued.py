# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.piece.domain import BasePieceState


class Queued(BasePieceState):
    """
    This class is initial state of Piece context
    """

    __state__ = 'queued'

    def mark_as_segmented(self) -> Result['BasePieceState']:
        """
        Mark the piece as segmented

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Segmented import Segmented
        self.context.transit_to(Segmented())
        return Result.ok(self)

    def mark_as_queued(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in queued state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
