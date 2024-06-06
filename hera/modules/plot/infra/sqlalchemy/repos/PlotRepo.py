# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache

from fastapi import Depends
from olympus.domain import Guid
from olympus.domain.events import trigger
from sqlalchemy.orm import Session

from config.database import get_db_connection
from infra.schemas.sqlalchemy import PlotModel
from modules.plot.domain import Plot
from modules.plot.infra.sqlalchemy.mappers.AlchemyPlotMapper import AlchemyPlotMapper
from modules.plot.repos import IPlotRepo


class PlotRepo(IPlotRepo):
    session: Session

    def __init__(self, session: Session = Depends(get_db_connection)) -> None:
        self.session = session

    def create(self, plot: Plot) -> Plot:
        model = AlchemyPlotMapper.to_model(plot)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        trigger(plot.get_events())
        return plot

    def update(self, plot: Plot) -> Plot:
        model = AlchemyPlotMapper.to_model(plot)
        self.session.merge(model)
        self.session.commit()
        trigger(plot.get_events())
        return plot

    def get(self, id: Guid) -> Plot | None:
        model = self.session.get(PlotModel, id.value)
        if model is None:
            return None
        return AlchemyPlotMapper.to_domain(model)

    @classmethod
    @lru_cache
    def instance(cls, session: Session | None = None) -> 'PlotRepo':
        session = session or get_db_connection()
        return PlotRepo(session)
