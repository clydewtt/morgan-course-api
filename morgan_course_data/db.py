from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://read:xtUxRpHUrVMhNI8T@courses.oqzo0.mongodb.net/?retryWrites=true&w=majority&appName=courses"


def get_db_connection(db_name):
    """
    Connect to MongoDB and return the database instance.
    """
    client = MongoClient(uri, server_api=ServerApi("1"))
    return client[db_name]
