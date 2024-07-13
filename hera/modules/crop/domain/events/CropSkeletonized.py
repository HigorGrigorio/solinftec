# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import Guid
from olympus.domain.events import DomainEvent

from modules.crop.domain import Crop


class CropSkeletonized(DomainEvent):
    """
    Emitted when a crop is skeletonized
    """
    crop: Crop

    def __init__(self, crop: Crop):
        super().__init__()
        self.crop = crop

    def get_aggregate_id(self) -> Guid:
        """
        Get the aggregate id

        --------
        Returns
        --------
        Guid
            The aggregate id
        """
        return self.crop.id
