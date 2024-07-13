# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.domain.events import EventHandler, bind

from modules.crop.domain.events import CropSegmented
from modules.crop.infra.sqlalchemy.repos.CropRepo import CropRepo
from modules.crop.services.LaquesisService import LaquesisService
from modules.crop.usecases.segment import SegmentCropUseCase


class AddCropToSegmentQueue(EventHandler):
    """
    AddCropToSegmentQueue is responsible for adding a crop to the segment queue
    """

    segment_piece: SegmentCropUseCase
    """
    segment_piece is the segment crop use case
    """

    def __init__(
            self,
            segment_piece: SegmentCropUseCase = SegmentCropUseCase(
                repo=CropRepo.instance(),
                service=LaquesisService.instance()
            )

    ) -> None:
        super().__init__()
        self.segment_piece = segment_piece

    def setup(self):
        """
        Set up the event handler
        """

        bind(CropSegmented, self.after_piece_segmented)

    def after_piece_segmented(self, event: CropSegmented):
        """
        after_piece_segmented is the method called after a crop is segmented
        """

        data: SegmentCropUseCase.DTO = SegmentCropUseCase.DTO({
            'id': event.crop.id.value
        })

        self.segment_piece.execute(data)
