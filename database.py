from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

# Load environment variables
load_dotenv(find_dotenv())

# Get MongoDB connection details from environment variables
mongo_username = os.environ.get("MONGO_USERNAME")
mongo_password = os.environ.get("MONGO_PASSWORD")
mongo_cluster = os.environ.get("MONGO_CLUSTER")

# Construct the connection string
connection_string = f"mongodb+srv://{mongo_username}:{mongo_password}@{mongo_cluster}"

try:
    # Connect to MongoDB
    client = MongoClient(connection_string)
    
    # Get or create a database
    db = client["mydatabase"]
    
    # Get or create a collection
    collection = db["mycollection"]
    
    # Insert a document
    document = {"name": "John Deep", "age": 30}
    collection.insert_one(document)
    
    # Query the collection
    results = collection.find()
    for doc in results:
        print(doc)
        
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")