from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

base_path = Path(__file__).resolve().parent.parent

data_path = base_path / "Data"

customer_df = pd.read_csv(data_path/"olist_customers_dataset.csv")
order_items_df = pd.read_csv(data_path/"olist_order_items_dataset.csv")
order_payments_df = pd.read_csv(data_path/"olist_order_payments_dataset.csv")
order_reviews_df = pd.read_csv(data_path/"olist_order_reviews_dataset.csv")
orders_df = pd.read_csv(data_path/"olist_orders_dataset.csv")
products_df = pd.read_csv(data_path/"olist_products_dataset.csv")
geolocation_df = pd.read_csv(data_path/"olist_geolocation_dataset.csv")
sellers_df = pd.read_csv(data_path/"olist_sellers_dataset.csv")
product_category_name_translation_df = pd.read_csv(data_path/"product_category_name_translation.csv")

base_path = Path(__file__).resolve().parent.parent

if Path("/opt/airflow").exists():
    env_file = base_path / ".env.airflow"
else:
    env_file = base_path / ".env"

load_dotenv(env_file)
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

engine = None

try:
    engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}")

    customer_df.to_sql(name="olist_customers_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    order_items_df.to_sql(name="olist_orders_items_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    order_payments_df.to_sql(name="olist_orders_payments_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    order_reviews_df.to_sql(name="olist_orders_reviews_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    orders_df.to_sql(name="olist_orders_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    products_df.to_sql(name="olist_products_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    geolocation_df.to_sql(name="olist_geolocation_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    sellers_df.to_sql(name="olist_sellers_dataset",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)

    product_category_name_translation_df.to_sql(name="product_category_name_translation",
                   con=engine,
                   schema="raw",
                   if_exists="replace",
                   index=False)
    
    print("The data was successfully extracted!!!")
    
except Exception as e:
    print(f'Detail: {e}')
    
finally:
    if engine:
        engine.dispose()
    
    

