# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from typing import Dict

from olympus.domain import Guid

from modules.piece.domain import Piece
from modules.piece.repos import IPieceRepo


class InMemoryPieceRepo(IPieceRepo):
    """
    InMemory Piece Repository
    """

    def __init__(self):
        self._pieces: Dict[str, Piece] = dict[str, Piece]()

    def create(self, piece: Piece):
        self._pieces[piece.id.value] = piece
        return piece

    def update(self, piece: Piece):
        self._pieces[piece.id] = piece
        return piece

    def get(self, id: Guid):
        return self._pieces.get(id.value)
