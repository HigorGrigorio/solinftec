# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from pydantic import BaseModel


class CreatePieceDTO(BaseModel):
    """
    Represents a piece data transfers object

    ---------
    Atributes
    ---------
    path : str
        The piece location
    name : str
        The piece filename
    extension : str
        The piece file extension
    plot : str
        The plot identifier that originated the pieceping
    """
    path: str
    name: str
    extension: str
    plot: str
