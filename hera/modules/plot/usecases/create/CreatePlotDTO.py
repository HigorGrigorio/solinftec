# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from pydantic import BaseModel


class CreatePlotDTO(BaseModel):
    name: str
    extension: str
    path: str
    description: str = ''
    buffer: bytes
