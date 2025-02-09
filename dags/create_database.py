import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from database.db_utils import create_database_musicStream

default_args = {
    'owner': 'Le Huynh Thanh Duong',
    'start_date': datetime(2024, 4, 2)
}

##tạo một đối tưởng DAG
dag = DAG(
    dag_id='create_database_mucsicStream',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['Music stream', 'etl', 'pipeline']
)


create_database = PythonOperator(
    task_id = 'MusicStream_transformation_song',
    python_callable= create_database_musicStream,
    dag = dag
)

##Đây là một luồng trong dag
create_database
 