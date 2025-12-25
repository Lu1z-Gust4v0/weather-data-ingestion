from typing import TypedDict

class CurrentUnits(TypedDict):
    time: str
    interval: str
    temperature_2m: str
    relative_humidity_2m: str
    apparent_temperature: str
    is_day: str
    precipitation: str
    weather_code: str
    wind_speed_10m: str
    wind_direction_10m: str
    wind_gusts_10m: str
    
class CurrentData(TypedDict):
    time: str
    interval: int
    temperature_2m: float
    relative_humidity_2m: int
    apparent_temperature: float
    is_day: int
    precipitation: int
    weather_code: int
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float
    
class WeatherApiResponse(TypedDict):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current_units: CurrentUnits
    current: CurrentData
    
class NormalizedWeatherData(TypedDict):
    latitude: float
    longitude: float
    elevation: float
    temperature_2m: float
    relative_humidity_2m: int
    apparent_temperature: float
    is_day: bool
    precipitation: int
    weather_type: str
    wind_speed_10m: float
    wind_direction_10m: int
    wind_gusts_10m: float
    extracted_at: str