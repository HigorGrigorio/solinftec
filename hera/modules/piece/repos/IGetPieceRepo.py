# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc

from olympus.domain import Guid

from modules.piece.domain import Piece


class IGetPieceRepo(abc.ABC):
    """
    Piece Repository Interface

    This interface is used to get a Piece.
    """

    @abc.abstractmethod
    def get(self, id: Guid) -> Piece:
        """
        Get a Piece

        ----------
        Parameters
        ----------
        id : Guid
            Piece id

        -------
        Returns
        -------
        Piece
            The Piece
        """
        pass
