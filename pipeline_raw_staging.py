import os
import psycopg2
from dotenv import load_dotenv

folder = r"C:\Professional_project"
file = "staging_script.sql"
path = os.path.join(folder, file)

with open(path, "r", encoding="utf-8") as f:
    sql = f.read()

load_dotenv()
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_NAME")

connection = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)

cursor = connection.cursor()
cursor.execute(sql)
connection.commit()

cursor.close()
connection.close()
print("Pipeline successfully constructed")


