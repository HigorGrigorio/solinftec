# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.piece.domain import BasePieceState


class Finished(BasePieceState):
    """
    The finished state of a piece.
    """

    __state__ = 'finished'

    def mark_as_finished(self) -> Result['BasePieceState']:
        """
        Returns a failure because a piece already in finished state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
