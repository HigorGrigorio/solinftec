# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from modules.plot.services.contracts import IAresService


class AresServiceInMemory(IAresService):
    queue: list = []

    def __init__(self):
        self.queue = []

    def crop(self, plot) -> None:
        self.queue.append(plot)


