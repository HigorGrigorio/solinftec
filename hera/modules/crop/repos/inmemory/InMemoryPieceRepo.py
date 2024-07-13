# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from typing import Dict

from olympus.domain import Guid

from modules.crop.domain import Crop
from modules.crop.repos import ICropRepo


class InMemoryCropRepo(ICropRepo):
    """
    InMemory Crop Repository
    """

    def __init__(self):
        self._pieces: Dict[str, Crop] = dict[str, Crop]()

    def create(self, crop: Crop):
        self._pieces[crop.id.value] = crop
        return crop

    def update(self, crop: Crop):
        self._pieces[crop.id] = crop
        return crop

    def get(self, id: Guid):
        return self._pieces.get(id.value)
