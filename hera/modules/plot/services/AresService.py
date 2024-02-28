# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from pydantic import json

from config.kafka import get_producer
from .contracts.IAresService import IAresService
from ..domain import Plot


class AresService(IAresService):
    def __init__(self, producer=get_producer('ares')) -> None:
        self.producer = producer

    async def crop(self, plot: Plot) -> None:
        data = {
            'id': plot.id,
            'path': plot.path,
        }
        self.producer.produce('add_plot_to_crop', json.dumps(data).encode('utf-8'))
        self.producer.poll()
        self.producer.flush()
