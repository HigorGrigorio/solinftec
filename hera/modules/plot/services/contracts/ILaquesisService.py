# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc

from modules.crop.domain import Crop


class ILaquesisService(abc.ABC):
    """
    ILaquesisService is the service that segments the clippings, saving the relationship
    between the segmented image and its respective field in the database.
    """

    @abc.abstractmethod
    def segment(self, crop: Crop) -> None:
        """
        segment is responsible for segmenting the crop.

        ----------
        Parameters
        ----------
        crop : Crop
            The crop id to be segmented.
        """
        ...
