import json
import sys
from confluent_kafka import Consumer, Producer, KafkaError, KafkaException
import numpy as np
from ModelTF import Model
from models import TileMessage
from pathlib import Path
from PIL import Image


def save(segmented: Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    segmented.save(fp=path)


def notify_segment_created(producer: Producer, id: str, path: Path) -> None:
    producer.produce(
        "hera.segment-created",
        json.dumps({"parent": id, "path": str(path)}).encode("utf-8"),
    )


def notify_plot_segmented(producer: Producer, id: str) -> None:
    producer.produce("hera.plot-segmented", json.dumps({"id": id}).encode("utf-8"))


def execute(model: Model, id: str, path: Path, producer: Producer) -> None:
    img = Image.open(path)
    img = np.asarray(img)
    segmented = model.predict(img)
    segmented = Image.fromarray(segmented)
    save(segmented, path)
    notify_segment_created(producer, id, path)


def main() -> None:

    model = Model("./data/", "model/")

    consumer_conf = {
        "bootstrap.servers": "localhost:19092",
        "auto.offset.reset": "earliest",
        "group.id": "laquesis-group",
    }

    producer_conf = {"bootstrap.servers": "localhost:19092"}

    consumer_topic = "hera.plot-cropped"

    producer_topic = "hera.plot-segmented"

    consumer = Consumer(consumer_conf)

    producer = Producer(producer_conf)

    running = True

    try:
        consumer.subscribe([consumer_topic])

        while running:
            msg = consumer.poll(1.0)

            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write(
                        "%% %s [%d] reached end at offset %d\n"
                        % (msg.topic(), msg.partition(), msg.offset())
                    )

            elif msg.error():
                raise KafkaException(msg.error())
            else:
                raw = json.loads(msg.value().decode("utf-8"))
                message = TileMessage(**raw)

                print(f"Message: {message}")

                path = Path(message.path)
                id: str = message.id

                execute(model, id, path, producer)
                notify_plot_segmented(producer, id)
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
