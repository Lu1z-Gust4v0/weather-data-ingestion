from src.schema import WeatherApiResponse, NormalizedWeatherData
from src.mapper import normalize_data
import json


class TestMapper:
    weather_data: WeatherApiResponse
    normalized_data: NormalizedWeatherData

    def load_mock_data(self):
        with open("./tests/mocks/weather_data.json") as file:
            self.weather_data = json.load(file)

        with open("./tests/mocks/normalized_weather_data.json") as file:
            self.normalized_data = json.load(file)

    def test_should_normalize_weather_data_correctly(self):
        self.load_mock_data()

        normalized = normalize_data(self.weather_data)

        assert normalized == self.normalized_data
