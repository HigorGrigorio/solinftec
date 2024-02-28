# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from turtle import right

from fastapi import Depends
from olympus.domain import IUseCase, Guid
from olympus.monads import Either, Result, left, right
from shared.logic import UnexpectedError

from modules.plot.repos import IPlotRepo
from .CropPlotDTO import CropPlotDTO
from ...domain import Plot

Response = Either[UnexpectedError, None]


class CropPlotUseCase(IUseCase[CropPlotDTO, Response]):
    dto: CropPlotDTO

    def __init__(
            self,
            repo: IPlotRepo = Depends()
    ) -> None:
        super().__init__()
        self.repo = repo

    def _load_plot(self) -> Result[Plot]:
        id = Guid(self.dto.id)
        return Result.ok(self.repo.get(id))

    def _crop_plot(self, plot: Plot) -> Result[Plot]:
        try:
            return plot.crop()
        except Exception as e:
            return Result.fail(e)

    def _update_plot(self, plot: Plot) -> Result[Plot]:
        try:
            self.repo.update(plot)
            return Result.ok(plot)
        except Exception as e:
            return Result.fail(e)

    def execute(self, dto: CropPlotDTO) -> Response:
        self.dto = dto

        return self._load_plot() \
            .bind(self._crop_plot) \
            .bind(self._update_plot) \
            .bind(lambda: right(None)) \
            .if_err(lambda e: left(UnexpectedError(e))) \
            .value
