# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import logging
from functools import lru_cache


def get_logger_config():
    return {
        'level': logging.DEBUG,
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'datefmt': '%Y-%m-%d %H:%M:%S',
    }


@lru_cache
def get_logger():
    logging.basicConfig(**get_logger_config())
    return logging.getLogger('hera')
