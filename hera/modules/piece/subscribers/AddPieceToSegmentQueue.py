# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from olympus.domain.events import EventHandler, bind

from modules.piece.domain.events import PieceSegmented
from modules.piece.infra.sqlalchemy.repos.PieceRepo import PieceRepo
from modules.piece.services.LaquesisService import LaquesisService
from modules.piece.usecases.segment import SegmentPieceUseCase


class AddPieceToSegmentQueue(EventHandler):
    """
    AddPieceToSegmentQueue is responsible for adding a piece to the segment queue
    """

    segment_piece: SegmentPieceUseCase
    """
    segment_piece is the segment piece use case
    """

    def __init__(
            self,
            segment_piece: SegmentPieceUseCase = SegmentPieceUseCase(
                repo=PieceRepo.instance(),
                service=LaquesisService.instance()
            )

    ) -> None:
        super().__init__()
        self.segment_piece = segment_piece

    def setup(self):
        """
        Set up the event handler
        """

        bind(PieceSegmented, self.after_piece_segmented)

    def after_piece_segmented(self, event: PieceSegmented):
        """
        after_piece_segmented is the method called after a piece is segmented
        """

        data: SegmentPieceUseCase.DTO = SegmentPieceUseCase.DTO({
            'id': event.piece.id.value
        })

        self.segment_piece.execute(data)
