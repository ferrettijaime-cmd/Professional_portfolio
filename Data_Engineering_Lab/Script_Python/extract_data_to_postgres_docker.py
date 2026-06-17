import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

customer_df = pd.read_csv(r"C:\Data_Base\Data\olist_customers_dataset.csv")
order_items_df = pd.read_csv(r"C:\Data_Base\Data\olist_order_items_dataset.csv")
order_payments_df = pd.read_csv(r"C:\Data_Base\Data\olist_order_payments_dataset.csv")
order_reviews_df = pd.read_csv(r"C:\Data_Base\Data\olist_order_reviews_dataset.csv")
orders_df = pd.read_csv(r"C:\Data_Base\Data\olist_orders_dataset.csv")
products_df = pd.read_csv(r"C:\Data_Base\Data\olist_products_dataset.csv")
geolocation_df = pd.read_csv(r"C:\Data_Base\Data\olist_geolocation_dataset.csv")
sellers_df = pd.read_csv(r"C:\Data_Base\Data\olist_sellers_dataset.csv")
product_category_name_translation_df = pd.read_csv(r"C:\Data_Base\Data\product_category_name_translation.csv")

load_dotenv()
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")
host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
database = os.getenv("POSTGRES_DB")

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
    
except Exception as e:
    print(f'Detail: {e}')
    
finally:
    engine.dispose()

