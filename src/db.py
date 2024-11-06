from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
from models.settings import settings


class DatabaseConnection:
    _client: MongoClient = None

    @classmethod
    def connect(cls):
        if cls._client is None:
            try:
                # Construct the connection string with authentication
                connection_string = (
                    f"mongodb://{settings.MONGO_USER}:{settings.MONGO_PASSWORD}@"
                    f"{settings.MONGO_HOST}:{settings.MONGO_PORT}/{settings.MONGO_DATABASE}?authSource=admin"
                )
                cls._client = MongoClient(connection_string)
                # Test the connection
                cls._client.admin.command('ping')
                print("Successfully connected to MongoDB")
            except ConnectionFailure as exc:
                print(f'Exception while connecting to database: {exc}')
                raise

    @classmethod
    def get_database(cls, name: str):
        if cls._client is None:
            cls.connect()
        return cls._client[name]

    @classmethod
    def close(cls):
        if cls._client is not None:
            cls._client.close()


database = DatabaseConnection.get_database(settings.MONGO_DATABASE)