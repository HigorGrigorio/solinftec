# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache

from olympus.domain import Guid
from olympus.domain.events import trigger
from sqlalchemy.orm import Session

from config.database import get_session
from infra.schemas.sqlalchemy import CropModel
from modules.crop.domain import Crop
from modules.crop.infra.sqlalchemy.mappers.AlchemyCropMapper import AlchemyCropMapper
from modules.crop.repos import ICropRepo


class CropRepo(ICropRepo):
    """
    CropRepo is the crop repository
    """

    session: Session

    def __init__(self, session: Session) -> None:
        """
        Creates a new CropRepo instance

        ----------
        Parameters
        ----------
        session: Session
            the database session manager
        """
        self.session = session

    @classmethod
    @lru_cache
    def instance(cls, session: Session | None = None) -> 'CropRepo':
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
        CropRepo
            a new PieceRepo instance
        """
        if session is None:
            with get_session() as session:
                instance = cls(session)
        else:
            instance = cls(session)
        return instance

    def get(self, id: Guid) -> Crop | None:
        """
        get returns a crop by its id

        ----------
        Parameters
        ----------
        id: Guid
            the crop id

        -------
        Returns
        -------
        Crop
            the crop
        """
        model = self.session.get(CropModel, id.value)

        if model is None:
            return None

        return AlchemyCropMapper.to_domain(model)

    def create(self, crop: Crop) -> Crop:
        """
        create creates a new crop

        ----------
        Parameters
        ----------
        crop: Crop
            The crop to be created
        """
        model = AlchemyCropMapper.to_model(crop)

        try:
            # Add the model to the session
            self.session.add(model)
            self.session.flush()  # Ensure constraints are checked
            self.session.commit()
            self.session.refresh(model)  # Synchronize the state
        except Exception as e:
            self.session.rollback()

            raise  # Reraise the exception

        # Trigger events after successful commit
        trigger(crop.get_events())

        return AlchemyCropMapper.to_domain(model)  # Optionally map back to domain

    def update(self, crop: Crop) -> Crop:
        """
        update updates a crop

        ----------
        Parameters
        ----------
        crop: Crop
            the crop to be updated
        """
        model = AlchemyCropMapper.to_model(crop)
        self.session.merge(model)
        self.session.commit()
        trigger(crop.get_events())
        return crop
