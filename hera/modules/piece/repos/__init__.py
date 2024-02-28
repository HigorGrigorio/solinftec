# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from .ICreatePieceRepo import ICreatePieceRepo
from .IGetPieceRepo import IGetPieceRepo
from .IPieceRepo import IPieceRepo
from .IUpdatePieceRepo import IUpdatePieceRepo

__all__ = [
    IGetPieceRepo,
    IUpdatePieceRepo,
    ICreatePieceRepo,
    IPieceRepo
]
