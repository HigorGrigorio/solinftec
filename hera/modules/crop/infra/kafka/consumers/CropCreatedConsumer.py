# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from logging import Logger

from confluent_kafka import Consumer
from pydantic import BaseModel
from shared.infra import ConsumerLoop

from config.kafka import get_consumer
from config.log import get_logger
from modules.core.domain import File
from modules.crop.infra.sqlalchemy.repos.CropRepo import CropRepo
from modules.crop.usecases.create import CreateCropUseCase, CreateCropDTO
from modules.plot.infra.sqlalchemy.repos import PlotRepo


class CropCreatedModel(BaseModel):
    path: str
    parent: str


class CropCreatedConsumer(ConsumerLoop[CropCreatedModel]):
    __topic__ = ['hera.crop-created']

    model: CropCreatedModel
    create_crop: CreateCropUseCase

    def __init__(
            self,
            create_crop: CreateCropUseCase = CreateCropUseCase(
                plot_repo=PlotRepo.instance(),
                crop_repo=CropRepo.instance()
            ),
            consumer: Consumer = get_consumer('crop-created'),
            logger: Logger = get_logger()
    ):
        super().__init__(consumer, logger)
        self.create_crop = create_crop

    def _get_model_class(self) -> type[CropCreatedModel]:
        return CropCreatedModel

    def _map_dto(self):
        return CreateCropDTO(path=self.model.path, plot_id=self.model.parent)

    def handle(self, model: CropCreatedModel) -> None:
        self.model = model
        self.create_crop.execute(self._map_dto())
