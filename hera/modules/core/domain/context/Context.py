# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from abc import ABC
from typing import TypeVar, Generic

from olympus.domain import Guid
from olympus.domain.events import AggregateRoot
from olympus.monads import Maybe, Result

P = TypeVar('P')


class UnableTransiteState(Exception):
    def __init__(self, state: 'Context.State'):
        super().__init__(f'Unable to transite to {state.__state__} state.')


class Context(Generic[P], AggregateRoot[P]):
    """
    The main propose of this class is to provide a context to the state
    machine into domain layer.

    When a state is changed, the context is updated with the new state, and
    this action is recorded as a domain event.
    """

    class State(ABC):
        """
        State is a class that represents a state of a use case.
        """

        __state__: str

        def __init__(self):
            """
            Initialize the state with a context
            """
            self._context = None

        @property
        def context(self) -> 'Context':
            """
            Get the context of the state
            """
            return self._context

        @context.setter
        def context(self, context: 'Context'):
            """
            Set the context of the state
            """
            self._context = context

        def _cannot_be(self, state: str) -> Result:
            """
            Returns a failure because a plot can't be any other state after failed.

            -------
            Returns
            -------
                Result[State]: The result of operation.
            """
            from modules.core.domain.errors import InvalidStateTransition
            return Result.fail(InvalidStateTransition(self.context.id, self.__state__, state))

    def __init__(self, state: State, props: P, id: Maybe[Guid] = None):
        """
        Creates a new instance of PlotContext.

        ----------
        Parameters
        ----------
        state: State
            The initial state.
        """
        super().__init__(props, id)
        self._state = state
        self._state.context = self

    @property
    def state(self) -> State:
        """
        State property.

        -------
        Returns
        -------
            The current state.
        """
        return self._state

    def __eq__(self, other: object) -> bool:
        """
        Compares two PlotContext objects.

        ----------
        Parameters
        ----------
        other: object
            The other object to compare.

        -------
        Returns
        -------
            True if the objects are equals, otherwise False.
        """
        if not isinstance(other, Context):
            return False

        return self.state == other.state

    def _do_transit(self, state: State | None):
        """
        Transits to a new state.

        ----------
        Parameters
        ----------
        state: S
            The new state.

        -------
        Returns
        -------
            The new state.
        """

        if self.state == state:
            print(f'Already in state {state}')
            return self

        print(f'Transiting {self.id} from {self.state.__state__} to {state.__state__}')

        self._state = state
        self._state.context = self

    def transit_to(self, state: State) -> 'Context':
        """
        Transits to a new state.

        ----------
        Parameters
        ----------
        state: S
            The new state.F

        -------
        Returns
        -------
            The new state.
        """
        return self._do_transit(state)
