# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from uuid import uuid4

from fastapi import Depends
from olympus.domain import IUseCase
from olympus.monads import (Either, Result, Maybe)
from shared.logic import UnexpectedError

from modules.plot.domain import (
    File,
    Plot
)
from modules.plot.repos import IPlotRepo
from .CreatePlotDTO import CreatePlotDTO
from ...infra.sqlalchemy.repos import PlotRepo

Response = Either[UnexpectedError, str]


class CreatePlotUseCase(IUseCase[CreatePlotDTO, Response]):
    dto: CreatePlotDTO
    repo: IPlotRepo

    def __init__(self, repo: IPlotRepo = Depends(PlotRepo)) -> None:
        self.repo = repo

    def _store_plot(self, plot: Plot) -> Result[Plot]:
        try:
            return self.repo.create(plot)
        except Exception as e:
            return Result.fail(e)

    def _create_path_if_not_exists(self) -> Result[None]:
        try:
            import os
            if not os.path.exists(self.dto.path):
                os.makedirs(self.dto.path)
            return Result.ok(None)
        except Exception as e:
            return Result.fail(e)

    def _store_local_plot(self, plot) -> Result[Plot]:
        try:
            self._create_path_if_not_exists()

            # Store plot in local storage
            with open(f'{self.dto.path}/{plot.file.get_name()}.{self.dto.extension}', 'wb') as f:
                f.write(self.dto.buffer)

            return Result.ok(plot)
        except Exception as e:
            return Result.fail(e)

    def execute(self, dto: CreatePlotDTO) -> Response:
        self.dto = dto

        name = str(uuid4())

        def _make_plot(file: File) -> Result[Plot]:
            return

        plot = File.new(name, dto.path, dto.extension) \
            .bind(lambda f: Plot.new({
                'file': f,
                'description': dto.description,
                'pieces': Maybe.nothing(),
            })) \
            .bind(self._store_local_plot) \
            .bind(self._store_plot)

        if plot.is_err:
            return Either.left(UnexpectedError(plot.err()))

        return Either.right(str(plot.value.id))
