# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache

from olympus.domain import Guid
from olympus.domain.events import trigger
from sqlalchemy.orm import Session

from config.database import get_db_connection
from infra.schemas.sqlalchemy import PieceModel
from modules.piece.domain import Piece
from modules.piece.infra.sqlalchemy.mappers.AlchemyPieceMapper import AlchemyPieceMapper
from modules.piece.repos import IPieceRepo


class PieceRepo(IPieceRepo):
    """
    PieceRepo is the piece repository
    """

    session: Session

    def __init__(self, session: Session) -> None:
        """
        Creates a new PieceRepo instance

        ----------
        Parameters
        ----------
        session: Session
            the database session manager
        """
        self.session = session

    @classmethod
    @lru_cache
    def instance(cls, session: Session | None = None) -> 'PieceRepo':
        """
        instance returns a new PieceRepo instance

        ----------
        Parameters
        ----------
        session: Session | None
            the database session manager

        -------
        Returns
        -------
        PieceRepo
            a new PieceRepo instance
        """
        return cls(session or get_db_connection())

    def get(self, id: Guid) -> Piece | None:
        """
        get returns a piece by its id

        ----------
        Parameters
        ----------
        id: Guid
            the piece id

        -------
        Returns
        -------
        Piece
            the piece
        """
        model = self.session.get(PieceModel, id.value)

        if model is None:
            return None

        return AlchemyPieceMapper.to_domain(model)

    def create(self, piece: Piece) -> Piece:
        """
        create creates a new piece

        ----------
        Parameters
        ----------
        piece: Piece
            the piece to be created
        """
        model = AlchemyPieceMapper.to_model(piece)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        trigger(piece.get_events())
        return piece

    def update(self, piece: Piece) -> Piece:
        """
        update updates a piece

        ----------
        Parameters
        ----------
        piece: Piece
            the piece to be updated
        """
        model = AlchemyPieceMapper.to_model(piece)
        self.session.merge(model)
        self.session.commit()
        trigger(piece.get_events())
        return piece
