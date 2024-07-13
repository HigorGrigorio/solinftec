# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.crop.domain import BaseCropState


class Restored(BaseCropState):
    """
    The restored state of a crop.
    """

    __state__ = 'restored'

    def mark_as_restored(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in restored state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_finished(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in restored state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Finished import Finished
        self.context.transit_to(Finished())
        return Result.ok(self)
