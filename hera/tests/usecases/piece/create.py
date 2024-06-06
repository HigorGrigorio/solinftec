# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
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


class TestCreatePieceUseCase(unittest.TestCase):
    def test_if_it_should_be_able_create_an_piece(self):
        # creates a fake plot repository with a fake plot
        fake_plot = make_fake_plot()
        plot_repo = InMemoryPlotRepo()
        plot_repo.create(fake_plot)

        piece_repo = InMemoryPieceRepo()

        # the use case executor
        executor = create.CreatePieceUseCase(
            plot_repo,
            piece_repo,
        )

        # the use case data transfer object
        dto = create.CreatePieceDTO(
            path='/path/to/file',
            name='file',
            extension='ext',
            plot_id=fake_plot.id.value,
        )

        # after execute the use case, expect the piece to be created
        # and the result to be the piece itself id
        res = executor.execute(dto)

        self.assertTrue(res.is_right)
        self.assertIsInstance(res.value, str)
        self.assertTrue(piece_repo._pieces.get(res.value) is not None)

    def test_if_it_should_not_be_able_to_create_an_piece_when_plot_does_not_exist(self):
        # if the plot does not exist, the use case should return a RelatedPlotNotFoundError

        # creates a fake empty plot repository
        plot_repo = InMemoryPlotRepo()

        piece_repo = InMemoryPieceRepo()

        # the use case executor
        executor = create.CreatePieceUseCase(
            plot_repo,
            piece_repo,
        )

        # the use case data transfer object
        dto = create.CreatePieceDTO(
            path='/path/to/file',
            name='file',
            extension='ext',
            plot_id='non-existent-plot-id',
        )

        # after execute the use case, expect the result to be a RelatedPlotNotFoundError
        # with the message 'Plot non-existent-plot-id related to piece not found.'
        res = executor.execute(dto)

        self.assertTrue(res.is_left)
        self.assertEqual(res.value.err(), 'Plot non-existent-plot-id related to piece not found.')
        self.assertTrue(piece_repo._pieces.__len__() == 0)


if __name__ == '__main__':
    unittest.main()
