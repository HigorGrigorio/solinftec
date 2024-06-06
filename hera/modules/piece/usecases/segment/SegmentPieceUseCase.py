# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from fastapi import Depends
from olympus.domain import IUseCase
from olympus.monads import Either, Result
from shared.logic import UnexpectedError

from modules.piece.usecases.errors import PieceNotFound
from .SegmentPieceDTO import SegmentPieceDTO
from .SegmentPieceError import PieceAlreadySegmented
from ...domain import Piece
from ...repos import IPieceRepo
from ...services.contracts.ILaquesisService import ILaquesisService

Response = Either[UnexpectedError | PieceNotFound | PieceAlreadySegmented, None]


class SegmentPieceUseCase(IUseCase[SegmentPieceDTO, Response]):
    """
    SegmentPieceUseCase is responsible to mark a piece as segmented
    """

    DTO = SegmentPieceDTO
    """
    DTO is the use case data transfer object
    """

    dto: DTO
    """
    dto is the use case data transfer object
    """

    service: ILaquesisService
    """
    service is the Laquesis service
    """

    repo: IPieceRepo
    """
    repo is the piece repository
    """

    def __init__(self, repo: IPieceRepo, service: ILaquesisService = Depends()):
        """
        Creates a new SegmentPieceUseCase instance

        ----------
        Parameters
        ----------
        repo : IPieceRepo
            The piece repository
        service : ILaquesisService
            Laquesis service
        """
        self.repo = repo
        self.service = service

    def _load_piece(self) -> Result[Piece] | PieceNotFound:
        """
        Loads the piece from the dto.

        ----------
        Parameters
        ----------
        dto : SegmentPieceDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Result
            Either a Piece or a PieceNotFound.
        """

        piece_id = self.dto.piece_id

        if (piece := self.repo.get(piece_id)) is None:
            return PieceNotFound(self.dto.piece_id)

        return Result.ok(piece)

    def _segment_piece(self, piece: Piece) -> Result[None] | PieceAlreadySegmented:
        """
        Segments the piece.

        ----------
        Parameters
        ----------
        piece : Piece
            The piece to be segmented.

        -------
        Returns
        -------
        Result
            Either a None or a PieceAlreadySegmented.
        """
        if piece.is_segmented():
            return PieceAlreadySegmented(piece.id)

        self.service.segment(piece)

        return Result.ok(None)

    def execute(self, dto: SegmentPieceDTO) -> Response:
        """
        Executes the use case

        ----------
        Parameters
        ----------
        dto : SegmentPieceDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Response
            Either a UnexpectedError, PieceNotFound, PieceAlreadySegmented or None.
        """
        try:
            self.dto = dto

            # load the piece and subscribe the piece to
            # the segment queue
            result = self._load_piece() \
                .bind(self._segment_piece)

            if result.is_ok:
                return Either.right(None)

            return Either.left(result)
        except Exception as e:
            return Either.left(UnexpectedError(str(e)))
