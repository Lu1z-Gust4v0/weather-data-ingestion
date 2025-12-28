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
    QUEUE_NAME: str


class Config(ConfigEnvs):
    def __init__(self):
        load_dotenv(dotenv_path="../.env")

        super().__init__(
            BASE_URL=os.environ.get("DATA_SOURCE_BASE_URL", ""),
            QUEUE_HOST=os.environ.get("RABBITMQ_HOST", ""),
            QUEUE_NAME=os.environ.get("MESSAGE_QUEUE_NAME", ""),
            LATITUDE=float(os.environ.get("LATITUDE", 0.0)),
            LONGITUDE=float(os.environ.get("LONGITUDE", 0.0)),
            TIMEZONE=os.environ.get("TIMEZONE", "UTC"),
        )


config = Config()
