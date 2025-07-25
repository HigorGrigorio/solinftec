# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
import datetime
from typing import Type

from olympus.domain import Guid
from olympus.monads.maybe import just

from infra.schemas.sqlalchemy import CropModel
from modules.core.domain import File
from modules.core.domain.File import FileProps
from modules.crop.domain import Crop, BaseCropState
from modules.crop.domain.CropContext import CropProps


class AlchemyCropMapper:
    """
    Crop Mapper
    """

    def __init__(self, crop: Crop | CropModel):
        self.crop = crop

    @staticmethod
    def _map_model_state_to_domain(crop: Type[CropModel]) -> BaseCropState:
        """
        Map the crop state to domain state. This function uses
        BasePlotState.__subclasses__() to get all BasePlotState
        subclasses and then compare __state__ with the crop state.
        """
        for subclass in BaseCropState.__subclasses__():
            if subclass.__state__ == crop.state:
                return subclass()

        raise Exception('Invalid state')

    @staticmethod
    def to_domain(crop: Type[CropModel]) -> Crop:
        """
        Convert to domain

        ----------
        Parameters
        ----------
        crop: Type[CropModel]
            The model

        -------
        Returns
        -------
        Crop
            The domain
        """

        return Crop(
            AlchemyCropMapper._map_model_state_to_domain(crop),
            CropProps(
                file=File(
                    FileProps(
                        name=crop.name,
                        path=crop.path,
                        extension=crop.extension
                    )
                ),
                plot_id=just(crop.plot_id),
                created_at=crop.created_at.isoformat(),
                updated_at=crop.updated_at.isoformat()
            ),
            just(Guid(crop.id))
        )

    @staticmethod
    def to_model(crop: Crop) -> CropModel:
        """
        Convert to crop
        """
        file = crop.get_file()

        plot_id = crop.get_plot_id().get_or_else(None)

        if plot_id is not None:
            plot_id = plot_id.value

        return CropModel(
            id=crop.id.value,
            name=file.get_name(),
            path=file.get_path(),
            plot_id=plot_id,
            state=crop.state.str(),
            extension=file.get_extension(),
            created_at=crop.get_created_at().get_or_else(datetime.datetime.now().isoformat()),
            updated_at=crop.get_updated_at().get_or_else(datetime.datetime.now().isoformat()),
        )
