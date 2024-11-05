from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables
load_dotenv(find_dotenv())

# Initialize MongoDB client
mongo_username = os.getenv("MONGO_USERNAME")
mongo_password = os.getenv("MONGO_PASSWORD")
mongo_cluster = os.getenv("MONGO_CLUSTER")
connection_string = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster}"

client = MongoClient(connection_string)
db = client["quest_Engine"]
collection = db["collection_one"]

def save_query_result(query, result, data_preview):
    """
    Saves a query result to MongoDB with all keys converted to strings.
    """
    # Convert data_preview keys to strings
    data_preview_str_keys = {str(k): v for k, v in data_preview.items()}

    # Document to be inserted
    doc = {
        "query": query,
        "result": result,
        "data_preview": data_preview_str_keys
    }

    collection.insert_one(doc)


def get_recent_results(limit=5):
    """
    Retrieves the most recent query results from MongoDB.
    """
    return list(collection.find().limit(limit))
