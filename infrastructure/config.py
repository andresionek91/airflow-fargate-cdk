import os
from typing import List
from aws_cdk import core

deploy_env: str = os.environ.get("DEPLOY_ENV", default="test")

default_tags: List[dict] = [
    dict(key="deploy_env", value=deploy_env),
    dict(key="owner", value="Data Engineering"),
    dict(key="service", value="Airflow"),
]

# Please change this and select the specific IP you wish to whitelist before deploying. 0.0.0.0/0 is public accessible.
whitelisted_ips: List[str] = ["0.0.0.0/0"]

default_removal_policy = core.RemovalPolicy.DESTROY

airflow_environment = {
    "AIRFLOW_USERNAME": "user",
    "AIRFLOW_PASSWORD": "",
    "AIRFLOW_EMAIL": "test@email.com",
    "AIRFLOW_EXECUTOR": "CeleryExecutor",
    "AIRFLOW_FERNET_KEY": "",
    "AIRFLOW_LOAD_EXAMPLES": "no",
    "AIRFLOW_BASE_URL": "http://localhost:8080",
    "AIRFLOW_DATABASE_HOST": "",
    "AIRFLOW_DATABASE_PORT_NUMBER": "",
    "AIRFLOW_DATABASE_NAME": "",
    "AIRFLOW_DATABASE_USERNAME": "",
    "AIRFLOW_DATABASE_PASSWORD": "",
    "AIRFLOW_DATABASE_USE_SSL": "no",
    "REDIS_HOST": "",
    "REDIS_PORT_NUMBER": "",
}
