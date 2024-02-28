# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from .ICreatePlotRepo import ICreatePlotRepo
from .IGetPlotRepo import IGetPlotRepo
from .IPlotRepo import IPlotRepo
from .IUpdatePlotRepo import IUpdatePlotRepo

__all__ = [
    'IPlotRepo',
    'IGetPlotRepo',
    'ICreatePlotRepo',
    'IUpdatePlotRepo'
]
