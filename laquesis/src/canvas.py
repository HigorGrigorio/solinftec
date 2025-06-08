# -----------------------------------------------------------------------------
# (C) 2025 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from typing import Any, Dict, List, Tuple
import numpy as np

class Canvas:
    """
    The Canvas class is a shared
    space in memory used for manipulation of images in the runtime of the application.
    """

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self._drawn = False

    def draw(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """
        Draw a pixel in the canva.

        Parameters
        ----------
        x : int
            The x position of the pixel.
        y : int
            The y position of the pixel.
        color : Tuple[int, int, int]
            The color of the pixel in RGB format.
        """
        self.image[y, x] = color
        self._drawn = True

    def clear(self) -> None:
        """
        Clear the canva.
        """
        self.image = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self._drawn = False

    def is_drawn(self) -> bool:
        """
        Check if the canva was drawn.

        Returns
        -------
        bool
            True if the canva was drawn, False otherwise.
        """
        return self._drawn

    def get_image(self) -> np.ndarray:
        """
        Get the image of the canva.

        Returns
        -------
        np.ndarray
            The image of the canva.
        """
        return self.image

    def save(self, path: str) -> None:
        """
        Save the image of the canva in a file.

        Parameters
        ----------
        path : str
            The path to save the image.
        """
        from PIL import Image
        image = Image.fromarray(self.image)
        image.save(path)

    def open(self, path: str) -> None:
        """
        Open an image file in the canva.

        Parameters
        ----------
        path : str
            The path to the image file.
        """
        from PIL import Image
        image = Image.open(path)
        self.image = np.array(image)
        self.height, self.width = self.image.shape[:2]
        self

    def __repr__(self) -> str:
        return f'Canvas(width={self.width}, height={self.height})'

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Canvas) and self.width == other.width and self.height == other.height

    def __hash__(self) -> int:
        return hash((self.width, self.height))

    def __bool__(self) -> bool:
        return self.is_drawn()