# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from abc import abstractmethod, ABC

from modules.piece.domain import Piece


class ICreatePieceRepo(ABC):
    """
    Piece Repository Interface

    This interface is used to create a Piece.
    """

    @abstractmethod
    def create(self, piece: Piece) -> Piece:
        """
        Create a Piece

        ----------
        Parameters
        ----------
        piece : Piece
            Piece to be created

        -------
        Returns
        -------
        Piece
            The created Piece
        """
        ...
