# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str
    APP_NAME: str
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DEBUG_MODE: bool
    UPLOAD_PATH: str
    KAFKA_BROKER_HOSTNAME: str
    KAFKA_BROKER_PORT: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


@lru_cache
def get_environment_variables():
    return EnvironmentSettings()


@lru_cache
def get_api_version():
    return get_environment_variables().API_VERSION


@lru_cache
def get_kafka_settings():
    return {
        "bootstrap.servers": f"{get_environment_variables().KAFKA_BROKER_HOSTNAME}:{get_environment_variables().KAFKA_BROKER_PORT}",
        "group.id": f"{get_environment_variables().APP_NAME}-group",
        "auto.offset.reset": "earliest",
    }
