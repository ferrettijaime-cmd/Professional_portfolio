from datetime import datetime

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="olist_etl_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["etl", "postgres", "olist"],
) as dag:

    extract_raw = BashOperator(
        task_id="extract_raw",
        bash_command="python /opt/airflow/Script_Python/extract_data_to_postgres_docker.py",
    )

    raw_to_staging = BashOperator(
        task_id="raw_to_staging",
        bash_command="python /opt/airflow/Script_Python/raw_to_staging.py",
    )

    staging_to_analytics = BashOperator(
        task_id="staging_to_analytics",
        bash_command="python /opt/airflow/Script_Python/staging_to_analytics.py",
    )

    extract_raw >> raw_to_staging >> staging_to_analytics