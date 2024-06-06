# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from shared.logic import UnexpectedError


class PieceAlreadySegmented(UnexpectedError):
    """
    PieceAlreadySegmented is raised when a piece is already segmented
    """

    id: str
    """
    id is the piece id
    """

    def __init__(self, id: str) -> None:
        """
        Creates a new PieceAlreadySegmented instance

        ----------
        Parameters
        ----------
        id : str
            The piece id
        """
        self.id = id
        super().__init__(f"Piece {id} is already segmented")
