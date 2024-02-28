# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import Guid
from olympus.domain.events import DomainEvent

from modules.plot.domain import PlotContext, BasePlotState


class PlotStateChanged(DomainEvent):
    plot: PlotContext
    old: BasePlotState

    def __init__(self, plot: PlotContext, old: BasePlotState) -> None:
        super().__init__()
        self.plot = plot
        self.old = old

    def get_aggregate_id(self) -> Guid:
        return self.plot.id
