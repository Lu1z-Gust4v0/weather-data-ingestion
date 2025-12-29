import json
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from pika.credentials import PlainCredentials
from dataclasses import asdict

from src.dto import NormalizedWeatherData
from src.logger import logger
from src.config import config


class MessageQueueClient:
    queue_host: str
    queue_port: int
    queue_user: str
    queue_pass: str
    queue_name: str

    channel: BlockingChannel | None

    def __init__(self):
        self.queue_host = config.QUEUE_HOST
        self.queue_port = config.QUEUE_PORT
        self.queue_name = config.QUEUE_NAME
        self.queue_user = config.QUEUE_USER
        self.queue_pass = config.QUEUE_PASS

    def connect(self):
        try:
            logger.info(f"Connecting to message queue {self.queue_host}")

            connection = BlockingConnection(
                ConnectionParameters(
                    host=self.queue_host,
                    port=self.queue_port,
                    credentials=PlainCredentials(
                        username=self.queue_user, password=self.queue_pass
                    ),
                )
            )

            channel = connection.channel()

            logger.info(f"Declaring queue {self.queue_name}")
            channel.queue_declare(queue=self.queue_name, durable=True)

            logger.info("Connected successfully")
            self.channel = channel

        except AMQPConnectionError:
            raise RuntimeError(f"Failed to connect to queue {self.queue_host}")

    def send_data(self, data: NormalizedWeatherData):
        logger.info("Sending data to queue")

        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=json.dumps(asdict(data))
        )

        logger.info("Data sent successfully")

    def close(self):
        logger.info("Closing connection")

        self.channel.close()

        logger.info("Connection closed")
