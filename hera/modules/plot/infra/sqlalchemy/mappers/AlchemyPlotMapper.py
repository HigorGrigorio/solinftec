# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from datetime import datetime
from typing import Type

from olympus.domain import Guid
from olympus.monads import Maybe
from olympus.monads.maybe import just

from infra.schemas.sqlalchemy import PlotModel
from modules.plot.domain import (
    Plot,
    File,
    BasePlotState,
)


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
    def _str_to_datetime(value: str):
        """
        Convert a string to a datetime

        ----------
        Parameters
        ----------
        value: str
            The string value

        Returns
        -------
        Maybe
            The datetime or nothing
        """
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return None

    @staticmethod
    def _datetime_to_str(value: datetime) -> str:
        """
        Convert a datetime to a string

        ----------
        Parameters
        ----------
        value: datetime
            The datetime value

        Returns
        -------
        str
            The string value
        """
        return value.isoformat()

    @staticmethod
    def to_domain(model: Type[PlotModel]) -> Plot:
        return Plot(
            AlchemyPlotMapper._map_plot_state(model.state),
            {
                'file': File.new(model.name, model.path, model.extension).unwrap(),
                'description': model.description,
                'created_at': AlchemyPlotMapper._datetime_to_str(model.created_at),
                'updated_at': AlchemyPlotMapper._datetime_to_str(model.updated_at),
                'pieces': Maybe.nothing(),  # TODO: use lazy loading
            }, just(Guid(model.id))
        )

    @staticmethod
    def to_model(plot: Plot) -> PlotModel:
        return PlotModel(
            id=plot.id.value,
            name=plot.file.get_name(),
            extension=plot.file.get_extension(),
            path=plot.file.get_path(),
            state=plot.state.__state__,
            description=plot.description,
            created_at=AlchemyPlotMapper._str_to_datetime(plot.created_at),
            updated_at=AlchemyPlotMapper._str_to_datetime(plot.updated_at),
        )
