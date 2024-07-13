# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from shared.logic import UnexpectedError


class CropNotFound(UnexpectedError):
    """
    CropNotFound is raised when the crop is not found
    """

    """
    id: str
        The crop id that was not found
    """
    id: str

    def __init__(self, id: str) -> None:
        super().__init__(f"Crop {id} not found")
        self.id = id
