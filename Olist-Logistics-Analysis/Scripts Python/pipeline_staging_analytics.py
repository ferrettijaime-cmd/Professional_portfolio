import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

cursor = None
connection = None

try:
    folder = r"C:\Professional_project"
    file = "Fact_and_dim.sql"
    path = os.path.join(folder, file)

    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    print("Pipeline successfully constructed")

except FileNotFoundError:
    print(f"The file was not found in the path:{path}")
   
except Exception as e:
    if connection:
        connection.rollback()
    print(f'Error details:{e}')

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
  