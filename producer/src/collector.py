import requests
from typing import List

from src.dto import WeatherApiResponse
from src.logger import logger
from src.config import config
from src.mapper import mapper


class WeatherDataCollector:
    base_url: str
    latitude: float
    longitude: float
    timezone: str

    options: List[str]

    def __init__(self):
        self.base_url = config.BASE_URL
        self.latitude = config.LATITUDE
        self.longitude = config.LONGITUDE
        self.timezone = config.TIMEZONE

        self.options = [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "is_day",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "wind_gusts_10m",
        ]

    def build_url(self) -> str:
        current = str.join(",", self.options)

        query_params = f"?latitude={self.latitude}&longitude={self.longitude}&current={current}&timezone={self.timezone}"

        return f"{self.base_url}{query_params}"

    def get_data(self) -> WeatherApiResponse | None:
        logger.info(f"Requesting weather data from {self.base_url}")
        logger.info(f"Data source options {self.options}")

        response = requests.get(url=self.build_url())

        if response.status_code != 200:
            return None

        data = response.json()

        return mapper.map_json_response(data)
