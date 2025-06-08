# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from fastapi import Depends
from olympus.domain import IUseCase, Guid
from olympus.monads import Either, Result
from olympus.monads.maybe import just
from shared.logic import UnexpectedError

from modules.core.domain import File
from modules.core.domain.File import FileProps
from modules.crop.repos import ICropRepo
from modules.plot.repos import IPlotRepo
from . import RelatedPlotNotFoundError
from .CreateCropDTO import CreateCropDTO
from ...domain import Crop

Response = Either[UnexpectedError, str]


class CreateCropUseCase(IUseCase[CreateCropDTO, Response]):
    def __init__(
            self,
            plot_repo: IPlotRepo = Depends(),
            crop_repo: ICropRepo = Depends(),
    ):
        """
        Create Crop Use Case

        This use case is used to create a Crop.

        ----------
        Parameters
        ----------
        plot_repo : IPlotRepo
            Plot repository
        crop_repo : ICropRepo
            Crop repository
        """
        self.plot_repo = plot_repo
        self.piece_repo = crop_repo

    def _create_file(self, dto: CreateCropDTO) -> Result[File]:
        """
        Creates a file from the dto.

        ----------
        Parameters
        ----------
        dto : CreateCropDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Result[File]
            Either a File or a UnexpectedError.
        """

        # split the path into name and extension
        path, name = dto.path.rsplit('\\', 1)

        # split the name into name and extension
        name, extension = name.rsplit('.', 1)

        return Result.ok(
            File(FileProps(
                path=path,
                name=name,
                extension=extension,
            ))
        )

    def _create_piece(self, file: File, plot_id: str) -> Result[Crop] | RelatedPlotNotFoundError:
        """
        Creates a crop from the file and plot_id.

        ----------
        Parameters
        ----------
        file : File
            The file
        plot_id : str
            The plot id

        -------
        Returns
        -------
        Result[Crop]
            Either a Crop or a UnexpectedError.
        """
        plot_id: Guid = Guid(plot_id)

        if self.plot_repo.get(plot_id) is None:
            return RelatedPlotNotFoundError(str(plot_id))

        return Crop.new({
            'file': file,
            'plot_id': just(plot_id),
            'created_at': None,
            'updated_at': None,
        })

    def _persist_piece(self, crop: Crop) -> Result[Crop]:
        """
        Persists the crop.

        ----------
        Parameters
        ----------
        crop : Crop
            The crop

        -------
        Returns
        -------
        Result[Crop]
            Either a Crop or a UnexpectedError.
        """
        self.piece_repo.create(crop)

        return Result.ok(crop)

    def execute(self, dto: CreateCropDTO) -> Response:
        """
        Executes the use case.

        ----------
        Parameters
        ----------
        dto : CreateCropDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Response
            Either a UnexpectedError or a str.
        """
        try:
            result_piece = self._create_file(dto) \
                .bind(lambda f: self._create_piece(f, dto.plot_id)) \
                .bind(self._persist_piece)

            if result_piece.is_err:
                return Either.left(result_piece)

            plot = result_piece.value

            return Either.right(plot.get_id().value)
        except Exception as err:
            return Either.left(UnexpectedError(err))
