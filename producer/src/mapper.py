from datetime import datetime
from venv import logger
from zoneinfo import ZoneInfo
from src.constants import LOCAL_TIMEZONE, WEATHER_CODE_MAP
from src.schema import NormalizedWeatherData, WeatherApiResponse


def map_weather_code(code: int) -> str:
    try:
        return WEATHER_CODE_MAP[code]
    except KeyError:
        return "unknown_weather_code"


def format_timestamp(time_str: str, timezone: str = LOCAL_TIMEZONE) -> str:
    raw_timestamp = datetime.fromisoformat(time_str)

    timestamp = raw_timestamp.replace(tzinfo=ZoneInfo(timezone))

    return timestamp.isoformat()


def normalize_data(data: WeatherApiResponse) -> NormalizedWeatherData:
    logger.info("Normalizing data collected from source")
    data = {
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "elevation": data["elevation"],
        "temperature_2m": data["current"]["temperature_2m"],
        "relative_humidity_2m": data["current"]["relative_humidity_2m"],
        "apparent_temperature": data["current"]["apparent_temperature"],
        "is_day": bool(data["current"]["is_day"]),
        "precipitation": data["current"]["precipitation"],
        "weather_type": map_weather_code(data["current"]["weather_code"]),
        "wind_speed_10m": data["current"]["wind_speed_10m"],
        "wind_direction_10m": data["current"]["wind_direction_10m"],
        "wind_gusts_10m": data["current"]["wind_gusts_10m"],
        "extracted_at": format_timestamp(data["current"]["time"], data["timezone"]),
    }
    logger.info("Data normalized successfully")
    return data
