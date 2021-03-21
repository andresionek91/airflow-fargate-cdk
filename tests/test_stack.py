from unittest.mock import patch

from aws_cdk.aws_ssm import StringParameter
from stack import AirflowStack
from aws_cdk.aws_ec2 import Vpc
from aws_cdk.aws_iam import Role, ManagedPolicy
from aws_cdk.aws_logs import LogGroup
import pytest


class TestAirflowStack:
    @pytest.mark.parametrize(
        "resource_name, resource_type",
        [
            ("ecs_task_role", Role),
            ("ecs_task_policy", ManagedPolicy),
            ("ecs_log_group", LogGroup),
            ("airflow_vpc", Vpc),
            ("fernet_key_secure_parameter", StringParameter),
        ],
    )
    def test_resource_is_instance(
        self, resource_name, resource_type, airflow_stack_fixture
    ):
        assert isinstance(getattr(airflow_stack_fixture, resource_name), resource_type)

    @patch.object(AirflowStack, "_apply_default_tags")
    def test_apply_default_tags_called(self, mock, app_fixture):
        AirflowStack(app_fixture, deploy_env="test")
        mock.assert_called_with(app_fixture)

    @pytest.mark.xfail(
        raises=NotImplementedError,
        strict=True,
        reason="Importing vpc needs to be implemented",
    )
    def test_import_vpc(self, app_fixture):
        AirflowStack(app_fixture, deploy_env="test", import_vpc=True)
