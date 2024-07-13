# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc

from olympus.domain import Guid

from modules.crop.domain import Crop


class IGetCropRepo(abc.ABC):
    """
    Crop Repository Interface

    This interface is used to get a Crop.
    """

    @abc.abstractmethod
    def get(self, id: Guid) -> Crop:
        """
        Get a Crop

        ----------
        Parameters
        ----------
        id : Guid
            Crop id

        -------
        Returns
        -------
        Crop
            The Crop
        """
        pass
