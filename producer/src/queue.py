
import json
from schema import NormalizedWeatherData
from logger import logger


def send_data_to_message_queue(data: NormalizedWeatherData):
    logger.info("Sending data to queue")
    
    with open("./output.json", "w") as file:
        file.write(json.dumps(data, indent=4))
        
    logger.info("Data sent successfully")