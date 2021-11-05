from __future__ import annotations

import aws_cdk.core as core
from aws_cdk import aws_secretsmanager as secrets_manager
import boto3
from cryptography.fernet import Fernet
import os
import json

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class SecretManagerFernetKeySecret(secrets_manager.Secret):
    """
    Creates Fernet key to be used to encrypt data in RDS
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-fernet-key-secret"
        super().__init__(
            stack,
            id=self.object_name,
            secret_name=self.object_name,
            description="Airflow Fernet Key used to encrypt secrets in Airflow Metadata DB",
            generate_secret_string=secrets_manager.SecretStringGenerator(
                password_length=32
            ),
        )


class SecretManagerAirflowPasswordSecret(secrets_manager.Secret):
    """
    Creates Fernet key to be used to encrypt data in RDS
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-master-user-secret"
        super().__init__(
            stack,
            id=self.object_name,
            secret_name=self.object_name,
            description="Airflow Password to access UI",
            generate_secret_string=secrets_manager.SecretStringGenerator(
                secret_string_template=json.dumps(dict(username="master_user")),
                generate_string_key="password",
                password_length=32,
            ),
        )
