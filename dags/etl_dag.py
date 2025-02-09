import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from etls.extract import extract_data
from etls.load import *
from etls.transform import process_log, process_time, process_song


default_args = {
    'owner': 'Le Huynh Thanh Duong',
    'start_date': datetime(2024, 4, 2)
}

file_postfix = datetime.now().strftime("%Y%m%d") #lấy ngày tháng năm hiện tại

##tạo một đối tưởng DAG
dag = DAG(
    dag_id='etl_MusicStreamPipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    tags=['Music stream', 'etl', 'pipeline']
)

# extraction log_data
path_log = "./data/input/log_data"
path_log_csv = "./data/processed/log_data.csv"
extract_log_data = PythonOperator(
    task_id='MusicStream_extraction_log_data',
    python_callable=extract_data,
    op_args= [path_log, path_log_csv],
    dag=dag
)

#extraction song_data
path_song = "./data/input/song_data"
path_song_csv = "./data/processed/song_data.csv"
extract_song_data = PythonOperator(
    task_id='MusicStream_extraction_song_data',
    python_callable=extract_data,
    op_args= [path_song, path_song_csv],
    dag=dag
)

#transform from csv
path_log = "./data/processed/log_data.csv"
path_song = "./data/processed/song_data.csv"
transform_log = PythonOperator(
    task_id = 'MusicStream_transformation_log',
    python_callable= process_log,
    op_args= [path_log],
    dag = dag
)
transform_song = PythonOperator(
    task_id = 'MusicStream_transformation_song',
    python_callable= process_song,
    op_args= [path_song],
    dag = dag
)
transform_time = PythonOperator(
    task_id = 'MusicStream_transformation_time',
    python_callable= process_time,
    dag = dag
)
load_time = PythonOperator(
    task_id = 'MusicStream_load_time',
    python_callable= load_dim_Time,
    op_args = ["./data/processed/stg_time.csv"],
    dag = dag
)

load_users = PythonOperator(
    task_id = 'MusicStream_load_user',
    python_callable= load_dim_Users,
    op_args = ["./data/processed/stg_user.csv"],
    dag = dag
)

load_artists = PythonOperator(
    task_id = 'MusicStream_load_artist',
    python_callable= load_dim_artists,
    op_args = ["./data/processed/stg_artist.csv"],
    dag = dag
)

load_songs = PythonOperator(
    task_id = 'MusicStream_load_song',
    python_callable= load_dim_songs,
    op_args = ["./data/processed/stg_song.csv"],
    dag = dag
)
load_songplays = PythonOperator(
    task_id = 'MusicStream_load_songplays',
    python_callable= load_fact_songplays,
    op_args = ["./data/processed/stg_log.csv"],
    dag = dag
)

##Đây là một luồng trong dag
extract_log_data >> transform_log >> load_users
extract_song_data >> transform_song >> load_artists >> load_songs 
transform_time >> load_time

[load_users, load_artists, load_songs, load_time]  >> load_songplays
 