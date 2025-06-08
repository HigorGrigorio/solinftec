# -----------------------------------------------------------------------------
# (C) 2025 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

import json
import sys
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf
from confluent_kafka import Consumer, KafkaError, KafkaException, Producer

import models
from constants import HEIGHT, WIDTH, MODEL, KAFKA_BROKER_PORT, KAFKA_BROKER_HOSTNAME

prealloc_img = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
input_buffer = np.zeros((1, HEIGHT, WIDTH, 3), dtype=np.float32)

model = tf.keras.models.load_model(
    MODEL,
    compile=False,
    custom_objects={'TrajGRUCell': 'TrajGRUCell', 'TrajGRU': 'TrajGRU'}
)


def segmentation(path: Path) -> np.ndarray:
    # read the image
    img = cv2.imread(path)

    if img is None:
        print(f"Failed to load image from {path}")
        return None

    # 4. Re-use the pre-allocated array for resizing.
    #    Here we use `dst=prealloc_img` to store the resized result *into* the prealloc_img.
    cv2.resize(img, (WIDTH, HEIGHT), dst=prealloc_img)

    # 5. Convert BGR->RGB if your model was trained on RGB
    # cv2.cvtColor(prealloc_img, cv2.COLOR_BGR2RGB, dst=prealloc_img)

    # 6. Convert to float32 [0..1] and store into the input buffer
    #    We do this in-place, so no new array is allocated
    input_buffer[0] = prealloc_img.astype(np.float32) / 255.0

    # 7. Run the model
    return model.predict(input_buffer)


def main():
    # kafka configuration
    consumer_conf = {'bootstrap.servers': f'{KAFKA_BROKER_HOSTNAME}:{KAFKA_BROKER_PORT}',
                     'auto.offset.reset': 'earliest',
                     'group.id': "ares-group"}
    producer_conf = {'bootstrap.servers': f'{KAFKA_BROKER_HOSTNAME}:{KAFKA_BROKER_PORT}'}
    consumer_topic = 'hera.segmentation'

    # the kafka topic consumer
    consumer = Consumer(consumer_conf)

    # the kafka topic producer
    producer = Producer(producer_conf)

    running = True

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
                message = models.SegmentationMessage(**raw)

                print(f"Message: {message}")

                path = Path(message.path)
                id: str = message.id

                if path.exists() is False or path.is_file() is False:
                    producer.produce(
                        'hera.segmentation-error',
                        json.dumps(
                            {
                                "id": id,
                                "cause": "The path must be a valid file."
                            }
                        ).encode('utf-8'))
                    continue

                # segmentation
                try:
                    result = segmentation(path)

                    if result is None:
                        producer.produce(
                            'hera.segmentation-error',
                            json.dumps({
                                "id": id,
                                "cause": "could not segment the image"
                            }).encode('utf-8')
                        )
                        continue
                except ValueError as e:
                    producer.produce(
                        'hera.segmentation-error',
                        json.dumps({"id": id, "cause": str(e)}).encode('utf-8')
                    )
                    continue

                # save the image
                output_path = path.parent / path.name.replace(path.suffix, '') / 'mask.png'

                cv2.imwrite(str(output_path), result[0] * 255)
                producer.produce(
                    'hera.segmentation-result',
                    json.dumps({"id": id, "path": str(output_path)}).encode('utf-8')
                )

                producer.flush()
    finally:
        # close down consumer to commit final offsets.
        consumer.close()


if __name__ == '__main__':
    main()
