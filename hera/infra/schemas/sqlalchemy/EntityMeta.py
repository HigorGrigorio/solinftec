# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import (
    database_exists,
    create_database
)

from config.database import Engine

# Base Entity Model Schema
EntityMeta = declarative_base()


def init():
    if not database_exists(Engine.url):
        create_database(Engine.url)

    EntityMeta.metadata.create_all(bind=Engine)
