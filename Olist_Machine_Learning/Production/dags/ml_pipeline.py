from datetime import datetime
from datetime import timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="ml_pipeline",
    start_date=datetime(2026,6,20),
    schedule=None,
    catchup=False,
    tags=["ml", "machine_learning", "olist_ml"],
) as dag:
    
    extract_data=BashOperator(
        task_id="extract_raw",
        bash_command="python /opt/airflow/scripts_task/revenue_forecasting_task.py",
        retries=2,
        retry_delay=timedelta(minutes=2),
    )

    build_features=BashOperator(
        task_id="features_engineering",
        bash_command="python /opt/airflow/scripts_task/features_engineering_task.py",
        retries=2,
        retry_delay=timedelta(minutes=2),
    )

    split_dataset=BashOperator(
        task_id="training_dataset",
        bash_command="python /opt/airflow/scripts_task/features_training_dataset_task.py",
        retries=2,
        retry_delay=timedelta(minutes=2),
    )

    evaluate_models=BashOperator(
        task_id="predictions_and_metrics",
        bash_command="python /opt/airflow/scripts_task/predictions_and_metrics_task.py",
        retries=2,
        retry_delay=timedelta(minutes=2),
    )

    extract_data >> build_features >> split_dataset >> evaluate_models


