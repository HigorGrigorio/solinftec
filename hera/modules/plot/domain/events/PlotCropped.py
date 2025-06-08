# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from .PlotStateChanged import PlotStateChanged


class PlotCropped(PlotStateChanged):
    def __init__(self, plot, old):
        super().__init__(plot, old)

    def __str__(self):
        return f'Plot {self.plot.id} cropped'
