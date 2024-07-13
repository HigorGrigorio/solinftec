# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.crop.domain import BaseCropState


class Failed(BaseCropState):
    """
    The failed state of a crop.
    """

    __state__ = 'failed'

    def mark_as_failed(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in failed state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_queued(self) -> Result['BaseCropState']:
        """
        Returns a failure because a crop already in failed state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Queued import Queued
        self.context.transit_to(Queued())
        return Result.ok(self)
