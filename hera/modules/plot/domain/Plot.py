# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import (
    Guid,
)
from olympus.monads import maybe, result, Maybe, guard_all, W, Result

from modules.core.domain.File import File
from .PlotContext import PlotContext, PlotProps, BasePlotState


class Plot(PlotContext):
    """
    Plot entity.
    """

    def __init__(self, state: BasePlotState, props: PlotProps, id: Maybe[Guid]) -> None:
        """
        Args:
            state (BasePlotState): Plot state.
            props (PlotProps): Plot properties.
            id (MaybeGuid): Plot id.
        """
        super().__init__(state, props, id)

    @property
    def file(self) -> File:
        """
        File object.

        Returns:
            File: File object.
        """

        return self.props['file']

    @property
    def description(self) -> str:
        """
        Plot description.

        Returns:
            str: Plot description.
        """

        return self.props['description']

    @property
    def created_at(self) -> str:
        """
        Plot creation date.

        Returns:
            str: Plot creation date.
        """

        return self.props['created_at']

    @property
    def updated_at(self) -> str:
        """
        Plot update date.

        Returns:
            str: Plot update date.
        """

        return self.props['updated_at']

    @classmethod
    def new(
            cls,
            props: PlotProps,
            state: Maybe[BasePlotState] = Maybe.nothing(),
            id: Maybe[Guid] = maybe.none()
    ) -> 'result.Result[Plot]':
        """
        Creates a new plot.

        ----------
        Parameters
        ----------
        props : NewPlotProps
            Plot properties.
        state : Maybe[BasePlotState], optional
            Plot state, by default Maybe.nothing()
        id : Maybe[Guid], optional
            Plot id, by default maybe.none()

        -------
        Returns
        -------
        Plot
            Plot object.
        """

        from .events import PlotCreated
        from .states import Queued

        guarded = guard_all(
            props,
            {
                'file': 'required',
                'description': 'between[0, 255]',
                'pieces': 'required'
            }
        )

        if not guarded.is_satisfied():
            return W(guarded)

        plot = cls(state.get_or_else(Queued), props, id)

        if id.is_nothing():  # is a new plot
            plot.remind(PlotCreated(plot))

        return result.ok(plot)

    def mark_as_cropped(self) -> Result['PlotContext']:
        """
        Mark the plot as cropped.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_cropped().bind(lambda: self)

    def mark_as_failed(self) -> Result['PlotContext']:
        """
        Mark the plot as failed.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_failed().bind(lambda: self)

    def mark_as_queued(self) -> Result['PlotContext']:
        """
        Mark the plot as queued.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_queued().bind(lambda: self)

    def mark_as_skeletonized(self) -> Result['PlotContext']:
        """
        Mark the plot as skeletonized.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_skeletonized().bind(lambda: self)

    def mark_as_segmented(self) -> Result['PlotContext']:
        """
        Mark the plot as segmented.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_segmented().bind(lambda: self)

    def mark_as_restored(self) -> Result['PlotContext']:
        """
        Mark the plot as restored.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_restored().bind(lambda: self)

    def mark_as_rescaled(self) -> Result['PlotContext']:
        """
        Mark the plot as rescaled.

        Returns:
            Result[Plot]: The result of operation.
        """

        return self.state.mark_as_rescaled().bind(lambda: self)

    def mark_as_canceled(self) -> Result['PlotContext']:
        """
        Mark the plot as canceled.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_canceled().bind(lambda: self)

    def mark_as_finished(self) -> Result['PlotContext']:
        """
        Mark the plot as finished.

        Returns:
            Result[Plot]: The result of operation.
        """
        return self.state.mark_as_finished().bind(lambda: self)
