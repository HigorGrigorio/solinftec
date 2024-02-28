# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from typing import List

from olympus.domain import WatchedList
from olympus.monads import Maybe

from modules.piece.domain import Piece


class Pieces(WatchedList[Piece]):
    """
    Represents a list of pieces
    """

    def compare(self, a: Piece, b: Piece) -> bool:
        """
        Compare two pieces

        ----------
        Parameters
        ----------
        a : Piece
            The first piece
        b : Piece
            The second piece

        -------
        Returns
        -------
        bool
            True if the pieces are equal, False otherwise
        """
        return a.id == b.id

    @classmethod
    def new(cls, pieces: Maybe[List[Piece]] = Maybe.nothing()) -> 'Pieces':
        """
        Creates a new Pieces instance

        ----------
        Parameters
        ----------
        pieces : list[Piece]
            The pieces list

        -------
        Returns
        -------
        Pieces
            The Pieces instance
        """
        return cls(pieces.get_or_else(lambda: []))
