# -----------------------------------------------------------------------------
# (C) 2023 Higor Grigorio (higorgrigorio@gmail.com)  (MIT License)
# -----------------------------------------------------------------------------

from confluent_kafka.admin import AdminClient, NewTopic
from fastapi import FastAPI

from config.enviroment import get_environment_variables
from config.subscribers import setup_subscribers
from infra.http.routes.v1 import V1Router
from infra.schemas.sqlalchemy import init

modules = [
    'crop',
    'plot',
]

topics = [
    # hera topics
    'hera.plot-to-crops',

    # ares related topics
    'hera.crop-created',
    'hera.crop-failed',
    'hera.crop-succeeded',

    # laquesis related topics
    'hera.segmentation',
    'hera.segmentation-failed',
    'hera.segmentation-succeeded',
]

# configure the kafka topics to be used
admin = AdminClient({
    'bootstrap.servers': f"{get_environment_variables().KAFKA_BROKER_HOSTNAME}:{get_environment_variables().KAFKA_BROKER_PORT}"
})

existent_topics = admin.list_topics().topics.keys()
not_existent_topics = [topic for topic in topics if topic not in existent_topics]
new_topics = [NewTopic(topic, num_partitions=1, replication_factor=1) for topic in not_existent_topics]

if new_topics:
    admin.create_topics(new_topics)
    print(f'Created topics: {not_existent_topics}')

app = FastAPI()

app.include_router(V1Router, prefix='/api')

# initialize the sqlalchemy models
init()

# set up the event subscribers
setup_subscribers(modules)

# set up kafka consumers
for module in modules:
    # if has infra/kafka/consumers.py
    try:
        module_consumer = __import__(f'modules.{module}.infra.kafka.consumers', fromlist=[''])

        if '__all__' not in module_consumer.__dict__:
            print(f'No consumers found in {module}')
            continue

        for consumer in module_consumer.__all__:
            # use FastAPI dependency injection to get the consumer instance
            consumer_instance = consumer()
            consumer_instance.setup()

    except ModuleNotFoundError:
        pass
    except Exception as e:
        print(f'Error setting up kafka consumers for {module}: {e}')
        continue
