# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import DomainError


class AlreadyInState(DomainError):
    def __init__(self, id: str, already: str):
        super().__init__(f'{id} already {already}.')
