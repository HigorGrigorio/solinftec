# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import abc
from typing import TypedDict, Optional

from olympus.domain import Guid
from olympus.monads import Result, Maybe

from modules.core.domain import Context, File, State


class CropProps(TypedDict):
    """
    Crop properties

    ----------
    Attributes
    ----------
    file: File
        The file of the crop
    """
    file: File
    plot_id: Maybe[Guid]

    created_at: Optional[str]
    updated_at: Optional[str]


class BaseCropState(State, abc.ABC):
    """
    Base class for all Crop states.
    States are used to control the Crop's behavior.
    """

    def __init__(self):
        super().__init__()

    def mark_as_cropped(self) -> Result['BaseCropState']:
        """
        Mark the crop as cropped

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_segmented(self) -> Result['BaseCropState']:
        """
        Mark the crop as segmented

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_skeletonized(self) -> Result['BaseCropState']:
        """
        Mark the crop as skeleton

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_restored(self) -> Result['BaseCropState']:
        """
        Mark the crop as restored

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_finished(self) -> Result['BaseCropState']:
        """
        Mark the crop as finished

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_failed(self) -> Result['BaseCropState']:
        """
        Mark the crop as failed

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_queued(self) -> Result['BaseCropState']:
        """
        Mark the crop as queued

        Returns:
            Result[BaseCropState]: The result of operation.
        """
        return self._cannot_be(self.__state__)


class CropContext(Context[CropProps]):
    """
    The main propose of this class is to bring the context of a crop
    defined in PieceStateBase to a more readable way.
    """

    @abc.abstractmethod
    def mark_as_segmented(self) -> Result:
        """
        Mark the crop as segmented
        """
        ...

    @abc.abstractmethod
    def mark_as_skeleton(self) -> Result:
        """
        Mark the crop as skeleton
        """
        ...

    @abc.abstractmethod
    def mark_as_cropped(self) -> Result:
        """
        Mark the crop as cropped
        """
        ...

    @abc.abstractmethod
    def mark_as_restored(self) -> Result:
        """
        Mark the crop as restored
        """
        ...

    @abc.abstractmethod
    def mark_as_finished(self) -> Result:
        """
        Mark the crop as finished
        """
        ...

    @abc.abstractmethod
    def mark_as_failed(self) -> Result:
        """
        Mark the crop as failed
        """
        ...

    @abc.abstractmethod
    def mark_as_queued(self) -> Result:
        """
        Mark the crop as queued
        """
        ...