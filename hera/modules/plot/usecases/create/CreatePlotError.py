# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from shared.logic import UnexpectedError


class PlotInvalid(UnexpectedError):
    def __init__(self, message: str) -> None:
        super().__init__(f'Invalid plot properties: {message}')
