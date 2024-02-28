# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Rescaled(BasePlotState):
    """
    The rescaled state of a plot.
    """

    __state__ = 'rescaled'

    def mark_as_finished(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be finished after rescaled.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Finished import Finished
        self.context.transit_to(Finished())
        return Result.ok(self)

    def mark_as_rescaled(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot already in rescaled state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))