import os
import json
from datetime import datetime

from dotenv import load_dotenv
from pymongo import MongoClient
from azure.storage.filedatalake import DataLakeServiceClient

load_dotenv("MongoDB_DataLake/credentials.env")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")
ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")

try:
    uri = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/'
    client = MongoClient(uri)
    print("Connected successfully to MongoDB Atlas!")

    ACCOUNT_URL = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"

    service_client = DataLakeServiceClient(
    account_url=ACCOUNT_URL,
    credential=ACCOUNT_KEY
    )

    print("Connected successfully to Azure!")

except Exception as e:
    print(f"Connection error: {e}")

try:
    db = client["bank_db"]
    transactions = db["transactions"]

    documents = list(transactions.find({}, {"_id": 0}))
    print(f"{len(documents)} documents extracted.")

    file_system_client = service_client.get_file_system_client("bronze")

    directory_client = file_system_client.get_directory_client("mongodb")

    try:
        directory_client.create_directory()
    except:
        pass

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = f"transactions_{timestamp}.json"

    file_client = directory_client.create_file(filename)

    ndjson = "\n".join(
        json.dumps(doc, default=str)
        for doc in documents
    )

    file_client.append_data(
        data=ndjson,
        offset=0,
        length=len(ndjson)
    )

    file_client.flush_data(len(ndjson))

    print(f"File '{filename}' uploaded successfully!")

except Exception as e:
    print(e)





