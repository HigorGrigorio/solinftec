# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import Guid
from olympus.domain.events import DomainEvent

from modules.piece.domain import Piece


class PieceSkeletonized(DomainEvent):
    """
    Emitted when a piece is skeletonized
    """
    piece: Piece

    def __init__(self, piece: Piece):
        super().__init__()
        self.piece = piece

    def get_aggregate_id(self) -> Guid:
        """
        Get the aggregate id

        --------
        Returns
        --------
        Guid
            The aggregate id
        """
        return self.piece.id
