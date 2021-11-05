from __future__ import annotations

from aws_cdk import aws_ecr as ecr

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class EcrAirflowDockerRepository(ecr.Repository):
    """
    Creates a Redis backend to run celery
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-docker-repository"

        super().__init__(
            stack,
            id=self.object_name,
            repository_name=self.object_name,
            lifecycle_rules=[
                ecr.LifecycleRule(
                    description="Keep only the latest 10 images", max_image_count=10
                )
            ],
            removal_policy=stack.default_removal_policy,
        )
