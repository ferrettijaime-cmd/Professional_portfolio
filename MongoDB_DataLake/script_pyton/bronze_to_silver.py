from pyspark.sql.functions import col

import os

from dotenv import load_dotenv
from azure.storage.filedatalake import DataLakeServiceClient

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("MongoDB_DataLake_Project")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

load_dotenv(r"C:\Professional_project\MongoDB_DataLake\credentials.env")

ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")

ACCOUNT_URL = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"

service_client = DataLakeServiceClient(
    account_url=ACCOUNT_URL,
    credential=ACCOUNT_KEY
)

file_system_client = service_client.get_file_system_client("bronze")
directory_client = file_system_client.get_directory_client("mongodb")

files = list(directory_client.get_paths())

latest_file = max(
    files,
    key=lambda x: x.last_modified
)

download_path = r"C:\Professional_project\MongoDB_DataLake\temp\bronze\transactions.json"

file_client = file_system_client.get_file_client(latest_file.name)

download = file_client.download_file()

with open(download_path, "wb") as f:
    f.write(download.readall())

print("Download completed!")

df = spark.read.json(download_path)

df_silver = df.select(
    col("step"),

    col("transaction.amount").alias("transaction_amount"),
    col("transaction.type").alias("transaction_type"),

    col("origin_account.account_id").alias("origin_account_id"),
    col("origin_account.balance_before").alias("origin_balance_before"),
    col("origin_account.balance_after").alias("origin_balance_after"),

    col("destination_account.account_id").alias("destination_account_id"),
    col("destination_account.balance_before").alias("destination_balance_before"),
    col("destination_account.balance_after").alias("destination_balance_after"),

    col("fraud.is_fraud").alias("is_fraud"),
    col("fraud.is_flagged").alias("is_flagged")
)

silver_path = r"C:\Professional_project\MongoDB_DataLake\temp\silver"

df_silver.write \
    .mode("overwrite") \
    .parquet(silver_path)

print("Parquet files created successfully!")

silver_container = service_client.get_file_system_client("silver")

try:
    silver_directory = silver_container.get_directory_client("transactions")
    silver_directory.create_directory()
except:
    silver_directory = silver_container.get_directory_client("transactions")

local_silver_path = r"C:\Professional_project\MongoDB_DataLake\temp\silver"

for file_name in os.listdir(local_silver_path):

    # Solo subir archivos Parquet
    if file_name.endswith(".parquet"):

        local_file = os.path.join(local_silver_path, file_name)

        file_client = silver_directory.create_file(file_name)

        with open(local_file, "rb") as f:
            data = f.read()

        file_client.append_data(
            data=data,
            offset=0,
            length=len(data)
        )

        file_client.flush_data(len(data))

        print(f"{file_name} uploaded successfully!")

print("All Parquet files uploaded successfully!")