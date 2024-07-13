# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import abc
from abc import ABC
from typing import TypeVar, TypedDict, Optional

from olympus.monads import Result, Maybe

from modules.core.domain import Context, File, State
from modules.plot.domain import Crops

P = TypeVar('P')


class PlotProps(TypedDict):
    """
    Plot properties.

    ----------
    Attributes
    ----------
    file: File
        File object.
    description: str
        Plot description.

    ----------
    Optional Attributes
    ----------
    User can add any other attributes to this dictionary.

    """

    file: File
    description: str
    crops: Maybe[Crops]

    created_at: Optional[str]
    updated_at: Optional[str]


class BasePlotState(State, abc.ABC):
    """
    This is an abstract base class that represents a crop of a plot in a state machine context.
    It provides three abstract methods that must be implemented by any concrete subclass:
    - crop: to crop the crop
    - restore: to restore the crop to its original state
    - rescale: to rescale the crop

    Each of these methods should return a Result object containing an instance of BasePlotState.
    """

    def __init__(self):
        """
        Initialize the BasePlotState instance.
        """
        super().__init__()

    def mark_as_queued(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as queued.
        This method must be implemented by any concrete subclass.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        return self._cannot_be('queued')

    def mark_as_cropped(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as cropped.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        return self._cannot_be('cropped')

    def mark_as_segmented(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as segmented.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        return self._cannot_be('segmented')

    def mark_as_skeletonized(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as skeleton.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        return self._cannot_be('skeletonized')

    def mark_as_restored(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as restored.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        return self._cannot_be('restored')

    def mark_as_rescaled(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as rescaled.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        return self._cannot_be('rescaled')

    def mark_as_finished(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as finished.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        return self._cannot_be('finished')

    def mark_as_canceled(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as cancelled.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        from .states.Canceled import Canceled
        self.context.transit_to(Canceled())
        return Result.ok(self)

    def mark_as_failed(self) -> Result['BasePlotState']:
        """
        Abstract method to mark the crop as failed.
        This method must be implemented by any concrete subclass.

        -------
        Returns
        -------
        Result[State]
            The result of operation.
        """
        from .states.Failed import Failed
        self.context.transit_to(Failed())
        return Result.ok(self)


class PlotContext(Context[PlotProps], ABC):
    """
    The main propose of this class is to provide a context to the state
    machine into domain layer.

    When a state is changed, the context is updated with the new state, and
    this action is recorded as a domain event.
    """

    @abc.abstractmethod
    def mark_as_queued(self) -> Result['PlotContext']:
        """
        Mark the plot as queued.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_cropped(self) -> Result['PlotContext']:
        """
        Mark the plot as cropped.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_segmented(self) -> Result['PlotContext']:
        """
        Mark the plot as segmented.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_skeletonized(self) -> Result['PlotContext']:
        """
        Mark the plot as skeletonized.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_restored(self) -> Result['PlotContext']:
        """
        Mark the plot as restored.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_rescaled(self) -> Result['PlotContext']:
        """
        Mark the plot as rescaled.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_finished(self) -> Result['PlotContext']:
        """
        Mark the plot as finished.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        ...

    @abc.abstractmethod
    def mark_as_canceled(self) -> Result['PlotContext']:
        """
        Mark the plot as cancelled. All states can be cancelled, except Cancelled.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        from .states import Canceled
        self.transit_to(Canceled())
        return Result.ok(self)

    @abc.abstractmethod
    def mark_as_failed(self) -> Result['PlotContext']:
        """
        Mark the plot as failed. When a plot is failed, it can't be changed to any other state
        except Cancelled.

        Returns:
            Result[PlotContext]: The result of operation.
        """
        from .states import Failed
        self.transit_to(Failed())
        return Result.ok(self)
