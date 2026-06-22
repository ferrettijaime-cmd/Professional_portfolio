from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

base_dir = Path(__file__).resolve().parent.parent.parent
file = base_dir / "ml_forecasting_db.env"

load_dotenv(file)
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
    query="""
          select *
          from
              raw.revenue_dataset
    """
    features = pd.read_sql(query, con=engine)
    print("The dataset was successfully extracted!!!")

    features["order_day"] = pd.to_datetime(features["order_day"])

    features["day_of_week"] = features["order_day"].dt.day_of_week
    features["is_weekend"] = (features["order_day"].dt.day_of_week >=5).astype(int)
    features["lag_7"] = features["revenue"].shift(7)
    features["rolling_mean_7"] =(
    features["revenue"]
    .rolling(7)
    .mean()
    )
    features["lag_14"] = features["revenue"].shift(14)
    features["rolling_mean_14"] =(
    features["revenue"]
    .rolling(14)
    .mean()
    )

    features.dropna(inplace=True)

    features.to_sql(
        name="features_engineering",
        con=engine,
        schema="features",
        if_exists="replace",
        index=False
    )
    print("The dataset was successfully loaded!!!")

except Exception as e:
    import traceback
    traceback.print_exc()

finally:
    if engine:
        engine.dispose()








