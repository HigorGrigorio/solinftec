# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from shared.logic import UnexpectedError


class PlotNotProcessedError(UnexpectedError):
    def __init__(self, id: str) -> None:
        super().__init__(f'Plot not processed: {id}')

    def __str__(self) -> str:
        return f'PlotNotProcessedError: {self.error}'
