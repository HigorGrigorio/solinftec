# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from olympus.domain import Guid
from olympus.monads import Maybe, guard_all, W, Result

from .CropContext import CropContext, CropProps, BaseCropState
from ...core.domain import File


class Crop(CropContext):
    """
    Crop is generated from a plot piecing
    """

    def __init__(self, state: BaseCropState, props: CropProps, id: Maybe[Guid] = Maybe.nothing()):
        """
        Crop constructor

        ----------
        Parameters
        ----------
        state: BasePlotState
            The state of the crop
        props: CropProps
            The parameters of the crop
        id: Maybe[Guid]
            The id of the crop
        """
        super().__init__(state, props, id)

    def mark_as_segmented(self) -> Result['Crop']:
        """
        Mark the crop as segmented

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        return self.state.mark_as_segmented().bind(lambda: self)

    def mark_as_skeletonized(self) -> Result['Crop']:
        """
        Mark the crop as skeletonized

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        return self.state.mark_as_skeletonized().bind(lambda: self)

    def mark_as_restored(self) -> Result['Crop']:
        """
        Mark the crop as restored

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        return self.state.mark_as_restored().bind(lambda: self)

    def mark_as_finished(self) -> Result['Crop']:
        """
        Mark the crop as finished

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        return self.state.mark_as_finished().bind(lambda: self)

    def mark_as_failed(self) -> Result['Crop']:
        """
        Mark the crop as failed

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        return self.state.mark_as_failed().bind(lambda: self)

    def mark_as_queued(self) -> Result['Crop']:
        """
        Mark the crop as queued

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        return self.state.mark_as_queued().bind(lambda: self)

    def get_file(self) -> File:
        return self.props['file']

    @classmethod
    def new(
            cls,
            props: CropProps,
            state: Maybe[BaseCropState] = Maybe.nothing(),
            id: Maybe[Guid] = Maybe.nothing()
    ) -> Result['Crop']:
        """
        Create a new Crop

        -------
        Args
        -------
        props: CropProps
            The parameters to create a new Crop
        state: Maybe[BasePlotState]
            The state of the new Crop
        id: Maybe[Guid]
            The id of the new Crop

        -------
        Returns
        -------
        Result[Crop]
            The result of operation
        """
        from .events import CropCreated
        from .states.Queued import Queued

        guard_result = guard_all(props, {
            'file': 'required',
        })

        if not guard_result.is_satisfied():
            return W(guard_result)

        is_new = id.is_nothing()
        crop = cls(
            state.get_or_else(Queued),
            props,
            id
        )

        if is_new:
            crop.remind(CropCreated(crop))

        return Result.ok(crop)
