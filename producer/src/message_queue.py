
import json
import pika
from schema import NormalizedWeatherData
from logger import logger
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")
QUEUE_HOST = os.environ.get("RABBITMQ_HOST")
QUEUE_NAME = os.environ.get("MESSAGE_QUEUE_NAME")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=QUEUE_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

def send_data_to_message_queue(data: NormalizedWeatherData):
    logger.info("Sending data to queue")
    
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=json.dumps(data)) 
        
    logger.info("Data sent successfully")
   
    
def close_message_queue_connection():
    channel.close()