import aws_cdk.core as core
from stack import AirflowStack
import pytest
import boto3
import localstack_client.session


@pytest.fixture(scope="function")
def app_fixture():
    return core.App()


@pytest.fixture(scope="function")
def airflow_stack_fixture(app_fixture):
    return AirflowStack(app_fixture, deploy_env="test")


@pytest.fixture(scope="function")
def template_fixture():
    app = core.App()
    AirflowStack(app, deploy_env="test")
    return app.synth().get_stack("test-airflow-stack").template


@pytest.fixture(autouse=True)
def boto3_localstack_patch(monkeypatch):
    local_session = localstack_client.session.Session()
    monkeypatch.setattr(boto3, "client", local_session.client)
    monkeypatch.setattr(boto3, "resource", local_session.resource)
