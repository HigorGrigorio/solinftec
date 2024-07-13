# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from typing import List

from olympus.domain import WatchedList
from olympus.monads import Maybe

from modules.crop.domain import Crop


class Crops(WatchedList[Crop]):
    """
    Represents a list of crops
    """

    def compare(self, a: Crop, b: Crop) -> bool:
        """
        Compare two crops

        ----------
        Parameters
        ----------
        a : Crop
            The first crop
        b : Crop
            The second crop

        -------
        Returns
        -------
        bool
            True if the crops are equal, False otherwise
        """
        return a.id == b.id

    @classmethod
    def new(cls, crops: Maybe[List[Crop]] = Maybe.nothing()) -> 'Crops':
        """
        Creates a new Pieces instance

        ----------
        Parameters
        ----------
        crops : list[Crop]
            The crops list

        -------
        Returns
        -------
        Crops
            The Pieces instance
        """
        return cls(crops.get_or_else(lambda: []))
