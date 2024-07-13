# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc

from modules.crop.domain import Crop


class IUpdateCropRepo(abc.ABC):
    """
    Crop Repository Interface

    This interface is used to update a Crop.
    """

    @abc.abstractmethod
    def update(self, crop: Crop) -> Crop:
        """
        Update a Crop

        ----------
        Parameters
        ----------
        crop : Crop
            Crop to be updated

        -------
        Returns
        -------
        Crop
            The updated Crop
        """
        ...
