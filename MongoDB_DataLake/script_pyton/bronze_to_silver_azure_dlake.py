import os
from dotenv import load_dotenv

from azure.storage.filedatalake import DataLakeServiceClient

from pyspark.sql import SparkSession

spark = (
    SparkSession.builder
    .appName("Silver_to_Gold_Data_Lake")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

load_dotenv(r"C:\Professional_project\MongoDB_DataLake\credentials.env")

ACCOUNT_NAME = os.getenv("AZURE_STORAGE_ACCOUNT")
ACCOUNT_KEY = os.getenv("AZURE_STORAGE_KEY")

ACCOUNT_URL = f"https://{ACCOUNT_NAME}.dfs.core.windows.net"

path =(
    r"C:\Professional_project\MongoDB_DataLake\temp\gold\fact_transactions"
)

try:
    service_client = DataLakeServiceClient(
    account_url=ACCOUNT_URL,
    credential=ACCOUNT_KEY
    )

    print("Connected successfully to Azure!")

    gold_container = service_client.get_file_system_client("gold")

    try:
        gold_directory = gold_container.get_directory_client("fact_transactions")
        gold_directory.create_directory()
    except:
        gold_directory = gold_container.get_directory_client("fact_transactions")

    try:
        delta_directory = gold_container.get_directory_client("fact_transactions/_delta_log")
        delta_directory.create_directory()
    except:
        delta_directory = gold_container.get_directory_client("fact_transactions/_delta_log")

    for root, dirs, files in os.walk(path):

        for file in (files):
            if file.endswith(".parquet"):
                local_file = os.path.join(root, file)
                gold_file = gold_directory.create_file(file)

                with open(local_file, "rb") as f:
                    data = f.read()

                gold_file.append_data(
                data=data,
                offset=0,
                length=len(data)
                )

                gold_file.flush_data(len(data))
                print("The parquet files were successfully uploaded!")

            elif file.endswith(".json"):
                    local_file = os.path.join(root, file)
                    delta_file = delta_directory.create_file(file)

                    with open(local_file, "rb") as f:
                        data = f.read()

                    delta_file.append_data(
                    data=data,
                    offset=0,
                    length=len(data)
                    )

                    delta_file.flush_data(len(data))
                    print("The files were successfully uploaded")

except Exception as e:
    print(f"Error Details: {e}")

            





        

        


    

 








