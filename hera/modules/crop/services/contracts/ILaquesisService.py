# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc


class ILaquesisService(abc.ABC):
    """
    ILaquesisService is the service that segments the clippings, saving the relationship
    between the segmented image and its respective field in the database.
    """

    @abc.abstractmethod
    def segment(self, crop_id: str) -> None:
        """
        segment is responsible for segmenting the crop.

        ----------
        Parameters
        ----------
        crop_id : str
            The crop id to be segmented.
        """
        ...
