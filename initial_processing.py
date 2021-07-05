from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['chowjt@uci.edu'],
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'download_crec',
    default_args=default_args,
    description='Pull down and process congressional record for the day',
    schedule_interval='0 8 * * *',
    start_date=datetime.today() - timedelta(days = 2),
    tags=['crec'],
) as dag:

    transfer_to_s3_task = DockerOperator(
        dag=dag,
        task_id='transfer_to_s3_task',
        image='jtchow/transfer_to_s3:latest',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        force_pull=True
    )

    transfer_to_s3_task