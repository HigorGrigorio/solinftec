# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import sqlalchemy
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel
from .PlotModel import PlotModel


class PieceModel(BaseModel):
    """
    Piece Model Schema

    ---------
    Attributes
    ---------
    id: int
        Piece id
    name: str
        Piece name
    path: str
        Piece path
    plot_id: int
        Piece plot id
    plot: PlotModel
        Piece plot

    """

    __tablename__ = 'pieces'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    plot_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(PlotModel.id), nullable=False)
    extension = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    plot = relationship('PlotModel', back_populates='pieces')

    state = sqlalchemy.Column(
        sqlalchemy.Enum('failed', 'finished', 'queued', 'restored', 'segmented', 'skeletonized',
                        name='piece_state'),
    )


