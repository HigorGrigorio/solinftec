import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import shared_memory
from pathlib import Path

import numpy as np
from PIL import Image
from confluent_kafka import Consumer, KafkaError, KafkaException, Producer

import constants as const
from aliases import Box
from models import CropMessage

# disable the image limit
Image.MAX_IMAGE_PIXELS = None


def save(cropped: Image, path: Path) -> None:
    # create the parent directory if it does not exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # save the image
    cropped.save(fp=path)


def notify_crop_created(producer: Producer, id: str, path: Path) -> None:
    producer.produce('hera.crop-created', json.dumps({"parent": id, "path": str(path)}).encode('utf-8'))


def notify_crop_success(producer: Producer, id: str) -> None:
    producer.produce('hera.crop-succeeded', json.dumps({"id": id}).encode('utf-8'))


def notify_crop_error(producer: Producer, id: str, message: str) -> None:
    producer.produce('hera.crop-failed', json.dumps({"id": id, "cause": message}).encode('utf-8'))


# TODO: I think that allocating a huge matrix in memory every time an
# image is processed is unnecessary, using a pre-allocated matrix may
# help to reduce processing time
def open_shared(path: Path):
    img = Image.open(path)
    img = np.asarray(img)

    # share the image in memory
    shm = shared_memory.SharedMemory(create=True, size=img.nbytes)

    # create a shared memory numpy array
    shared_img = np.ndarray(img.shape, dtype=img.dtype, buffer=shm.buf)
    shared_img[:] = img

    return img, shm


def worker(id: str, path: Path, shape, box: Box, shm_name: str) -> tuple[str, Path]:
    shm = None
    try:
        # open the shared memory
        shm = shared_memory.SharedMemory(name=shm_name)
        img = np.ndarray(shape, dtype=np.uint8, buffer=shm.buf)

        # cut the image
        img = img[box[1]:box[3], box[0]:box[2]]

        # convert to PIL image
        img = Image.fromarray(img)

        # save the image
        save(img, path)

        return id, path
    except Exception as e:
        print(f"Error: {e}")
        raise e
    finally:
        if shm is not None:
            # close the shared memory
            shm.close()


def chop(path: Path, id: str, producer: Producer, tile: tuple = const.TILE, overlap: int = 0,
         executor: ThreadPoolExecutor = None) -> None:
    if executor is None:
        executor = ThreadPoolExecutor(2)  # default to 2 workers

    img, shm = open_shared(path)

    width, height = tile
    name = path.name.replace(path.suffix, "")
    output_path = path.parent / '..' / "cropped" / name

    futures = []

    for y in range(0, img.shape[0], height - overlap):
        for x in range(0, img.shape[1], width - overlap):
            box = (x, y, min(x + width, img.shape[1]), min(y + height, img.shape[0]))

            # create the path
            path = output_path / f"{name}_{box[0]}_{box[1]}.png"

            # schedule the worker
            futures.append(executor.submit(worker, id, path, img.shape, box, shm.name))

    # if it has a future with an exception, clean the output path
    exception = None
    results = []

    for future in as_completed(futures):
        if exception := future.exception():
            break
        else:
            results.append(future.result())

    if exception is not None:
        # clean the output path
        output_path.rmtree()

        # notify that the plot failed
        notify_crop_error(producer, id, str(exception))
    else:
        for id, path in results:
            # notify that the plot was cropped
            notify_crop_created(producer, id, path)

        # notify that the plot was cropped
        notify_crop_success(producer, id)

    # send the messages
    producer.poll(0)
    producer.flush()

    # close the shared memory
    shm.close()
    shm.unlink()


def main() -> None:
    # the max of worker threads used to crop the image paralleling
    workers = 20

    # kafka configuration
    consumer_conf = {'bootstrap.servers': os.getenv('KAFKA_BROKER_HOSTNAME', 'localhost:19092'),
                     'auto.offset.reset': 'earliest',
                     'group.id': "ares-group"}
    producer_conf = {'bootstrap.servers': os.getenv('KAFKA_BROKER_HOSTNAME', 'localhost:19092')}

    # consumer topic
    consumer_topic = 'hera.plot-to-crops'

    # the kafka topic consumer
    consumer = Consumer(consumer_conf)

    # the kafka topic producer
    producer = Producer(producer_conf)

    running = True

    # create executor
    with ThreadPoolExecutor(max_workers=workers) as executor:
        try:
            # subscribe in the topic to consume
            consumer.subscribe([consumer_topic])

            while running:
                # poll for a message
                msg = consumer.poll(timeout=1.0)

                if msg is None:
                    continue

                # handle Error
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # end of partition event
                        sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                         (msg.topic(), msg.partition(), msg.offset()))

                elif msg.error():
                    raise KafkaException(msg.error())
                else:
                    # handle message
                    raw = json.loads(msg.value().decode('utf-8'))
                    message = CropMessage(**raw)

                    print(f"Message: {message}")

                    path = Path(message.path)
                    id: str = message.id

                    if path.exists() is False or path.is_file() is False:
                        producer.produce(
                            'hera.crop-failed',
                            json.dumps({
                                "id": id,
                                "cause": "The path must be a valid file."
                            }).encode('utf-8'))
                        continue

                    chop(path, id, producer, executor=executor)
        finally:
            # close down consumer to commit final offsets.
            consumer.close()


if __name__ == "__main__":
    main()
