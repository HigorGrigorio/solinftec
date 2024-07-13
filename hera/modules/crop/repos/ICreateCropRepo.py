# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from abc import abstractmethod, ABC

from modules.crop.domain import Crop


class ICreateCropRepo(ABC):
    """
    Crop Repository Interface

    This interface is used to create a Crop.
    """

    @abstractmethod
    def create(self, crop: Crop) -> Crop:
        """
        Create a Crop

        ----------
        Parameters
        ----------
        crop : Crop
            Crop to be created

        -------
        Returns
        -------
        Crop
            The created Crop
        """
        ...
