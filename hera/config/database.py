# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, scoped_session

from config.enviroment import get_environment_variables

env = get_environment_variables()

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------

# Generate Database URL
DATABASE_URL = URL.create(
    drivername=env.DATABASE_DIALECT,
    username=env.DATABASE_USERNAME,
    password=env.DATABASE_PASSWORD,
    host=env.DATABASE_HOSTNAME,
    port=env.DATABASE_PORT,
    database=env.DATABASE_NAME
)

print(DATABASE_URL)

Engine = create_engine(
    DATABASE_URL, echo=env.DEBUG_MODE, future=True
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=Engine
)


def get_db_connection():
    db = scoped_session(SessionLocal)
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_session():
    # Assuming get_db_connection is a generator that yields a session
    db_connection_gen = get_db_connection()
    session = next(db_connection_gen)
    try:
        yield session
    finally:
        # Ensures the session is closed properly
        next(db_connection_gen, None)