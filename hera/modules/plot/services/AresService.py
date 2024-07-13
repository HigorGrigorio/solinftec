# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import json

from config.kafka import get_producer
from .contracts.IAresService import IAresService, CropPlotModel


class AresService(IAresService):
    def __init__(self, producer=get_producer('ares')) -> None:
        self.producer = producer

    async def crop(self, plot: CropPlotModel) -> None:
        data = {
            'id': plot['id'],
            'path': plot['path'],
        }
        self.producer.produce('hera.plot-to-crops', json.dumps(data).encode('utf-8'))
        self.producer.poll()
        self.producer.flush()
