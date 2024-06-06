# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from fastapi import APIRouter, Request, Response, Depends

from modules.plot.usecases.create import CreatePlotController

PlotRouter = APIRouter(prefix='/plot')


# -----------------------------------------------------------------------------
# Stores a plot
# -----------------------------------------------------------------------------
@PlotRouter.post(
    '/',
)
async def store(
        request: Request,
        response: Response,
        ctrl: CreatePlotController = Depends(CreatePlotController)
):
    return await ctrl.execute(request, response)


__all__ = [
    PlotRouter
]
