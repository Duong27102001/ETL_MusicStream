FROM apache/airflow:2.9.0

COPY requirements.txt /opt/airflow/

USER root
RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

USER airflow