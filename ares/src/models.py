# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class CropMessage(BaseModel):
    id: str
    path: str
