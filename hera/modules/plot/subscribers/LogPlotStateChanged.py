# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain.events import (
    EventHandler,
    bind
)

from config.log import get_logger
from modules.plot.domain.events import PlotStateChanged


class LogPlotStateChanged(EventHandler):
    def __init__(self, logger=get_logger()) -> None:
        super().__init__()
        self.logger = logger

    def setup(self):
        bind(PlotStateChanged, self.on_state_changed)

    def on_state_changed(self, event: PlotStateChanged):
        self.logger \
            .set_context('PlotStateChanged') \
            .info(f'Plot {event.plot.id} changed from {event.old} to {event.plot.state}')
