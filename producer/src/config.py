from dotenv import load_dotenv
from dataclasses import dataclass
import os


@dataclass
class ConfigEnvs:
    BASE_URL: str
    LATITUDE: float
    LONGITUDE: float
    TIMEZONE: str
    QUEUE_HOST: str
    QUEUE_PORT: int
    QUEUE_NAME: str
    QUEUE_USER: str
    QUEUE_PASS: str


class Config(ConfigEnvs):
    def __init__(self):
        load_dotenv()

        super().__init__(
            BASE_URL=os.environ.get("DATA_SOURCE_BASE_URL", ""),
            QUEUE_HOST=os.environ.get("RABBITMQ_HOST", ""),
            QUEUE_PORT=int(os.environ.get("RABBITMQ_PORT", 5672)),
            QUEUE_NAME=os.environ.get("RABBITMQ_QUEUE_NAME", ""),
            QUEUE_USER=os.environ.get("RABBITMQ_USER", ""),
            QUEUE_PASS=os.environ.get("RABBITMQ_PASS", ""),
            LATITUDE=float(os.environ.get("LATITUDE", 0.0)),
            LONGITUDE=float(os.environ.get("LONGITUDE", 0.0)),
            TIMEZONE=os.environ.get("TIMEZONE", "UTC"),
        )


config = Config()
