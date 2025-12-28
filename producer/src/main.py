from src.collector import WeatherDataCollector
from src.mapper import mapper
from src.message_queue import MessageQueueClient
from src.logger import logger


def main():
    try:
        queue_client = MessageQueueClient()

        queue_client.connect()

        data = WeatherDataCollector().get_data()

        if not data:
            raise RuntimeError("Failed to fetch weather data")

        normalized_data = mapper.normalize_data(data)

        queue_client.send_data(normalized_data)

        queue_client.close()

    except RuntimeError as error:
        logger.error(error)


if __name__ == "__main__":
    main()
