# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod

from olympus.domain import Guid

from modules.plot.domain import Plot


class IGetPlotRepo(ABC):
    """
    Get Plot Repository Interface
    """

    @abstractmethod
    def get(self, id: Guid) -> Plot | None:
        """
        Get a plot by id

        ----------
        Parameters
        ----------
        id : Guid
            Plot id

        -------
        Returns
        -------
        Plot | None
            The plot or None if not found
        """
        raise NotImplementedError
