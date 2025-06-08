# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain.events import EventHandler, bind

from config.log import get_logger
from modules.plot.domain.events import PlotCropped
from modules.plot.infra.sqlalchemy.repos import PlotRepo
from modules.plot.services import LaquesisService
from modules.plot.services.contracts import ILaquesisService


class AddPlotToSegmentationQueue(EventHandler):
    def __init__(self, logger=get_logger(), plot_repo: PlotRepo = PlotRepo.instance(),
                 segment_service: ILaquesisService = LaquesisService()) -> None:
        super().__init__()
        self.logger = logger
        self.plot_repo = plot_repo
        self.segment_service = segment_service

    def setup(self):
        bind(PlotCropped, self.add_plot_segmentation)

    def load_crops(self, id: str):
        return self.plot_repo.get_crops(id)

    def add_plot_segmentation(self, event: PlotCropped):
        crops = self.load_crops(event.plot.id.value)

        for crop in crops:
            self.logger.info(f"Adding crop {crop.id} to segmentation queue.")
            # Add crop to segmentation queue
            self.segment_service.segment(crop)


