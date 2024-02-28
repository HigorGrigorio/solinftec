# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from shared.logic import UnexpectedError


class PlotCanceledError(UnexpectedError):
    def __init__(self, id: str) -> None:
        super().__init__(f'Not possible to crop plot {id} because it was canceled.')
