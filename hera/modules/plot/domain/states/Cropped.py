# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.monads import Result

from modules.core.domain.errors import AlreadyInState
from modules.plot.domain import BasePlotState


class Cropped(BasePlotState):
    """
    The cropped state of a plot.
    """

    __state__ = 'cropped'

    def mark_as_segmented(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot can't be segmented after cropped.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        from .Segmented import Segmented

        return self.context.transit_to(Segmented()).bind(lambda: Result.ok(self))

    def mark_as_cropped(self) -> Result['BasePlotState']:
        """
        Returns a failure because a plot already in cropped state.

        -------
        Returns
        -------
        Result[State]
             The result of operation.
        """
        return Result.fail(AlreadyInState(self.context.id, self.__state__))
