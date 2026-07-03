
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

def load_random_sample(path, chunksize=50000, frac=0.03, random_state=42):
    """
    Reads a large CSV file in chunks and returns a random sample.

    Parameters
    ----------
    path : str
        Path to the CSV file.
    chunksize : int, optional
        Number of rows to read per chunk.
    frac : float, optional
        Fraction of rows to randomly sample from each chunk.
    random_state : int, optional
        Seed for reproducibility.

    Returns
    -------
    pandas.DataFrame
        Random sample of the original dataset.
    """

    sampled_chunks = []

    for chunk in pd.read_csv(path, chunksize=chunksize):

        sample = chunk.sample(
            frac=frac,
            random_state=random_state
        )

        sampled_chunks.append(sample)

    df = pd.concat(sampled_chunks, ignore_index=True)

    return df

df = load_random_sample(
    r"C:\Data_Base\Bank_dataset\dataset.csv"
)

load_dotenv("NoSQL_MongoDB/credentials.env")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_CLUSTER = os.getenv("MONGO_CLUSTER")

try:
    uri = f'mongodb+srv://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_CLUSTER}/'

    client = MongoClient(uri)
    print("Connected successfully to MongoDB Atlas!")

    db = client["bank_db"]
    transactions = db["transactions"]

    documents = []

    for _, row in df.iterrows():

        document = {

            "step": row["step"],

            "transaction": {
            "type": row["type"],
            "amount": row["amount"]
            },

            "origin_account": {
            "account_id": row["nameOrig"],
            "balance_before": row["oldbalanceOrg"],
            "balance_after": row["newbalanceOrig"]
            },

            "destination_account": {
            "account_id": row["nameDest"],
            "balance_before": row["oldbalanceDest"],
            "balance_after": row["newbalanceDest"]
            },

            "fraud": {
            "is_fraud": bool(row["isFraud"]),
            "is_flagged": bool(row["isFlaggedFraud"])
            }

        }

        documents.append(document)

        if len(documents) == 5000:
            transactions.insert_many(documents)

            documents = []

    if documents:
        transactions.insert_many(documents)
        print("Documents inserted successfully!")
        

except Exception as e:
    print(f'Error datail ---> {e}')

finally:
    client.close()
    print("Connection closed.")


