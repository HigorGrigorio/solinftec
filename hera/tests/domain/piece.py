# -----------------------------------------------------------------------------
# (C) 2024 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import unittest

from olympus.monads import Maybe, Result

from modules.core.domain import File
from modules.core.domain.errors import InvalidStateTransition, AlreadyInState
from modules.piece.domain import Crop, BaseCropState
from modules.piece.domain.states import Queued, Segmented, Skeletonized, Restored, Finished
from tests.mocks import FileMock


def make_stu(
        file: File = FileMock(),
        state: BaseCropState = Queued()
) -> Result[Crop]:
    return Crop.new(
        props={'file': file, 'plot_id': Maybe.nothing()},
        state=Maybe.just(state)
    )


class TestPiece(unittest.TestCase):
    def test_if_should_be_able_create_a_piece_with_valid_props(self):
        # Arrange
        stu = make_stu().unwrap()

        # Assert
        self.assertIsInstance(stu, Crop)
        self.assertIsInstance(stu.state, Queued)

    def test_if_should_be_able_create_a_piece_with_invalid_props(self):
        # Arrange
        stu = make_stu(file=None)

        # Assert
        self.assertTrue(stu.is_err)

    def _test_transitions(self, machine: Crop, transitions: list):
        # a recursive helper function to test transitions

        if not transitions:
            return Result.ok(machine)

        method = getattr(machine, f'mark_as_{transitions.pop(0)}')

        return method() \
            .bind(lambda m: self._test_transitions(m, transitions))

    def test_piece_transitions(self):
        self._test_transitions(make_stu().unwrap(), ['segmented'])
        self._test_transitions(make_stu().unwrap(), ['segmented', 'skeletonized'])
        self._test_transitions(make_stu().unwrap(), ['segmented', 'skeletonized', 'restored'])
        self._test_transitions(make_stu().unwrap(), ['segmented', 'skeletonized', 'restored', 'finished'])
        self._test_transitions(make_stu().unwrap(), ['segmented', 'skeletonized', 'restored', 'finished', 'failed'])

    def _test_invalid_transition_error(self, machine: Crop, transitions: list):
        # a helper function to test invalid transitions

        states = ['queued', 'segmented', 'skeletonized', 'restored', 'finished']

        for transition in states:

            # skip valid transitions
            if transition in transitions:
                continue

            method = getattr(machine, f'mark_as_{transition}')
            result = method()
            self.assertIsInstance(result, Result)
            self.assertTrue(result.is_err)
            self.assertIsInstance(result.err(), InvalidStateTransition)

    def test_invalid_transition(self):
        self._test_invalid_transition_error(make_stu(state=Segmented()).unwrap(), ['skeletonized', 'segmented'])
        self._test_invalid_transition_error(make_stu(state=Skeletonized()).unwrap(), ['restored', 'skeletonized'])
        self._test_invalid_transition_error(make_stu(state=Restored()).unwrap(), ['finished', 'restored'])
        self._test_invalid_transition_error(make_stu(state=Finished()).unwrap(), ['finished'])

    def _test_already_in_state(self, machine: Crop):
        # a helper function to test already in state error

        method = getattr(machine, f'mark_as_{machine.state.__state__}')
        result = method()
        self.assertIsInstance(result, Result)
        self.assertTrue(result.is_err)
        self.assertIsInstance(result.err(), AlreadyInState)

    def test_already_in_state_error(self):
        self._test_already_in_state(make_stu(state=Segmented()).unwrap())
        self._test_already_in_state(make_stu(state=Skeletonized()).unwrap())
        self._test_already_in_state(make_stu(state=Restored()).unwrap())
        self._test_already_in_state(make_stu(state=Finished()).unwrap())


if __name__ == '__main__':
    unittest.main()
