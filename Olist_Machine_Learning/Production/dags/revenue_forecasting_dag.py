from pathlib import Path
import os
from dotenv import load_dotenv
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
import pandas as pd

base_dir_neon = Path(__file__).resolve().parent.parent.parent
file_neondb = base_dir_neon / "neondb_credentials.env"

base_dir_local = Path(__file__).resolve().parent.parent.parent
file_ml_foresc = base_dir_local / "ml_forecasting_db.env"

load_dotenv(file_neondb)
neon_user = os.getenv("DB_USER")
neon_password = os.getenv("DB_PASSWORD")
neon_host = os.getenv("DB_HOST")
neon_port = os.getenv("DB_PORT")
neon_database = os.getenv("DB_NAME")

load_dotenv(file_ml_foresc, override=True)
local_user = os.getenv("POSTGRES_USER")
local_password = os.getenv("POSTGRES_PASSWORD")
local_host = os.getenv("POSTGRES_HOST")
local_port = os.getenv("POSTGRES_PORT")
local_database = os.getenv("POSTGRES_DB")

neon_url = URL.create(
    drivername="postgresql+psycopg2",
    username=neon_user,
    password=neon_password,
    host=neon_host,
    port=neon_port,
    database=neon_database
)

local_url = URL.create(
    drivername="postgresql+psycopg2",
    username=local_user,
    password=local_password,
    host=local_host,
    port=local_port,
    database=local_database
)

engine_neon = None
engine_local = None

try:
    engine_neon = create_engine(neon_url)
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
    revenue_df = pd.read_sql(query, con=engine_neon)
    print(f"Rows extracted: {len(revenue_df)}")

    engine_local = create_engine(local_url)

    revenue_df.to_sql(name="revenue_dataset",
                   con=engine_local,
                   schema="raw",
                   if_exists="replace",
                   index=False)
    print("The dataset was successfully loaded!!!")
    
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    if engine_neon:
        engine_neon.dispose()
    if engine_local:
        engine_local.dispose()