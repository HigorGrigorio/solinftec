# -----------------------------------------------------------------------------
# (C) 2025 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import os
from pathlib import Path

WIDTH = os.getenv("WIDTH", 256)
HEIGHT = os.getenv("HEIGHT", 256)

MODEL = Path(__file__).parent / "../model"

# Kafka
KAFKA_BROKER_HOSTNAME = os.getenv("KAFKA_BROKER_HOSTNAME", "localhost")
KAFKA_BROKER_PORT = os.getenv("KAFKA_BROKER_PORT", "19092")