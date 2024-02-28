# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from typing import Type

from olympus.domain import Guid
from olympus.monads.maybe import just

from modules.plot.domain import (
    Plot,
    File,
    BasePlotState,
)
from modules.plot.infra.sqlalchemy.models import PlotModel


class AlchemyPlotMapper:
    @staticmethod
    def _map_plot_state(state: str) -> BasePlotState:
        """
        Map the state of plot to the state of domain.

        ----------
        Parameters
        ----------
        state: str
            The state of plot.

        Returns
        -------
        BasePlotState
            The state of domain.
        """
        cls = None

        for sub in BasePlotState.__subclasses__():
            if sub.__state__ == state:
                cls = sub
                break

        if cls is None:
            raise ValueError(f'Invalid state {state}')

        state = cls()

        return state

    @staticmethod
    def to_domain(model: Type[PlotModel]) -> Plot:
        return Plot(
            AlchemyPlotMapper._map_plot_state(model.state),
            {
                'file': File.new(model.name, model.path, model.extension).unwrap(),
                'description': model.description,
                'created_at': model.created_at,
                'updated_at': model.updated_at,
            }, just(Guid(model.id))
        )

    @staticmethod
    def to_model(plot: Plot) -> PlotModel:
        return PlotModel(
            id=plot.id.value,
            name=plot.file.get_name(),
            extension=plot.file.get_extension(),
            path=plot.file.get_path(),
            state=plot.state.to_string(),
            description=plot.description,
            created_at=plot.created_at,
            updated_at=plot.updated_at,
        )
