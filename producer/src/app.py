import requests

from src.mapper import normalize_data
from src.schema import WeatherApiResponse
from src.constants import (
    DATA_SOURCE_BASE_URL,
    DATA_SOURCE_CURRENT_OPTIONS,
    FORTALEZA_LATITUDE,
    FORTALEZA_LONGITUDE,
    LOCAL_TIMEZONE,
)
from src.logger import logger
from src.message_queue import send_data_to_message_queue, close_message_queue_connection


def get_weather_data() -> WeatherApiResponse:
    current_params = str.join(",", DATA_SOURCE_CURRENT_OPTIONS)

    query_params = f"?latitude={FORTALEZA_LATITUDE}&longitude={FORTALEZA_LONGITUDE}&current={current_params}&timezone={LOCAL_TIMEZONE}"

    logger.info(f"Requesting weather data from {DATA_SOURCE_BASE_URL}")
    logger.info(f"Query params used: ${query_params}")

    response = requests.get(f"{DATA_SOURCE_BASE_URL}{query_params}")

    if response.status_code != 200:
        logger.error(f"Failed to fetch data from {DATA_SOURCE_BASE_URL}")
        raise RuntimeError("Failed to fetch data from source")

    return response.json()


def main():
    try:
        data = get_weather_data()

        normalized_data = normalize_data(data)

        send_data_to_message_queue(normalized_data)

        close_message_queue_connection()

    except RuntimeError as error:
        logger.error(str(error))


if __name__ == "__main__":
    main()
