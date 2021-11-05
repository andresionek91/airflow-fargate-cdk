from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook
import requests
from backoff import on_exception, constant
from ratelimit import limits, RateLimitException
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

config = {
    "bucket": "s3-belisquito-turma-5-production-data-lake-raw",
    "coins": ["BCH", "BTC", "ETH", "LTC"],
}

default_args = {
    "owner": "andresionek91",
    "start_date": datetime(2021, 1, 1),
    "depends_on_past": False,
    "provide_context": True,
}

dag = DAG(
    "mercado_bitcoin_dag",
    description="Extrai dados do sumario diario do mercado bitcoin.",
    schedule_interval="0 0 * * *",
    catchup=True,
    default_args=default_args,
)


@on_exception(constant, RateLimitException, interval=60, max_tries=3)
@limits(calls=20, period=60)
@on_exception(constant, requests.exceptions.HTTPError, max_tries=3, interval=10)
def get_daily_summary(date, coin):
    year, month, day = date.split("-")
    endpoint = (
        f"https://www.mercadobitcoin.net/api/{coin}/day-summary/{year}/{month}/{day}"
    )

    logger.info(f"Getting data from API with: {endpoint}")

    response = requests.get(endpoint)
    response.raise_for_status()
    logger.info(f"Data downloaded from API: {response.text}")

    return response.json()


def upload_to_s3(date, coin, **context):
    logger.info(f"Getting context from previous task")
    json_data = context["ti"].xcom_pull(task_ids=f"get_daily_summary_{coin}")
    string_data = json.dumps(json_data)
    now_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
    logger.info(f"Uploading to S3")
    S3Hook(aws_conn_id="aws_default").load_string(
        string_data=string_data,
        key=f"mercado_bitcoin/{coin}/execution_date={date}/mercado_bitcoin{coin}_{now_string}.json",
        bucket_name=config["bucket"],
    )


for coin in config["coins"]:
    logger.info(f"Starting extractions tasks for {coin}")

    task_1 = PythonOperator(
        task_id=f"get_daily_summary_{coin}",
        dag=dag,
        python_callable=get_daily_summary,
        op_kwargs={"date": "{{ ds }}", "coin": coin},
    )

    task_2 = PythonOperator(
        task_id=f"upload_to_s3_{coin}",
        dag=dag,
        python_callable=upload_to_s3,
        op_kwargs={"date": "{{ ds }}", "coin": coin},
        provide_context=True,
    )

    task_1 >> task_2
