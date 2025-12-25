import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from schema import NormalizedWeatherData, WeatherApiResponse
from constants import (
    DATA_SOURCE_BASE_URL, 
    DATA_SOURCE_CURRENT_OPTIONS, 
    FORTALEZA_LATITUDE, 
    FORTALEZA_LONGITUDE,
    LOCAL_TIMEZONE,
    WEATHER_CODE_MAP
)
from logger import logger
from queue import send_data_to_message_queue

def get_weather_data() -> WeatherApiResponse:
    current_params = str.join(',', DATA_SOURCE_CURRENT_OPTIONS)
    
    query_params = f'?latitude={FORTALEZA_LATITUDE}&longitude={FORTALEZA_LONGITUDE}&current={current_params}&timezone={LOCAL_TIMEZONE}' 
    
    logger.info(f"Requesting weather data from {DATA_SOURCE_BASE_URL}")
    logger.info(f"Query params used: ${query_params}")
    
    response = requests.get(f'{DATA_SOURCE_BASE_URL}{query_params}')    
    
    if response.status_code != 200:
        logger.error(f"Failed to fetch data from {DATA_SOURCE_BASE_URL}")
        raise RuntimeError("Failed to fetch data from source")  
    
    return response.json()


def map_weather_code(code: int) -> str:
    try:    
        return WEATHER_CODE_MAP[code]
    except KeyError:
        return 'unknown_weather_code'

def format_timestamp(time_str: str, timezone: str = LOCAL_TIMEZONE) -> str:
   raw_timestamp = datetime.fromisoformat(time_str)
   
   timestamp = raw_timestamp.replace(tzinfo=ZoneInfo(timezone))
   
   return timestamp.isoformat()


def normalize_data(data: WeatherApiResponse) -> NormalizedWeatherData:
    logger.info("Normalizing data collected from source")
    data = {
        "latitude": data['latitude'],
        "longitude": data['longitude'],
        "elevation": data['elevation'],
        "temperature_2m": data["current"]["temperature_2m"],
        "relative_humidity_2m": data["current"]["relative_humidity_2m"],
        "apparent_temperature": data["current"]["apparent_temperature"],
        "is_day": bool(data["current"]["is_day"]),
        "precipitation": data["current"]["precipitation"],
        "weather_type": map_weather_code(data["current"]["weather_code"]),
        "wind_speed_10m": data["current"]["wind_speed_10m"],
        "wind_direction_10m": data["current"]["wind_direction_10m"],
        "wind_gusts_10m": data["current"]["wind_gusts_10m"],
        "extracted_at": format_timestamp(data["current"]['time'], data["timezone"]),
    }
    logger.info("Data normalized successfully")
    return data


def main():
    try:
        data = get_weather_data()
        
        normalized_data = normalize_data(data)

        send_data_to_message_queue(normalized_data)
            
    except RuntimeError as error:
        logger.error(str(error))

if __name__ == "__main__":
    main()
