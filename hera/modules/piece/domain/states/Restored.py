# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.piece.domain import BasePieceState


class Restored(BasePieceState):
    """
    The restored state of a piece.
    """

    __state__ = 'restored'

    def mark_as_restored(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in restored state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_finished(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in restored state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Finished import Finished
        self.context.transit_to(Finished())
        return Result.ok(self)
