from time import sleep
import pika

import logconf

logger = logconf.Logger(__name__)


def run():
    credentials = pika.PlainCredentials(
        "demo",
        "demo"
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host="rabbitmq-01",
            credentials=credentials,
            heartbeat_interval=60,
            socket_timeout=60,
        )
    )
    channel = connection.channel()

    arguments = dict()
    channel.queue_declare(
        queue="demo",
        auto_delete=False,
        durable=True,
        arguments=arguments
    )

    for i in range(0, 100):
        state = channel.basic_publish(
            exchange='',
            routing_key="demo",
            body=str(i)
        )
        logger.info(f"[x] send {i}")
        sleep(30)
