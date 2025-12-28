from datetime import datetime
from venv import logger
from zoneinfo import ZoneInfo
from src.constants import WEATHER_CODE_MAP

from typing import Dict

from src.dto import CurrentData, CurrentUnits, NormalizedWeatherData, WeatherApiResponse


class DataMapper:
    weather_code_map: Dict[int, str]

    def __init__(self):
        self.weather_code_map = WEATHER_CODE_MAP

    def map_json_response(self, data: Dict[str, str]) -> WeatherApiResponse:
        return WeatherApiResponse(
            latitude=data["latitude"],
            longitude=data["longitude"],
            generationtime_ms=data["generationtime_ms"],
            utc_offset_seconds=data["utc_offset_seconds"],
            timezone=data["timezone"],
            timezone_abbreviation=data["timezone_abbreviation"],
            elevation=data["elevation"],
            current_units=CurrentUnits(**data["current_units"]),
            current=CurrentData(**data["current"]),
        )

    def normalize_data(self, data: WeatherApiResponse) -> NormalizedWeatherData:
        logger.info("Normalizing data collected from source")

        normalized_data = {
            "latitude": data.latitude,
            "longitude": data.longitude,
            "elevation": data.elevation,
            "temperature_2m": data.current.temperature_2m,
            "relative_humidity_2m": data.current.relative_humidity_2m,
            "apparent_temperature": data.current.apparent_temperature,
            "is_day": bool(data.current.is_day),
            "precipitation": data.current.precipitation,
            "weather_type": self.map_weather_code(data.current.weather_code),
            "wind_speed_10m": data.current.wind_speed_10m,
            "wind_direction_10m": data.current.wind_direction_10m,
            "wind_gusts_10m": data.current.wind_gusts_10m,
            "extracted_at": self.format_timestamp(data.current.time, data.timezone),
        }

        logger.info("Data normalized successfully")

        return NormalizedWeatherData(**normalized_data)

    def map_weather_code(self, code: int) -> str:
        try:
            return self.weather_code_map[code]
        except KeyError:
            return "unknown_weather_code"

    def format_timestamp(self, time_str: str, timezone: str) -> str:
        raw_timestamp = datetime.fromisoformat(time_str)

        timestamp = raw_timestamp.replace(tzinfo=ZoneInfo(timezone))

        return timestamp.isoformat()


mapper = DataMapper()
