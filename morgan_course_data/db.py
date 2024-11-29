from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://read:0kS4fcyXXOqWwSpt@coursedatacluster.r4jik.mongodb.net/?retryWrites=true&w=majority&appName=CourseDataCluster"

def get_db_connection(db_name):
    """
    Connect to MongoDB and return the database instance.
    """
    client = MongoClient(uri, server_api=ServerApi("1"))
    return client[db_name]
