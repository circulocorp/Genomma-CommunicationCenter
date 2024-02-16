import pika
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from system.settings import (RABBIT_MQ_HOST, RABBIT_MQ_DEFAULT_QUEUE, RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)


class RabbitMQConfiguration:
    def __init__(self, host=RABBIT_MQ_HOST, queue_name=RABBIT_MQ_DEFAULT_QUEUE):
        credentials = pika.PlainCredentials(RABBIT_MQ_USERNAME, RABBIT_MQ_PASSWORD)
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host, port=5672, credentials=credentials, virtual_host='lmjbfdtx'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)
        self.queue_name = queue_name

    def send_message(self, message):
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        print(f" [x] Sent {message}")

    def receive_message(self, callback):
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close_connection(self):
        self.connection.close()
        print('Connection closed')