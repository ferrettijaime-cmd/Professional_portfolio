from pathlib import Path
import os
import psycopg2
from dotenv import load_dotenv

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

cursor = None
connection = None

try:
    base_path = Path(__file__).resolve().parent.parent
    sql_file = base_path / "Script_SQL" / "updating_analytics_schema.sql"

    with open(sql_file, "r", encoding="utf-8") as f:
        sql = f.read()

    connection = psycopg2.connect(user=user, password=password, host=host, port=port, database=database)
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
    print("Pipeline successfully constructed")

except FileNotFoundError:
    print(f"The file was not found in the path:{sql_file}")
   
except Exception as e:
    if connection:
        connection.rollback()
    print(f'Error details:{e}')

finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()