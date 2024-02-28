# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from abc import ABC

from .ICreatePieceRepo import ICreatePieceRepo
from .IGetPieceRepo import IGetPieceRepo
from .IUpdatePieceRepo import IUpdatePieceRepo


class IPieceRepo(
    ICreatePieceRepo,
    IGetPieceRepo,
    IUpdatePieceRepo,
    ABC
):
    """
    Piece Repository Interface
    """
    ...
