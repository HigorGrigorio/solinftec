# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from shared.logic import UnexpectedError


class RelatedPlotNotFoundError(UnexpectedError):
    """
    Related Not Found Error

    When a related entity is not found
    """
    def __init__(self, plot: str):
        super().__init__(f'Plot {plot} related to piece not found.')
