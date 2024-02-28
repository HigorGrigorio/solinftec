# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from sqlalchemy import Column, String, Integer

from infra.schemas.sqlalchemy.BaseModel import BaseModel


class PlotModel(BaseModel):
    """
    PlotModel is the SQLAlchemy ORM model for the Plot entity. This class
    is responsible for mapping Plot entity to database model.

    -----------
    Attributes:

        id (str): Plot id.
        name (str): Plot name.
        extension (str): Plot extension.
        path (str): Plot path.
        description (str): Plot description.
        created_at (datetime): Plot creation date.
        updated_at (datetime): Plot update date.
        state (int): Plot state.
    """

    __tablename__ = 'plots'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    extension = Column(String, nullable=False)
    path = Column(String, nullable=False)
    description = Column(String, nullable=False)
    state = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
