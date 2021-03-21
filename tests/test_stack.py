from unittest.mock import patch
from aws_cdk.core import App
from stack import AirflowStack
from aws_cdk.aws_ec2 import Vpc
from aws_cdk.aws_iam import Role, ManagedPolicy
import pytest


@pytest.fixture()
def app_fixture():
    return App()


class TestAirflowStack:
    def test_ecs_task_role_is_isntance(self, app_fixture):
        airflow_stack = AirflowStack(app_fixture, deploy_env="test")
        assert isinstance(airflow_stack.ecs_task_role, Role)

    def test_ecs_task_policy_is_isntance(self, app_fixture):
        airflow_stack = AirflowStack(app_fixture, deploy_env="test")
        assert isinstance(airflow_stack.ecs_task_policy, ManagedPolicy)

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

    def test_airflow_vpc_is_isntance(self, app_fixture):
        airflow_stack = AirflowStack(app_fixture, deploy_env="test")
        assert isinstance(airflow_stack.airflow_vpc, Vpc)
