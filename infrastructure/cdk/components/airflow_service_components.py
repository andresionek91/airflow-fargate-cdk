from __future__ import annotations

from aws_cdk import (
    core,
    aws_iam as iam,
    aws_logs as logs,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_patterns,
    aws_elasticloadbalancingv2 as elb,
    aws_route53 as route53,
    aws_certificatemanager as certificate_manager,
)

from infrastructure.config import airflow_environment
import base64

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class EcsAirflowTaskDefinition(ecs.FargateTaskDefinition):
    """
    Task Definition for Airflow Services
    """

    def __init__(
        self,
        stack: AirflowStack,
        service_name: str,
        service_port: int,
        cpu: int,
        memory: int,
        image: str,
        **kwargs,
    ) -> None:
        self.service_name = service_name
        self.service_port = service_port
        self.object_name = (
            f"{stack.deploy_env}-airflow-{self.service_name}-task-definition"
        )
        self.airflow_environment = airflow_environment
        self._update_environment(stack=stack)
        super().__init__(
            stack,
            id=self.object_name,
            cpu=cpu,
            memory_limit_mib=memory,
            family=self.object_name,
        )

        self.container = self.add_container(
            id=f"{stack.deploy_env}-airflow-{self.service_name}-container",
            image=ecs.ContainerImage.from_registry(image),
            environment=self.airflow_environment,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=f"{stack.deploy_env}-airflow-{self.service_name}"
            ),
            command=[self.service_name],
        )
        if self.service_port:
            self.container.add_port_mappings(
                ecs.PortMapping(container_port=self.service_port)
            )

    def _update_environment(self, stack: AirflowStack):
        self.airflow_environment.update(
            AIRFLOW_USERNAME=stack.master_user_secret.secret_value_from_json(
                "username"
            ).to_string()
        )
        self.airflow_environment.update(
            AIRFLOW_PASSWORD=stack.master_user_secret.secret_value_from_json(
                "password"
            ).to_string()
        )
        self.airflow_environment.update(
            AIRFLOW_FERNET_KEY=base64.urlsafe_b64encode(
                stack.fernet_key_secret.secret_value.to_string().encode()
            ).decode()
        )
        self.airflow_environment.update(
            AIRFLOW_DATABASE_HOST=stack.rds_metadata_db.db_instance_endpoint_address
        )
        self.airflow_environment.update(
            AIRFLOW_DATABASE_PORT_NUMBER=stack.rds_metadata_db.db_instance_endpoint_port
        )
        self.airflow_environment.update(
            AIRFLOW_DATABASE_NAME=stack.rds_metadata_db.secret.secret_value_from_json(
                "dbname"
            ).to_string()
        )
        self.airflow_environment.update(
            AIRFLOW_DATABASE_USERNAME=stack.rds_metadata_db.secret.secret_value_from_json(
                "username"
            ).to_string()
        )
        self.airflow_environment.update(
            AIRFLOW_DATABASE_PASSWORD=stack.rds_metadata_db.secret.secret_value_from_json(
                "password"
            ).to_string()
        )
        self.airflow_environment.update(
            REDIS_HOST=stack.celery_backend.attr_redis_endpoint_address
        )
        self.airflow_environment.update(
            REDIS_PORT_NUMBER=stack.celery_backend.attr_redis_endpoint_port
        )


class EcsAirflowLoadBalancedFargateService(
    ecs_patterns.ApplicationLoadBalancedFargateService
):
    """
    Task Definition for Airflow Services
    """

    def __init__(
        self,
        stack: AirflowStack,
        service_name: str,
        task_definition: ecs.FargateTaskDefinition,
        desired_count: int,
        cluster: ecs.Cluster,
        **kwargs,
    ) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-{service_name}-ecs-service"

        super().__init__(
            stack,
            id=self.object_name,
            service_name=self.object_name,
            task_definition=task_definition,
            desired_count=desired_count,
            cluster=cluster,
        )

        self.target_group.configure_health_check(healthy_http_codes="200-399")


class EcsAirflowAutoscalingFargateService(ecs.FargateService):
    """
    Task Definition for Airflow Services
    """

    def __init__(
        self,
        stack: AirflowStack,
        service_name: str,
        task_definition: ecs.FargateTaskDefinition,
        desired_count: int,
        cluster: ecs.Cluster,
        max_worker_count: int,
        target_memory_utilization: int,
        memory_scale_in_cooldown: int,
        memory_scale_out_cooldown: int,
        target_cpu_utilization: int,
        cpu_scale_in_cooldown: int,
        cpu_scale_out_cooldown: int,
        **kwargs,
    ) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-{service_name}-ecs-service"

        super().__init__(
            stack,
            id=self.object_name,
            service_name=self.object_name,
            task_definition=task_definition,
            desired_count=desired_count,
            cluster=cluster,
        )

        self.scalable_task_count = self.auto_scale_task_count(
            max_capacity=max_worker_count
        )

        self.scalable_task_count.scale_on_memory_utilization(
            f"{stack.deploy_env}-airflow-{service_name}-memory-utilization-scaler",
            policy_name=f"{stack.deploy_env}-airflow-{service_name}-memory-utilization-scaler",
            target_utilization_percent=target_memory_utilization,
            scale_in_cooldown=core.Duration.seconds(memory_scale_in_cooldown),
            scale_out_cooldown=core.Duration.seconds(memory_scale_out_cooldown),
        )

        self.scalable_task_count.scale_on_cpu_utilization(
            f"{stack.deploy_env}-airflow-{service_name}-cpu-utilization-scaler",
            policy_name=f"{stack.deploy_env}-airflow-{service_name}-cpu-utilization-scaler",
            target_utilization_percent=target_cpu_utilization,
            scale_in_cooldown=core.Duration.seconds(cpu_scale_in_cooldown),
            scale_out_cooldown=core.Duration.seconds(cpu_scale_out_cooldown),
        )


class EcsAirflowFargateService(ecs.FargateService):
    """
    Task Definition for Airflow Services
    """

    def __init__(
        self,
        stack: AirflowStack,
        service_name: str,
        task_definition: ecs.FargateTaskDefinition,
        desired_count: int,
        cluster: ecs.Cluster,
        **kwargs,
    ) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-{service_name}-ecs-service"

        super().__init__(
            stack,
            id=self.object_name,
            service_name=self.object_name,
            task_definition=task_definition,
            desired_count=desired_count,
            cluster=cluster,
        )
