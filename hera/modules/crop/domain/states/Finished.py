# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.crop.domain import BaseCropState


class Finished(BaseCropState):
    """
    The finished state of a crop.
    """

    __state__ = 'finished'

    def mark_as_finished(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in finished state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
