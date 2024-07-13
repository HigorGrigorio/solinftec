# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from shared.logic import UnexpectedError


class CropAlreadySegmented(UnexpectedError):
    """
    CropAlreadySegmented is raised when a crop is already segmented
    """

    id: str
    """
    id is the crop id
    """

    def __init__(self, id: str) -> None:
        """
        Creates a new CropAlreadySegmented instance

        ----------
        Parameters
        ----------
        id : str
            The crop id
        """
        self.id = id
        super().__init__(f"Crop {id} is already segmented")
