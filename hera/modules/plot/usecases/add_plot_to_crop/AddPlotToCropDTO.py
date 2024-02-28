# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class AddPlotToCropDTO(BaseModel):
    """
    CropPlotDTO is the data transfer object for CropPlotUseCase

    Attributes:
        id (int): The plot id to be processed
    """

    id: str
