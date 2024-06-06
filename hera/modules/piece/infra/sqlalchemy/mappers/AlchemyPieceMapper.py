# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from typing import Type

from olympus.domain import Guid
from olympus.monads import Maybe
from olympus.monads.maybe import just

from infra.schemas.sqlalchemy import PieceModel
from modules.core.domain import File
from modules.core.domain.File import FileProps
from modules.piece.domain import Piece, BasePieceState
from modules.piece.domain.PieceContext import PieceProps


class AlchemyPieceMapper:
    """
    Piece Mapper
    """

    def __init__(self, piece: Piece | PieceModel):
        self.piece = piece

    @staticmethod
    def _map_model_state_to_domain(piece: Type[PieceModel]) -> BasePieceState:
        """
        Map the piece state to domain state. This function uses
        BasePlotState.__subclasses__() to get all BasePlotState
        subclasses and then compare __state__ with the piece state.
        """
        for subclass in BasePieceState.__subclasses__():
            if subclass.__state__ == piece.state:
                return subclass()

        raise Exception('Invalid state')

    @staticmethod
    def to_domain(piece: Type[PieceModel]) -> Piece:
        """
        Convert to domain

        ----------
        Parameters
        ----------
        piece: Type[PieceModel]
            The model

        -------
        Returns
        -------
        Piece
            The domain
        """

        return Piece(
            AlchemyPieceMapper._map_model_state_to_domain(piece),
            PieceProps(
                file=File(
                    FileProps(
                        name=piece.name,
                        path=piece.path,
                        extension=piece.extension
                    )
                ),
                plot_id=just(piece.plot_id),
                created_at=piece.created_at.isoformat(),
                updated_at=piece.updated_at.isoformat()
            ),
            just(Guid(piece.id))
        )

    def to_model(self):
        """
        Convert to piece
        """
        file = self.piece.get_file()

        return PieceModel(
            id=self.piece.id,
            name=file.get_name(),
            path=file.get_path(),
            extension=file.get_extension(),
            created_at=self.piece.created_at,
            updated_at=self.piece.updated_at
        )
