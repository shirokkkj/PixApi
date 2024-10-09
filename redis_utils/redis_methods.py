from redis import Redis

class RedisMethodsHandler:
    def __init__(self, redis_connection: Redis):
        self.__con = redis_connection
        
    def insert(self, key, value):
        self.__con.set(key, value)
        
    def get_value(self, key):
        self.__con.get(key)