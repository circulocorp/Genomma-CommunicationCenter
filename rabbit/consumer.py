import requests
from rabbit_configuration import RabbitMQConfiguration
import json

def process_message(ch, method, properties, body):
    
    data = json.loads(body)
    
    print(f" [x] Received {data}")

rabbitmq_config = RabbitMQConfiguration()

try:
    rabbitmq_config.receive_message(process_message)
except KeyboardInterrupt:
    rabbitmq_config.close_connection()
