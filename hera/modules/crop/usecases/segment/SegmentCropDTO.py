# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class SegmentCropDTO(BaseModel):
    """
    SegmentCropDTO is the data transfer object to segment a crop
    """

    id: str
    """
    id is the crop id to be segmented
    """
