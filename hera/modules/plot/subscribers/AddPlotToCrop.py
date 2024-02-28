# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain.events import EventHandler, bind

from config.log import get_logger
from modules.plot.domain.events import PlotCreated
from modules.plot.services import AresService
from modules.plot.services.contracts import IAresService


class AddPlotToCrop(EventHandler):

    def __init__(self, service: IAresService = AresService(), logger=get_logger()) -> None:
        super().__init__()
        self.logger = logger
        self.service = service

    def setup(self):
        bind(PlotCreated, self.on_state_changed)

    def on_state_changed(self, event: PlotCreated):
        self.logger \
            .log(10, msg=f'Plot {event.plot.id} added to crop queue')


