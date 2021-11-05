from __future__ import annotations

from typing import List
from aws_cdk import core, aws_ec2 as ec2
from components.ecs import EcsAirflowCluster
from components.ec2 import VpcAirflow
from components.secretsmanager import (
    SecretManagerFernetKeySecret,
    SecretManagerAirflowPasswordSecret,
)
from components.rds import RdsAirflowMetadataDb
from components.elasticache import ElasticacheAirflowCeleryBackendCluster
from components.ecr import EcrAirflowDockerRepository
from components.airflow_service_components import (
    EcsAirflowTaskDefinition,
    EcsAirflowFargateService,
    EcsAirflowLoadBalancedFargateService,
    EcsAirflowAutoscalingFargateService,
)


class AirflowStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        import_vpc: bool = False,
        **kwargs,
    ) -> None:
        self.import_vpc = import_vpc
        self.deploy_env = scope.deploy_env
        self.default_removal_policy = scope.default_removal_policy
        self.whitelisted_ips = scope.whitelisted_ips
        super().__init__(scope, id=f"{self.deploy_env}-airflow-stack", **kwargs)

        if self.import_vpc:
            raise NotImplementedError()
        else:
            self.vpc_airflow = VpcAirflow(self)

        self.fernet_key_secret = SecretManagerFernetKeySecret(self)
        self.master_user_secret = SecretManagerAirflowPasswordSecret(self)
        self.rds_metadata_db = RdsAirflowMetadataDb(self)
        self.celery_backend = ElasticacheAirflowCeleryBackendCluster(self)
        self.ecr_repository = EcrAirflowDockerRepository(self)
        self.ecs_cluster = EcsAirflowCluster(self)

        # Flower Definition
        self.flower_task_definition = EcsAirflowTaskDefinition(
            self,
            service_name="flower",
            service_port=5555,
            cpu=512,
            memory=1024,
            image="docker.io/bitnami/airflow:2-debian-10",
        )
        self.flower = EcsAirflowLoadBalancedFargateService(
            self,
            service_name="flower",
            task_definition=self.flower_task_definition,
            cluster=self.ecs_cluster,
            desired_count=1,
        )

        # Worker Definition
        self.worker_task_definition = EcsAirflowTaskDefinition(
            self,
            service_name="worker",
            service_port=8793,
            cpu=512,
            memory=1024,
            image="docker.io/bitnami/airflow-worker:2-debian-10",
        )
        self.worker = EcsAirflowAutoscalingFargateService(
            self,
            service_name="worker",
            task_definition=self.worker_task_definition,
            cluster=self.ecs_cluster,
            desired_count=2,
            max_worker_count=4,
            target_memory_utilization=80,
            memory_scale_in_cooldown=10,
            memory_scale_out_cooldown=20,
            target_cpu_utilization=80,
            cpu_scale_in_cooldown=10,
            cpu_scale_out_cooldown=20,
        )

        # Webserver Definition
        self.webserver_task_definition = EcsAirflowTaskDefinition(
            self,
            service_name="webserver",
            service_port=8080,
            cpu=1024,
            memory=2048,
            image="docker.io/bitnami/airflow:2-debian-10",
        )
        self.webserver = EcsAirflowLoadBalancedFargateService(
            self,
            service_name="webserver",
            task_definition=self.webserver_task_definition,
            cluster=self.ecs_cluster,
            desired_count=1,
        )

        # Scheduler Definition
        self.scheduler_task_definition = EcsAirflowTaskDefinition(
            self,
            service_name="scheduler",
            service_port=None,
            cpu=512,
            memory=1024,
            image="docker.io/bitnami/airflow-scheduler:2-debian-10",
        )
        self.scheduler = EcsAirflowFargateService(
            self,
            service_name="scheduler",
            task_definition=self.scheduler_task_definition,
            cluster=self.ecs_cluster,
            desired_count=1,
        )

        for service in (
            self.scheduler,
            self.webserver.service,
            self.worker,
            self.flower.service,
        ):
            service.connections.allow_to(
                self.rds_metadata_db,
                ec2.Port.tcp(5432),
                description="Allow connection to Metadata DB",
            )

            service.connections.allow_to(
                self.celery_backend.security_group,
                ec2.Port.tcp(6379),
                description="Allow connection to celery backend / message broker",
            )

        for ip in self.whitelisted_ips:
            for service in (self.webserver.service, self.flower.service):
                service.connections.allow_to(
                    ec2.Peer.ipv4(ip),
                    ec2.Port.tcp(80),
                    description="Allow HTTP connections",
                )

                service.connections.allow_to(
                    ec2.Peer.ipv4(ip),
                    ec2.Port.tcp(443),
                    description="Allow HTTPS connections",
                )
