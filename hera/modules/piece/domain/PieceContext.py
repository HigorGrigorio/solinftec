# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import abc
from typing import TypedDict

from olympus.monads import Result

from modules.core.domain import Context, File, State


class PieceProps(TypedDict):
    """
    Piece properties

    ----------
    Attributes
    ----------
    file: File
        The file of the piece
    """
    file: File


class BasePieceState(State, abc.ABC):
    """
    Base class for all Piece states.
    States are used to control the Piece's behavior.
    """

    def __init__(self):
        super().__init__()

    def mark_as_cropped(self) -> Result['BasePieceState']:
        """
        Mark the piece as cropped

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_segmented(self) -> Result['BasePieceState']:
        """
        Mark the piece as segmented

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_skeletonized(self) -> Result['BasePieceState']:
        """
        Mark the piece as skeleton

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_restored(self) -> Result['BasePieceState']:
        """
        Mark the piece as restored

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_finished(self) -> Result['BasePieceState']:
        """
        Mark the piece as finished

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_failed(self) -> Result['BasePieceState']:
        """
        Mark the piece as failed

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)

    def mark_as_queued(self) -> Result['BasePieceState']:
        """
        Mark the piece as queued

        Returns:
            Result[BasePieceState]: The result of operation.
        """
        return self._cannot_be(self.__state__)


class PieceContext(Context[PieceProps]):
    """
    The main propose of this class is to bring the context of a piece
    defined in PieceStateBase to a more readable way.
    """

    @abc.abstractmethod
    def mark_as_segmented(self) -> Result:
        """
        Mark the piece as segmented
        """
        ...

    @abc.abstractmethod
    def mark_as_skeleton(self) -> Result:
        """
        Mark the piece as skeleton
        """
        ...

    @abc.abstractmethod
    def mark_as_cropped(self) -> Result:
        """
        Mark the piece as cropped
        """
        ...

    @abc.abstractmethod
    def mark_as_restored(self) -> Result:
        """
        Mark the piece as restored
        """
        ...

    @abc.abstractmethod
    def mark_as_finished(self) -> Result:
        """
        Mark the piece as finished
        """
        ...

    @abc.abstractmethod
    def mark_as_failed(self) -> Result:
        """
        Mark the piece as failed
        """
        ...

    @abc.abstractmethod
    def mark_as_queued(self) -> Result:
        """
        Mark the piece as queued
        """
        ...
