# lakehouse_pipeline_dag.py
# DAG de orquestração do pipeline Bronze -> Silver -> Gold

from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="lakehouse_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:

    bronze = BashOperator(
        task_id="bronze_ingestion",
        bash_command="python notebooks/01_bronze_ingestion.py",
    )

    silver = BashOperator(
        task_id="silver_transformation",
        bash_command="python notebooks/02_silver_transformation.py",
    )

    gold = BashOperator(
        task_id="gold_aggregation",
        bash_command="python notebooks/03_gold_aggregation.py",
    )

    bronze >> silver >> gold
