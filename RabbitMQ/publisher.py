import pika
import json


class RabbitMQPublisher():
    def __init__(self):
        self.__host = 'localhost'
        self.__port = 5672
        self.__username = 'guest'
        self.__password = 'guest'
        self.__queue = 'my_queue'
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
        
        
        return channel
    
    def publish_message(self, message):
        self.__channel.basic_publish(
            exchange='my_exchange',
            routing_key='RK',
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2
            )
        )
        
            

    