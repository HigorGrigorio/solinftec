# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import DomainError


class InvalidStateTransition(DomainError):
    """
    The state transition is invalid.
    """

    def __init__(self, id: str, from_state: str, to_state: str):
        """
        The constructor for InvalidStateTransition class.

        ----------
        Parameters
        ----------
        id : str
            The id of the object.
        from_state : str
            The current state.
        to_state : str
            The target state.
        """
        super().__init__(f'The context {id} cannot be transitioned from {from_state} to {to_state}.')
        self.id = id
        self.from_state = from_state
        self.to_state = to_state
