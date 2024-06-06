# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from fastapi import FastAPI

from config.subscribers import setup_subscribers
from infra.http.routes.v1 import V1Router
from infra.schemas.sqlalchemy import init

setup_subscribers([
    'plot',
    'piece',
])

app = FastAPI()

app.include_router(V1Router, prefix='/api')

# initialize the sqlalchemy models
init()
