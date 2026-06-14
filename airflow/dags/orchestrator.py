import sys
from datetime import timedelta, datetime
from airflow import DAG
# pyrefly: ignore [missing-import]
from airflow.operators.python import PythonOperator
# pyrefly: ignore [missing-import]
from airflow.providers.docker.operators.docker import DockerOperator
from docker.types import Mount

sys.path.append("/opt/airflow")

from fetcher.insert_records import main

default_args={
    'description': 'Weather API Orchestrator DAG',
    'start_date': datetime(2026, 6, 12),
    'catchup': False
}

dag = DAG(
    dag_id='weather-api-dbt-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=1)
)

with dag:
    fetch_and_insert=PythonOperator(
        task_id='fetch_and_insert',
        python_callable=main
    )
    transform_data=DockerOperator(
        task_id='transform_weather_data',
        image='ghcr.io/dbt-labs/dbt-postgres:1.9.latest',
        command='run',
        working_dir="/usr/app",
        mounts=[
            Mount(source="/home/mahmoud-elassy/projects/weather-stream/dbt/my_project", target="/usr/app", type="bind"),
            Mount(source="/home/mahmoud-elassy/projects/weather-stream/dbt/profiles.yml", target="/root/.dbt/profiles.yml", type="bind"),
        ],
        auto_remove="success",
        network_mode='weather-stream_pg_af_dbt_net',
        docker_url='unix://var/run/docker.sock',
    )
    
    fetch_and_insert >> transform_data
