# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from pydantic import BaseModel


class CreateCropDTO(BaseModel):
    """
    Represents a crop data transfers object

    ---------
    Atributes
    ---------
    path : str
        The crop location
    name : str
        The crop filename
    extension : str
        The crop file extension
    plot_id : str
        The plot identifier that originated the pieceping
    """
    path: str
    plot_id: str
