from __future__ import annotations

from aws_cdk import core, aws_elasticache as elasticache, aws_ec2 as ec2

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class ElasticacheAirflowCeleryBackendCluster(elasticache.CfnCacheCluster):
    """
    Creates a Redis backend to run celery
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-celery-cluster"

        self.security_group = Ec2AirflowCeleryBackendSecurityGroup(stack)
        self.subnet_group = ElasticacheAirflowCeleryBackendSubnetGroup(stack)

        super().__init__(
            stack,
            id=self.object_name,
            auto_minor_version_upgrade=True,
            az_mode="single-az",
            cache_node_type="cache.t3.micro",
            cluster_name=self.object_name,
            engine="redis",
            engine_version="4.0.10",
            num_cache_nodes=1,
            port=6379,
            vpc_security_group_ids=[self.security_group.security_group_id],
            cache_subnet_group_name=self.subnet_group.cache_subnet_group_name,
        )

        self.node.add_dependency(self.subnet_group)
        self.node.add_dependency(self.security_group)


class Ec2AirflowCeleryBackendSecurityGroup(ec2.SecurityGroup):
    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-celery-backend-security-group"
        super().__init__(
            stack,
            id=self.object_name,
            vpc=stack.vpc_airflow,
            allow_all_outbound=True,
            security_group_name=self.object_name,
        )

        for subnet in stack.vpc_airflow.private_subnets:
            self.add_ingress_rule(
                peer=ec2.Peer.ipv4(subnet.ipv4_cidr_block), connection=ec2.Port.tcp(6379)
            )


class ElasticacheAirflowCeleryBackendSubnetGroup(elasticache.CfnSubnetGroup):
    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-celery-backend-subnet-group"
        super().__init__(
            stack,
            id=self.object_name,
            cache_subnet_group_name=self.object_name,
            description="Place airflow celery backend on private subnet",
            subnet_ids=[subnet.subnet_id for subnet in stack.vpc_airflow.private_subnets],
        )
