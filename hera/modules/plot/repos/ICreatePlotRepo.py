# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from abc import ABC, abstractmethod

from modules.plot.domain import Plot


class ICreatePlotRepo(ABC):
    """
    Create Plot Repository Interface
    """
    @abstractmethod
    def create(self, plot: Plot) -> Plot:
        """
        Create a plot

        ----------
        Parameters
        ----------
        plot : Plot
            Plot to be created

        -------
        Returns
        -------
        Plot
            The created plot
        """
        raise NotImplementedError
