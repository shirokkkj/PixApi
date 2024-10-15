import pika
import json

class RabbitMQConsumer():
    def __init__(self, callback):
        self.__host = 'localhost'
        self.__port = 5672
        self.__username = 'guest'
        self.__password = 'guest'
        self.__queue = 'my_queue'
        self.__callback = callback
        self.__channel = self.create_channel()
        
    def create_channel(self):
        connection_parameters = pika.ConnectionParameters(
        host = self.__host,
        port=self.__port,
        credentials=pika.PlainCredentials(
            username=self.__username,
            password=self.__password
        )
        
    )

        channel = pika.BlockingConnection(connection_parameters).channel()

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )

        channel.basic_consume(
            queue='my_queue',
            auto_ack=True,
            on_message_callback=self.__callback
        )
        
        return channel
    
    def start(self):
        print('RabbitMQ listening in port 5672')
        self.__channel.start_consuming()
        
        

    
