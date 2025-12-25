import json
from pika import BlockingConnection, ConnectionParameters

from src.constants import QUEUE_HOST, QUEUE_NAME
from src.schema import NormalizedWeatherData
from src.logger import logger


def connect_to_message_queue() -> BlockingConnection:
    connection = BlockingConnection(ConnectionParameters(host=QUEUE_HOST))

    connection.channel().queue_declare(queue=QUEUE_NAME)

    return connection


def send_data_to_message_queue(
    connection: BlockingConnection, data: NormalizedWeatherData
):
    logger.info("Sending data to queue")

    connection.channel().basic_publish(
        exchange="", routing_key=QUEUE_NAME, body=json.dumps(data)
    )

    logger.info("Data sent successfully")


def close_message_queue_connection(connection: BlockingConnection):
    connection.channel().close()
