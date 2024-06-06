# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class SegmentPieceDTO(BaseModel):
    """
    SegmentPieceDTO is the data transfer object to segment a piece
    """

    id: str
    """
    id is the piece id to be segmented
    """
