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
from modules.piece.repos import IPieceRepo
from modules.plot.repos import IPlotRepo
from . import RelatedPlotNotFoundError
from .CreatePieceDTO import CreatePieceDTO
from ...domain import Piece

Response = Either[UnexpectedError, str]


class CreatePieceUseCase(IUseCase[CreatePieceDTO, Response]):
    def __init__(
            self,
            plot_repo: IPlotRepo = Depends(),
            crop_repo: IPieceRepo = Depends(),
    ):
        """
        Create Piece Use Case

        This use case is used to create a Piece.

        ----------
        Parameters
        ----------
        plot_repo : IPlotRepo
            Plot repository
        crop_repo : IPieceRepo
            Piece repository
        """
        self.plot_repo = plot_repo
        self.piece_repo = crop_repo

    def _create_file(self, dto: CreatePieceDTO) -> Result[File]:
        """
        Creates a file from the dto.

        ----------
        Parameters
        ----------
        dto : CreatePieceDTO
            The use case data transfer object.

        -------
        Returns
        -------
        Result[File]
            Either a File or a UnexpectedError.
        """
        return Result.ok(
            File(FileProps(
                path=dto.path,
                name=dto.name,
                extension=dto.extension,
            ))
        )

    def _create_piece(self, file: File, plot_id: str) -> Result[Piece] | RelatedPlotNotFoundError:
        """
        Creates a piece from the file and plot_id.

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
        Result[Piece]
            Either a Piece or a UnexpectedError.
        """
        plot_id: Guid = Guid(plot_id)

        if self.plot_repo.get(plot_id) is None:
            return RelatedPlotNotFoundError(str(plot_id))

        return Piece.new({
            'file': file,
            'plot_id': just(plot_id),
        })

    def _persist_piece(self, piece: Piece) -> Result[Piece]:
        """
        Persists the piece.

        ----------
        Parameters
        ----------
        piece : Piece
            The piece

        -------
        Returns
        -------
        Result[Piece]
            Either a Piece or a UnexpectedError.
        """
        self.piece_repo.create(piece)

        return Result.ok(piece)

    def execute(self, dto: CreatePieceDTO) -> Response:
        """
        Executes the use case.

        ----------
        Parameters
        ----------
        dto : CreatePieceDTO
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
