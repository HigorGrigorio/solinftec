# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import Guid
from olympus.monads import Maybe, guard_all, W, Result

from .PieceContext import PieceContext, PieceProps, BasePieceState


class Piece(PieceContext):
    """
    Piece is generated from a plot piecing
    """

    def __init__(self, state: BasePieceState, props: PieceProps, id: Maybe[Guid] = Maybe.nothing()):
        """
        Piece constructor

        ----------
        Parameters
        ----------
        state: BasePlotState
            The state of the piece
        props: PieceProps
            The parameters of the piece
        id: Maybe[Guid]
            The id of the piece
        """
        super().__init__(state, props, id)

    def mark_as_segmented(self) -> Result['Piece']:
        """
        Mark the piece as segmented

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        return self.state.mark_as_segmented().bind(lambda: self)

    def mark_as_skeletonized(self) -> Result['Piece']:
        """
        Mark the piece as skeletonized

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        return self.state.mark_as_skeletonized().bind(lambda: self)

    def mark_as_restored(self) -> Result['Piece']:
        """
        Mark the piece as restored

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        return self.state.mark_as_restored().bind(lambda: self)

    def mark_as_finished(self) -> Result['Piece']:
        """
        Mark the piece as finished

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        return self.state.mark_as_finished().bind(lambda: self)

    def mark_as_failed(self) -> Result['Piece']:
        """
        Mark the piece as failed

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        return self.state.mark_as_failed().bind(lambda: self)

    def mark_as_queued(self) -> Result['Piece']:
        """
        Mark the piece as queued

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        return self.state.mark_as_queued().bind(lambda: self)

    @classmethod
    def new(
            cls,
            props: PieceProps,
            state: Maybe[BasePieceState] = Maybe.nothing(),
            id: Maybe[Guid] = Maybe.nothing()
    ) -> Result['Piece']:
        """
        Create a new Piece

        -------
        Args
        -------
        props: PieceProps
            The parameters to create a new Piece
        state: Maybe[BasePlotState]
            The state of the new Piece
        id: Maybe[Guid]
            The id of the new Piece

        -------
        Returns
        -------
        Result[Piece]
            The result of operation
        """
        from .events import PieceCreated
        from .states.Queued import Queued

        guard_result = guard_all(props, {
            'file': 'required',
        })

        if not guard_result.is_satisfied():
            return W(guard_result)

        is_new = id.is_nothing()
        piece = cls(
            state.get_or_else(Queued),
            props,
            id
        )

        if is_new:
            piece.remind(PieceCreated(piece))

        return Result.ok(piece)
