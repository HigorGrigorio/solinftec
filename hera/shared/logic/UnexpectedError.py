# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import sys

from olympus.monads import result

from .UseCaseError import UseCaseError


class UnexpectedError(result.Result[UseCaseError]):

    def __init__(self, message: str | Exception):
        if isinstance(message, Exception):
            message = str(message)
        super().__init__(False, None, message)
        sys.stderr.write(f'UnexpectedError: {message}\n')

    def message(self) -> str:
        return self.error
