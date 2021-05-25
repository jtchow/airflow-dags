from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}

with DAG(
    'tutorial',
    default_args=default_args,
    description='Pull down and process congressional record for the day',
    schedule_interval='0 23 * * *',
    start_date=datetime.today() - timedelta(days = 2),
    tags=['crec'],
) as dag:

    transfer_to_s3_task = DockerOperator(
        dag=dag,
        task_id='transfer_to_s3_task',
        image='jtchow/transfer_to_s3',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock'
    )

    transfer_to_s3_task