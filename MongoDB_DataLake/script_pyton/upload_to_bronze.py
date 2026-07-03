from dotenv import load_dotenv
import os
from azure.storage.filedatalake import DataLakeServiceClient
from pymongo import MongoClient
import json

load_dotenv("MongoDB_DataLake/azure_credential.env")
ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")

try:
    ACCOUNT_URL = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"

    service_client = DataLakeServiceClient(
    account_url=ACCOUNT_URL,
    credential=ACCOUNT_KEY
    )

    print("Connected successfully!")

    file_system_client = service_client.get_file_system_client(
    file_system="bronze"
    )

except Exception as e:
    print(f"Azure error detail: {e}")

load_dotenv("MongoDB_DataLake/credentials.env")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

try:
    uri = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/'
    client = MongoClient(uri)
    print("Connected successfully to MongoDB Atlas!")

    db = client["bank_db"]
    transactions = db["transactions"]

    documents = list(transactions.find({}, {"_id": 0}))

    json_data = json.dumps(
    documents,
    indent=4,
    default=str
    )

    directory_client = file_system_client.get_directory_client("mongodb")

    directory_client.create_directory()

    file_client = directory_client.create_file("transactions.json")

    file_client.append_data(
    data=json_data,
    offset=0,
    length=len(json_data)
    )

    file_client.flush_data(len(json_data))

except Exception as e:
    print(f"MongoDB error detail: {e}")





