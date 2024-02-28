# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import abc
from logging import Logger
from threading import Thread, Event
from typing import TypeVar, Generic

from confluent_kafka import Consumer, Message, KafkaError
from pydantic import BaseModel

M = TypeVar('M', bound=BaseModel)


class ConsumerLoop(Generic[M], abc.ABC):
    __topic__: list[str] = []

    def __init__(self, consumer: Consumer, logger: Logger, ):
        self.consumer = consumer
        self.thread = Thread(target=self.run)
        self.event = Event()
        self.logger = logger

    @abc.abstractmethod
    def handle(self, model: M) -> None:
        ...

    def _decode_message(self, message: Message) -> M:
        message = message.value().decode("utf-8")
        self.logger.info(f'Consuming message: {message}')
        return M.model_validate_json(message)

    def setup(self):
        self.thread.start()

    def shutdown(self):
        self.event.set()
        self.thread.join()

    def run(self):
        try:
            self.consumer.subscribe(self.__topic__)
            self.logger.info(f'Subscribed to {self.__topic__}')

            while not self.event.is_set():
                message = self.consumer.poll(1.0)

                if message is None:
                    continue

                if message.error():
                    print("Consumer error: {}".format(message.error()))
                    continue

                self.handle(self._decode_message(message))
        except KafkaError as e:
            print(e)
        finally:
            self.consumer.close()
