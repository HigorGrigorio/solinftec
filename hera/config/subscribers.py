# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------
from functools import lru_cache


def import_module(module):
    return __import__(module, fromlist=['__all__'])


@lru_cache
def setup_subscribers():
    modules = ['plot']
    instances = []

    for module in modules:
        subscribers = __import__('modules.%s.subscribers' % module, fromlist=['__all__'])

        for subscriber in subscribers.__all__:
            instance = subscriber()
            instance.setup()
            instances.append(instance)

    return instances
