# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod

from modules.plot.domain import Plot


class IUpdatePlotRepo(ABC):
    """
    Update Plot Repository Interface
    """
    @abstractmethod
    def update(self, plot: Plot) -> Plot:
        """
        Update a plot

        ----------
        Parameters
        ----------
        plot : Plot
            Plot to be updated

        -------
        Returns
        -------
        Plot
            The updated plot

        """
        raise NotImplementedError
