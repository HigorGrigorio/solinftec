# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from modules.plot.repos import IPlotRepo


class InMemoryPlotRepo(IPlotRepo):
    """
    In Memory Plot Repository

    This class is a mock of Plot Repository Interface, used for testing purposes.
    """

    def __init__(self):
        self._plots = []

    def create(self, plot):
        self._plots.append(plot)
        return plot

    def update(self, plot):
        self._plots = [p for p in self._plots if p.id != plot.id]
        self._plots.append(plot)
        return plot

    def get(self, plot_id):
        return next((p for p in self._plots if p.id == plot_id), None)
