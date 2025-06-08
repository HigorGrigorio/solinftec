# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

class UseCaseError:
    message: str

    def __init__(self, message: str) -> None:
        self.message = message
