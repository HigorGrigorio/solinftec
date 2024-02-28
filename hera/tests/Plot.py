# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------


import unittest

from olympus.domain import Guid
from olympus.monads import Result, Maybe

from modules.core.domain.errors import InvalidStateTransition, AlreadyInState
from modules.plot.domain import Pieces, PlotProps, BasePlotState
from modules.plot.domain.Plot import Plot
from modules.plot.domain.states import Queued, Cropped, Segmented, Skeletonized, Restored, Rescaled, Finished
from tests.mocks import FileMock


def make_stu(
        file: FileMock = FileMock(),
        description: str = '',
        pieces: Pieces = Pieces.new(),
        state: BasePlotState = Queued()
) -> Result[Plot]:
    props = PlotProps(
        file=file,
        description=description,
        pieces=pieces
    )
    return Plot.new(props, Maybe.just(state))


class PlotTests(unittest.TestCase):
    def test_plot_creation_with_valid_props(self):
        # Arrange
        stu = make_stu().unwrap()

        # Assert
        self.assertIsInstance(stu, Plot)
        self.assertIsInstance(stu.id, Guid)
        self.assertIsInstance(stu.state, Queued)

    def test_plot_creation_with_invalid_props(self):
        # Arrange
        stu = make_stu(file=None)

        # Assert
        self.assertTrue(stu.is_err)

    def test_plot_creation_with_invalid_pieces(self):
        # Arrange
        result = make_stu(pieces=None)

        # Assert
        self.assertTrue(result.is_err)

    def _test_transitions(self, machine: Plot, transitions: list):
        if not transitions:
            return Result.ok(machine)

        transition = transitions.pop(0)
        method = getattr(machine, f'mark_as_{transition}')

        return method() \
            .bind(lambda m: self._test_transitions(m, transitions))

    def test_valid_machine(self):
        self.assertTrue(self._test_transitions(make_stu().unwrap(), ['cropped']).is_ok)
        self.assertTrue(self._test_transitions(make_stu().unwrap(), ['cropped', 'segmented']).is_ok)
        self.assertTrue(self._test_transitions(make_stu().unwrap(), ['cropped', 'segmented', 'skeletonized']).is_ok)
        self.assertTrue(
            self._test_transitions(make_stu().unwrap(), ['cropped', 'segmented', 'skeletonized', 'restored']).is_ok)
        self.assertTrue(self._test_transitions(make_stu().unwrap(),
                                               ['cropped', 'segmented', 'skeletonized', 'restored', 'rescaled']).is_ok)
        self.assertTrue(self._test_transitions(make_stu().unwrap(),
                                               ['cropped', 'segmented', 'skeletonized', 'restored', 'rescaled',
                                                'finished']).is_ok)

    def _test_invalid_transition_error(self, machine: Plot, transitions: list):
        states = ['queued', 'cropped', 'segmented', 'skeletonized', 'restored', 'rescaled', 'finished']

        for transition in states:
            if transition in transitions:
                continue

            method = getattr(machine, f'mark_as_{transition}')
            result = method()
            self.assertIsInstance(result, Result)
            self.assertTrue(result.is_err)
            self.assertIsInstance(result.err(), InvalidStateTransition)

    def test_invalid_transition(self):
        self._test_invalid_transition_error(make_stu().unwrap(), ['cropped', 'queued'])
        self._test_invalid_transition_error(make_stu(state=Cropped()).unwrap(), ['segmented', 'cropped'])
        self._test_invalid_transition_error(make_stu(state=Segmented()).unwrap(), ['skeletonized', 'segmented'])
        self._test_invalid_transition_error(make_stu(state=Skeletonized()).unwrap(), ['restored', 'skeletonized'])
        self._test_invalid_transition_error(make_stu(state=Restored()).unwrap(), ['rescaled', 'restored'])
        self._test_invalid_transition_error(make_stu(state=Rescaled()).unwrap(), ['finished', 'rescaled'])
        self._test_invalid_transition_error(make_stu(state=Finished()).unwrap(), ['finished'])

    def _test_already_in_state(self, machine: Plot):
        method = getattr(machine, f'mark_as_{machine.state.__state__}')
        result = method()
        self.assertIsInstance(result, Result)
        self.assertTrue(result.is_err)
        self.assertIsInstance(result.err(), AlreadyInState)

    def test_already_in_state_error(self):
        self._test_already_in_state(make_stu(state=Cropped()).unwrap())
        self._test_already_in_state(make_stu(state=Segmented()).unwrap())
        self._test_already_in_state(make_stu(state=Skeletonized()).unwrap())
        self._test_already_in_state(make_stu(state=Restored()).unwrap())
        self._test_already_in_state(make_stu(state=Rescaled()).unwrap())
        self._test_already_in_state(make_stu(state=Finished()).unwrap())


if __name__ == '__main__':
    unittest.main()
