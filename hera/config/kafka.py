# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache

from confluent_kafka import Consumer, Producer

from config.enviroment import get_kafka_settings


@lru_cache
def get_consumer(name: str = 'hera') -> Consumer:
    return Consumer(get_kafka_settings())


@lru_cache
def get_producer(name: str = 'hera') -> Producer:
    return Producer(get_kafka_settings())
