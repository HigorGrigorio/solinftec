# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import DomainError


class NotYet(DomainError):
    def __init__(self, id: str, yet: str):
        super().__init__(f'{id} not yet {yet}.')
