# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.domain import Guid
from olympus.monads.maybe import just

from infra.schemas.sqlalchemy import PieceModel
from modules.piece.domain import Piece


class AlchemyPieceMapper:
    """
    Piece Mapper
    """

    def __init__(self, piece: Piece | PieceModel):
        self.piece = piece

    def _map_model_state_to_domain(self) -> PieceBaseState:
        """
        Map the model state to domain state. This function uses
        BasePlotState.__subclasses__() to get all BasePlotState
        subclasses and then compare __state__ with the model state.
        """
        for subclass in PieceBaseState.__subclasses__():
            if subclass.__state__ == self.piece.state:
                return subclass()

        raise Exception('Invalid state')

    def to_domain(self) -> Piece:
        """
        Convert to domain
        """
        if isinstance(self.piece, Piece):
            return self.piece

        return Piece.new({
            'path': self.piece.path,
            'name': self.piece.name,
            'extension': self.piece.image,
            'state': self._map_model_state_to_domain(),
        }, just(Guid(self.piece.id))).unwrap()

    def to_model(self):
        """
        Convert to model
        """
        return PieceModel(
            id=self.piece.id,
            name=self.piece.name,
            image=self.piece.image,
            segmented=self.piece.segmented,
            skeletonized=self.piece.skeletonized,
            created_at=self.piece.created_at,
            updated_at=self.piece.updated_at
        )
