from __future__ import annotations

from aws_cdk import core, aws_iam as iam, aws_logs as logs, aws_ecs as ecs

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class EcsAirflowCluster(ecs.Cluster):
    """
    Creates ECS cluster to be used by Airflow
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-ecs-cluster"
        super().__init__(
            stack,
            id=self.object_name,
            cluster_name=self.object_name,
            container_insights=True,
            vpc=stack.vpc_airflow,
        )
