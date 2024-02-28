# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Finished(BasePlotState):
    """
    The finished state of a plot. After a plot is finished, it can't be changed.
    """

    __state__ = 'finished'

    def mark_as_finished(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot already in finished state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))

    def mark_as_failed(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot already in finished state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))