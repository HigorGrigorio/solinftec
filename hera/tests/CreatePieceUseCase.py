import unittest

from olympus.monads import Maybe

from modules.core.domain import File
from modules.core.domain.File import FileProps
from modules.piece.repos.inmemory import InMemoryPieceRepo
from modules.piece.usecases import create
from modules.plot.domain import Pieces
from modules.plot.repos.inmemory import InMemoryPlotRepo


def make_fake_plot():
    from modules.plot.domain import Plot
    from modules.plot.domain import PlotProps
    from modules.plot.domain.states import Queued

    file = File(FileProps(
        path='path',
        name='name',
        extension='ext',
    ))

    return Plot(Queued(), PlotProps(
        file=file,
        description='',
        pieces=Pieces([]),
    ), Maybe.nothing())


class MyTestCase(unittest.TestCase):
    def test_create(self):
        plot_repo = InMemoryPlotRepo()
        piece_repo = InMemoryPieceRepo()

        executor = create.CreatePieceUseCase(
            plot_repo,
            piece_repo,
        )

        dto = create.CreatePieceDTO(
            path='path',
            name='name',
            extension='ext',
            plot='0',
        )

        res = executor.execute(dto)

        self.assertIsInstance(res.value, create.RelatedNotFoundError)

    if __name__ == '__main__':
        unittest.main()
