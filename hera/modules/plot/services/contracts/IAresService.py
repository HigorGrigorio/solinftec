# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import abc
from typing import TypedDict


class CropPlotModel(TypedDict):
    """
    CropPlotModel is the data transfer object for CropPlotController

    Attributes:
        id (str): The plot id to be processed
        path (str): The plot to be processed
    """

    id: str
    path: str


class IAresService(abc.ABC):
    @abc.abstractmethod
    def crop(self, plot: CropPlotModel) -> None:
        ...
