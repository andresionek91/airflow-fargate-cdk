from unittest.mock import patch

import boto3
from stack import AirflowStack


class TestFernetKeySecureParameter:
    def setup_ssm(self):
        client = boto3.client("ssm")
        client.put_parameter(
            Name="test-airflow-fernet-key-parameter",
            Value="fetched_fernet_key",
            Type="SecureString",
            Overwrite=True,
            Tier="Standard",
        )

    def teardown_ssm(self):
        client = boto3.client("ssm")
        client.delete_parameter(Name="test-airflow-fernet-key-parameter")

    def test_fernet_key_is_fetched_from_ssm(self, app_fixture):
        self.setup_ssm()
        airflow_stack = AirflowStack(app_fixture, deploy_env="test")
        self.teardown_ssm()
        assert (
            airflow_stack.fernet_key_secure_parameter.fernet_key_secret
            == "fetched_fernet_key"
        )

    @patch(
        "cryptography.fernet.Fernet.generate_key",
        return_value=b"kMK8snNv4UdM0Kxo6KE1DthX_zOq7UxN1wNKqbAGdCU=",
    )
    def test_fernet_key_is_created(self, mock_fernet, app_fixture):
        airflow_stack = AirflowStack(app_fixture, deploy_env="test")
        assert (
            airflow_stack.fernet_key_secure_parameter.fernet_key_secret
            == "kMK8snNv4UdM0Kxo6KE1DthX_zOq7UxN1wNKqbAGdCU="
        )
