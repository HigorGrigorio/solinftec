# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from fastapi import Depends
from olympus.domain import IUseCase, Guid
from olympus.monads import Either
from shared.logic import UnexpectedError

from modules.piece.repos import IPieceRepo
from modules.plot.repos import IPlotRepo
from .CreatePieceDTO import CreatePieceDTO

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
            plot_id = Guid.from_string(dto.plot)
            plot = self.plot_repo.get(plot_id)

            if plot is None:
                return Either.left(UnexpectedError('Plot not found'))

            piece = self.piece_repo.create()

            return Either.right(piece.id.value)
        except Exception as err:
            return Either.left(UnexpectedError(err))
