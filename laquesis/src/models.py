<<<<<<< HEAD
# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class SegmentationMessage(BaseModel):
    id: str
    path: str
=======
from pydantic import BaseModel


class TileMessage(BaseModel):
    id: str
    path: str
>>>>>>> 40a9ea28e2dcabcb9e10d8eff880dd9c2a536e17
