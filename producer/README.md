# Data Producer ✅

A lightweight data producer that fetches current weather data from the Open-Meteo API, normalizes the response, and publishes the normalized payload to a RabbitMQ message queue.

---

## How it works 🔧

- The main entrypoint is `src/app.py` which:

  1. Requests current weather data (latitude/longitude are set in `src/constants.py`) from the Open-Meteo API.
  2. Normalizes the API response using `src/mapper.py` (maps codes, formats timestamps, and selects relevant fields).
  3. Publishes the normalized data to a RabbitMQ queue via `src/message_queue.py`.
  4. Logs progress and errors using `src/logger.py`.

- Data schemas are described in `src/schema.py` (`WeatherApiResponse` and `NormalizedWeatherData`).

---

## Configuration ⚙️

Create a `.env` file at the project root with the following variables:

```env
RABBITMQ_HOST=localhost
MESSAGE_QUEUE_NAME=weather
```

`src/message_queue.py` loads the `.env` file (it expects it one directory up from `src/`).

---

## Running locally ▶️

1. Install dependencies with Poetry:

```bash
poetry install
```

2. Start RabbitMQ (Docker compose):

```bash
# Run in the project source
docker compose up rabbitmq
```

3. Run the producer:

```bash
poetry run start
# or
python -m src.app
```

The producer will fetch the latest weather data, normalize it, and publish a JSON message to the queue named by `MESSAGE_QUEUE_NAME`.

---

## Testing 🧪

Run unit tests with:

```bash
poetry run pytest
```

Current tests live in `tests/` (for example, `tests/mapper_test.py`).

---

## Message format (normalized payload) 💬

The message published to the queue follows the `NormalizedWeatherData` shape (see `src/schema.py`) and includes fields such as:

- `latitude`, `longitude`, `elevation`
- `temperature_2m`, `relative_humidity_2m`, `apparent_temperature`
- `is_day`, `precipitation`, `weather_type`
- `wind_speed_10m`, `wind_direction_10m`, `wind_gusts_10m`
- `extracted_at` (ISO timestamp)

---
