import aws_cdk.core as core
from aws_cdk import aws_ssm as ssm
import boto3
from cryptography.fernet import Fernet
import os


class FernetKeySecureParameter(ssm.StringParameter):
    """
    Creates role to be assumed by ECS tasks
    """

    def __init__(self, scope: core.Construct, deploy_env: str, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.object_name = f"iam-{self.deploy_env}-fernet-key-secret"
        self.fernet_key_secret = self._create_fernet_key()
        super().__init__(
            scope,
            id=self.object_name,
            parameter_name=self.object_name,
            string_value=self.fernet_key_secret,
            type=ssm.ParameterType.SECURE_STRING,
            description="Airflow Fernet Key secure parameter used to encrypt secrets in Airflow Metadata DB",
            tier=ssm.ParameterTier.STANDARD,
        )

    def _create_fernet_key(self):
        """
        Try to find fernet key in AWS Secrets Manager.
        If resource does not exist, create a new key.
        Set key as environment variable to be used by CF template.
        """

        client = boto3.client("ssm", endpoint_url=os.environ.get("AWS_ENDPOINT"))

        try:
            response = client.get_parameter(Name=self.object_name, WithDecryption=True)
            return response["Parameter"]["Value"]
        except client.exceptions.ParameterNotFound:
            return Fernet.generate_key().decode()