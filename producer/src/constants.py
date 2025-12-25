DATA_SOURCE_BASE_URL = "https://api.open-meteo.com/v1/"
FORTALEZA_LATITUDE = -3.731862
FORTALEZA_LONGITUDE = -38.526669
DATA_SOURCE_CURRENT_OPTIONS = [
    "temperature_2m",
    "relative_humidity_2m",
    "apparent_temperature",
    "is_day",
    "precipitation",
    "weather_code",
    "wind_speed_10m",
    "wind_direction_10m",
    "wind_gusts_10m"
]

LOCAL_TIMEZONE = 'America/Sao_Paulo'

WEATHER_CODE_MAP = {
    0: 'clear_sky',
    1: 'mainly_clear',
    2: 'partly_cloudy',
    3: 'overcast',
    45: 'fog',
    48: 'depositing_rime_fog',
    51: 'drizzle_light',
    53: 'drizzle_moderate',
    55: 'drizzle_dense',
    56: 'freezing_drizzle_light',
    57: 'freezing_drizzle_dense',
    61: 'rain_slight',
    63: 'rain_moderate',
    65: 'rain_heavy',
    66: 'freezing_rain_light',
    67: 'freezing_rain_heavy',
    71: 'snow_fall_slight',
    73: 'snow_fall_moderate',
    75: 'snow_fall_heavy',
    77: 'snow_grains',
    80: 'rain_showers_slight',
    81: 'rain_showers_moderate',
    82: 'rain_showers_violent',
    85: 'snow_showers_slight',
    86: 'snow_showers_heavy',
    95: 'thunderstorm',
    96: 'thunderstorm_with_slight_hail',
    99: 'thunderstorm_with_heavy_hail'
}