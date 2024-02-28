# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from abc import ABC

from .ICreatePlotRepo import ICreatePlotRepo
from .IGetPlotRepo import IGetPlotRepo
from .IUpdatePlotRepo import IUpdatePlotRepo


class IPlotRepo(
    ICreatePlotRepo,
    IUpdatePlotRepo,
    IGetPlotRepo,
    ABC
):
    """
    Plot Repository Interface
    """
    ...
