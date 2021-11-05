from __future__ import annotations

import aws_cdk.core as core
from aws_cdk import aws_ec2 as ec2

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class VpcAirflow(ec2.Vpc):
    """
    Creates VPC
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-vpc"
        super().__init__(stack, id=self.object_name)
