# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache
from typing import Type

from olympus.domain.events import EventHandler


def import_module(module):
    return __import__(module, fromlist=['__all__'])


def setup_subscriber(subscriber: Type[EventHandler]) -> EventHandler:
    """
    Set up a subscriber instance

    ----------
    Parameters
    ----------
    subscriber :
        The subscriber name

    -------
    Returns
    -------
    object
        The subscriber instance
    """
    instance = subscriber()
    instance.setup()
    return instance


def setup_subscribers(modules: list[str]) -> list[EventHandler]:
    """
    Setup all subscribers in the modules registered on folders
    named subscribers.

    -------
    Returns
    -------
    list[EventHandler]
        A list with all subscribers instances
    """
    instances = []

    for module in modules:
        subscribers = import_module('modules.%s.subscribers' % module)

        if '__all__' not in subscribers.__dict__:  # pragma: no cover
            print(f'No subscribers found in {module}')
            continue

        for subscriber in subscribers.__all__:
            instances.append(setup_subscriber(subscriber))

    return instances
