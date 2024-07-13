# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from fastapi import Depends
from olympus.domain import IUseCase
from olympus.monads import Either, Result
from shared.logic import UnexpectedError

from modules.crop.usecases.errors import CropNotFound
from .SegmentCropDTO import SegmentCropDTO
from .SegmentPieceError import CropAlreadySegmented
from ...domain import Crop
from ...repos import ICropRepo
from ...services.contracts.ILaquesisService import ILaquesisService

Response = Either[UnexpectedError | CropNotFound | CropAlreadySegmented, None]


class SegmentCropUseCase(IUseCase[SegmentCropDTO, Response]):
    """
    SegmentCropUseCase is responsible to mark a crop as segmented
    """

    DTO = SegmentCropDTO
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

    repo: ICropRepo
    """
    repo is the crop repository
    """

    def __init__(self, repo: ICropRepo, service: ILaquesisService = Depends()):
        """
        Creates a new SegmentCropUseCase instance

        ----------
        Parameters
        ----------
        repo : ICropRepo
            The crop repository
        service : ILaquesisService
            Laquesis service
        """
        self.repo = repo
        self.service = service

    def _load_piece(self) -> Result[Crop] | CropNotFound:
        """
        Loads the crop from the dto.

        ----------
        Parameters
        ----------
        dto : SegmentCropDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Result
            Either a Crop or a CropNotFound.
        """

        piece_id = self.dto.piece_id

        if (crop := self.repo.get(piece_id)) is None:
            return CropNotFound(self.dto.piece_id)

        return Result.ok(crop)

    def _segment_piece(self, crop: Crop) -> Result[None] | CropAlreadySegmented:
        """
        Segments the crop.

        ----------
        Parameters
        ----------
        crop : Crop
            The crop to be segmented.

        -------
        Returns
        -------
        Result
            Either a None or a CropAlreadySegmented.
        """
        if crop.is_segmented():
            return CropAlreadySegmented(crop.id)

        self.service.segment(crop)

        return Result.ok(None)

    def execute(self, dto: SegmentCropDTO) -> Response:
        """
        Executes the use case

        ----------
        Parameters
        ----------
        dto : SegmentCropDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Response
            Either a UnexpectedError, CropNotFound, CropAlreadySegmented or None.
        """
        try:
            self.dto = dto

            # load the crop and subscribe the crop to
            # the segment queue
            result = self._load_piece() \
                .bind(self._segment_piece)

            if result.is_ok:
                return Either.right(None)

            return Either.left(result)
        except Exception as e:
            return Either.left(UnexpectedError(str(e)))
