# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from shared.logic import UnexpectedError


class PieceNotFound(UnexpectedError):
    """
    PieceNotFound is raised when the piece is not found
    """

    """
    id: str
        The piece id that was not found
    """
    id: str

    def __init__(self, id: str) -> None:
        super().__init__(f"Piece {id} not found")
        self.id = id
