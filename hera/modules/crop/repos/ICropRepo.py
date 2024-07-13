# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from abc import ABC

from .ICreateCropRepo import ICreateCropRepo
from .IGetCropRepo import IGetCropRepo
from .IUpdateCropRepo import IUpdateCropRepo


class ICropRepo(
    ICreateCropRepo,
    IGetCropRepo,
    IUpdateCropRepo,
    ABC
):
    """
    Crop Repository Interface
    """
    ...
