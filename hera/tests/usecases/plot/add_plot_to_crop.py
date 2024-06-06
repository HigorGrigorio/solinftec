# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import unittest

from olympus.domain.events import EventBus
from olympus.monads import Maybe

from modules.core.domain import File
from modules.plot.domain import Plot
from modules.plot.domain.events import PlotCreated
from modules.plot.repos.inmemory import InMemoryPlotRepo
from modules.plot.services.inmemory import AresServiceInMemory
from modules.plot.usecases.add_plot_to_crop.AddPlotToCropDTO import AddPlotToCropDTO
from modules.plot.usecases.add_plot_to_crop.AddPlotToCropUseCase import AddPlotToCropUseCase


class TestAddPlotToCrop(unittest.TestCase):

    def setUp(self) -> None:
        from modules.plot.domain.states import Queued

        ares = AresServiceInMemory()
        plotRepository = InMemoryPlotRepo()
        executor = AddPlotToCropUseCase(plotRepository, ares)
        plot = Plot(Queued(), {
            'file': File.new(
                '/path/to/file',
                'file',
                'png',
            ).unwrap(),
            'description': '',
            'pieces': Maybe.nothing(),
            'created_at': None,
            'updated_at': None,
        }, Maybe.nothing())

        self.ares = ares
        self.plotRepository = plotRepository
        self.executor = executor
        self.plot = plot

        # store the plot in the repository
        plotRepository.create(plot)

        def _execute(event: PlotCreated):
            executor.execute(AddPlotToCropDTO(id=event.plot.id.value))

        EventBus.clear_event_bus()

        # on plot created, execute this callback
        EventBus.bind(PlotCreated, _execute)

    def testIfPlotIsAddedToCropQueueAfterBeingCreated(self):
        # create a fake plot
        plot = Plot.new({
            'file': File.new(
                '/path/to/file',
                'file',
                'png',
            ).unwrap(),
            'description': '',
            'pieces': Maybe.nothing(),
            'created_at': None,
            'updated_at': None,
        }).unwrap()

        # store the plot in the repository
        self.plotRepository.create(plot)

        # trigger the event from aggregate plot
        EventBus.dispatch_event_bus_for_aggregate(plot)

        # expect the plot to be added to the crop queue
        self.assertEqual(len(self.ares.queue), 1)

    def testIfNotShouldBeAbleToAddPlotToCropIfPlotDoesNotExist(self):
        self.plotRepository._plots.clear()

        self.plot.remind(PlotCreated(self.plot))

        # expect the use case to return an error
        res = self.executor.execute(AddPlotToCropDTO(id=self.plot.id.value))
        self.assertTrue(res.is_left)

        # expect the plot to be added to the crop queue
        self.assertEqual(len(self.ares.queue), 0)

        # expect the error to be a PlotNotFoundError
        self.assertEqual(res.value.err(), f'Plot not found: {self.plot.id.value}')
