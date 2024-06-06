# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from datetime import datetime

from sqlalchemy import Column, DateTime

from .EntityMeta import EntityMeta


class BaseModel(EntityMeta):
    """
    Base Model Schema

    This class is responsible for mapping the common attributes of all entities
    to database piece.
    """
    __abstract__ = True
    __table_args__ = {'extend_existing': True}

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
