# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import IUseCase, Guid
from olympus.monads import Either, Result, left, right
from shared.logic import UnexpectedError

from modules.plot.services.contracts import IAresService
from .AddPlotToCropDTO import AddPlotToCropDTO
from .AddPlotToCropError import PlotNotFoundError
from ...domain import Plot
from ...repos import IPlotRepo

Response = Either[UnexpectedError | PlotNotFoundError, None]


class AddPlotToCropUseCase(IUseCase[AddPlotToCropDTO, Response]):
    dto: AddPlotToCropDTO

    def __init__(self, repo: IPlotRepo, ares: IAresService):
        self.ares = ares
        self.repo = repo

    def _load_plot(self) -> Result[Plot]:
        id = Guid(self.dto.id)
        return Result.ok(self.repo.get(id))

    def _notify_ares(self, plot: Plot) -> Result[Plot] | PlotNotFoundError:
        try:

            if plot is None:
                return PlotNotFoundError(self.dto.id)

            self.ares.crop({
                'id': plot.id.value,
                'path': plot.file.get_location(),
            })
            return Result.ok(plot)
        except Exception as e:
            return Result.fail(e)

    def execute(self, dto: AddPlotToCropDTO) -> Response:
        self.dto = dto

        result = self._load_plot() \
            .bind(self._notify_ares)

        if result.is_ok:
            return right(result.value)

        return left(result)
