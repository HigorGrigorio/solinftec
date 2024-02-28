# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.domain.events import DomainEvent

from modules.plot.domain import Plot


class PlotCreated(DomainEvent):
    def __init__(self, plot: Plot) -> None:
        super().__init__()
        self.plot = plot

    def get_aggregate_id(self) -> str:
        return self.plot.id
