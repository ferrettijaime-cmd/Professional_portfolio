from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import pandas as pd

base_dir = Path(__file__).resolve().parent.parent
file = base_dir / ".neondb_credentials.env"

load_dotenv(file)
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

engine = None

try:
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")
    query="""
        select
            order_purchase_timestamp::date as order_day,
        sum(price) as revenue
        from
            analytics.fact_orders
        where 
            order_purchase_timestamp is not null
        group by 
            order_day  
        order by 
        order_day
    """

    revenue_df = pd.read_sql(query, con=engine)
    revenue_df.to_csv("revenue_dataset.csv", index=False)
    print("The dataset was successfully loaded!!!")

except Exception as e:
    print(f"Detail error: {e}")
finally:
    if engine:
        engine.dispose()
        
