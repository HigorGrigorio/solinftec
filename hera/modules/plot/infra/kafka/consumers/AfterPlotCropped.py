# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from logging import Logger

from confluent_kafka import Consumer
from fastapi import Depends
from pydantic import BaseModel
from shared.infra import ConsumerLoop

from config.kafka import get_consumer
from config.log import get_logger
from modules.plot.infra.sqlalchemy.repos import PlotRepo
from modules.plot.usecases.mark_plot_as_cropped import CropPlotUseCase, CropPlotDTO


class AfterPlotCroppedModel(BaseModel):
    id: str


class AfterPlotCropped(ConsumerLoop[AfterPlotCroppedModel]):
    __topic__ = ['hera.crop-succeeded']

    model: AfterPlotCroppedModel
    mark_as_cropped: CropPlotUseCase

    def __init__(
            self,
            usecase: CropPlotUseCase = CropPlotUseCase(
                repo=PlotRepo.instance()
            ),
            consumer: Consumer = get_consumer('after-plot-cropped'),
            logger: Logger = get_logger()
    ) -> None:
        super().__init__(consumer, logger)
        self.mark_as_cropped = usecase

    def _map_dto(self):
        return CropPlotDTO(id=self.model.id)

    def _get_model_class(self) -> type[AfterPlotCroppedModel]:
        return AfterPlotCroppedModel

    def handle(self, model: AfterPlotCroppedModel) -> None:
        self.logger.info(f'Plot {model.id} was cropped.')
        self.model = model
        self.mark_as_cropped.execute(self._map_dto())
