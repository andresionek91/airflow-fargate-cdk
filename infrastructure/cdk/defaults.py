import os
from aws_cdk.core import RemovalPolicy

deploy_env = os.environ["DEPLOY_ENV"]
default_removal_policy = (
    RemovalPolicy.RETAIN if deploy_env == "production" else RemovalPolicy.DESTROY
)
