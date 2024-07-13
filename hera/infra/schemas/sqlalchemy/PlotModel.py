# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship

from .BaseModel import BaseModel


class PlotModel(BaseModel):
    """
    PlotModel is the SQLAlchemy ORM piece for the Plot entity. This class
    is responsible for mapping Plot entity to database piece.

    -----------
    Attributes
    ----------
    id: str
        Plot id
    name: str
        Plot name
    extension: str
        Plot extension
    path: str
        Plot path
    description: str
        Plot description
    state: int
        Plot state
    """

    __tablename__ = 'plots'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    path = Column(String, nullable=False)
    description = Column(String, nullable=False)

    state = Column(Enum('canceled', 'cropped', 'failed', 'finished', 'queued', 'rescaled', 'restored', 'segmented',
                        'skeletonized', name='plot_state'), nullable=False)
    """
    The state of the plot
    """

    crops = relationship('CropModel', lazy='joined', back_populates='plot')
    """
    The plot crops
    """