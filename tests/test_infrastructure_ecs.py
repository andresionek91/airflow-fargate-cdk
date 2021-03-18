import json
import pytest

from aws_cdk import core
from infrastructure.cdk.stack import AirflowStack


@pytest.fixture()
def fixture_template():
    app = core.App()
    AirflowStack(app)
    return json.dumps(app.synth().get_stack("test-airflow-stack").template)


@pytest.mark.parametrize(
    "resource_name",
    [
        ("iam-test-ecs-task-role"),
        ("iam-test-ecs-task-policy"),
        ("logs-test-ecs-log-group"),
    ],
)
def test_resource_in_template(resource_name, fixture_template):
    assert resource_name in fixture_template
