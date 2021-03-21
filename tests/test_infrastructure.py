import json
import pytest
from aws_cdk import core
from stack import AirflowStack


@pytest.fixture()
def fixture_template():
    app = core.App()
    AirflowStack(app, deploy_env="test")
    return app.synth().get_stack("test-airflow-stack").template


@pytest.fixture()
def policies_resources_fixture(fixture_template):
    for resource_name, resource in fixture_template["Resources"].items():
        if resource["Type"] in ["AWS::IAM::Policy", "AWS::IAM::ManagedPolicy"]:
            yield resource


@pytest.mark.parametrize(
    "resource_name, expected",
    [
        ("iam-test-ecs-task-role", True),
        ("iam-test-ecs-task-policy", True),
        ("logs-test-ecs-log-group", True),
        ("logs-test-non-existent-resource", False),
    ],
)
def test_resource_in_template(resource_name, expected, fixture_template):
    assert (resource_name in json.dumps(fixture_template)) == expected


def test_if_actions_in_policies_are_open(policies_resources_fixture):
    """
    Will
    """
    for statement in policies_resources_fixture["Properties"]["PolicyDocument"][
        "Statement"
    ]:
        if statement["Action"] == "*":
            raise AssertionError(
                f"The following policy contains a '*' "
                f"action, please revise and specify actions one by one. \n"
                f"{policies_resources_fixture}"
            )
