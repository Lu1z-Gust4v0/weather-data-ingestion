import json
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError
from dataclasses import asdict

from src.dto import NormalizedWeatherData
from src.logger import logger
from src.config import config


class MessageQueueClient:
    queue_host: str
    queue_name: str

    channel: BlockingChannel | None

    def __init__(self):
        self.queue_host = config.QUEUE_HOST
        self.queue_name = config.QUEUE_NAME

    def connect(self):
        try:
            logger.info(f"Connecting to message queue {self.queue_host}")

            connection = BlockingConnection(ConnectionParameters(host=self.queue_host))
            channel = connection.channel()

            logger.info(f"Declaring queue {self.queue_name}")
            channel.queue_declare(queue=self.queue_name)

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
