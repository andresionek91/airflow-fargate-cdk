from typing import List
from cdk.stack import AirflowStack
from aws_cdk import core
import os

deploy_env: str = os.environ["DEPLOY_ENV"]
default_tags: List[dict] = [
    dict(key="deploy_env", value=deploy_env),
    dict(key="owner", value="Data Engineering"),
    dict(key="service", value="Airflow"),
]

app = core.App()
AirflowStack(app, deploy_env=deploy_env, default_tags=default_tags)
app.synth()
