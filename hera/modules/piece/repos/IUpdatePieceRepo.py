# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc

from modules.piece.domain import Piece


class IUpdatePieceRepo(abc.ABC):
    """
    Piece Repository Interface

    This interface is used to update a Piece.
    """

    @abc.abstractmethod
    def update(self, piece: Piece) -> Piece:
        """
        Update a Piece

        ----------
        Parameters
        ----------
        piece : Piece
            Piece to be updated

        -------
        Returns
        -------
        Piece
            The updated Piece
        """
        ...
