import json
from dataclasses import asdict

from src.dto import WeatherApiResponse, NormalizedWeatherData
from src.mapper import mapper


class TestMapper:
    weather_data: WeatherApiResponse
    normalized_data: NormalizedWeatherData

    def load_mock_data(self):
        with open("./tests/mocks/weather_data.json") as file:
            self.weather_data = mapper.map_json_response(json.load(file))

        with open("./tests/mocks/normalized_weather_data.json") as file:
            self.normalized_data = NormalizedWeatherData(**json.load(file))

    def test_should_normalize_weather_data_correctly(self):
        self.load_mock_data()

        normalized = mapper.normalize_data(self.weather_data)

        assert asdict(normalized) == asdict(self.normalized_data)
