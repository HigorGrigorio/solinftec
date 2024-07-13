# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import sqlalchemy
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel
from .PlotModel import PlotModel


class CropModel(BaseModel):
    """
    Crop Model Schema

    ---------
    Attributes
    ---------
    id: int
        Crop id
    name: str
        Crop name
    path: str
        Crop path
    plot_id: int
        Crop plot id
    plot: PlotModel
        Crop plot

    """

    __tablename__ = 'crops'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    path = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)
    plot_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey(PlotModel.id), nullable=False)
    extension = sqlalchemy.Column(sqlalchemy.String(255), nullable=False)

    plot = relationship('PlotModel', back_populates='crops')

    state = sqlalchemy.Column(
        sqlalchemy.Enum('failed', 'finished', 'queued', 'restored', 'segmented', 'skeletonized',
                        name='piece_state'),
    )


