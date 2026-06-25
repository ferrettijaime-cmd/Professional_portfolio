import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

load_dotenv("/opt/airflow/ml_forecasting_db.env")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

url = URL.create(
    drivername="postgresql+psycopg2",
    username=user,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = None

try:
    engine = create_engine(url)
    query= """
          select *
          from features.features_engineering
    """
    ml_df = pd.read_sql(query, con=engine)

    x = ml_df.drop("revenue", axis=1)
    y = ml_df["revenue"]

    train_size = int(len(x)*0.80)

    X_train = x.iloc[:train_size]
    X_test = x.iloc[train_size:]

    y_train = y.iloc[:train_size]
    y_test = y.iloc[train_size:]

    X_train.to_sql(
        name="x_train_dataset",
        con=engine,
        schema="features_training",
        if_exists="replace",
        index=False
    )
    X_test.to_sql(
        name="x_test_dataset",
        con=engine,
        schema="features_training",
        if_exists="replace",
        index=False
    )
    y_train.to_sql(
        name="y_train_dataset",
        con=engine,
        schema="features_training",
        if_exists="replace",
        index=False
    )
    y_test.to_sql(
        name="y_test_dataset",
        con=engine,
        schema="features_training",
        if_exists="replace",
        index=False
    )

    print("The datasets were successfully loaded!!!")

except Exception as e:
    import traceback
    traceback.print_exc()

finally:
    if engine:
        engine.dispose()

