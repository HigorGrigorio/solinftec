# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from fastapi import APIRouter

from modules.plot.infra.http.plot import PlotRouter

V1Router = APIRouter(prefix='/v1')

V1Router.include_router(PlotRouter)

__all__ = [
    V1Router
]
