import pandas as pd
from sqlalchemy import create_engine

customer_df = pd.read_csv(r"C:\Data_Base\Data\olist_customers_dataset.csv")
order_items_df = pd.read_csv(r"C:\Data_Base\Data\olist_order_items_dataset.csv")
order_payments_df = pd.read_csv(r"C:\Data_Base\Data\olist_order_payments_dataset.csv")
order_reviews_df = pd.read_csv(r"C:\Data_Base\Data\olist_order_reviews_dataset.csv")
orders_df = pd.read_csv(r"C:\Data_Base\Data\olist_orders_dataset.csv")
products_df = pd.read_csv(r"C:\Data_Base\Data\olist_products_dataset.csv")

engine = create_engine("postgresql+psycopg2://neondb_owner:npg_G6rXFW2Pieqg@ep-soft-butterfly-alwuk7e8.c-3.eu-central-1.aws.neon.tech:5432/neondb")

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
print("The data was sent successfully!!!")






