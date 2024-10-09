import redis

class RedisConnectionHandler:
    def __init__(self, host, port, db):
        self.__host = host
        self.__port = port
        self.__db = db
        
    def make_connection(self):
        return redis.Redis(
            host=self.__host,
            port=self.__port,
            db=self.__db
        )