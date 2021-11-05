from __future__ import annotations

from aws_cdk import core, aws_rds as rds, aws_ec2 as ec2

# To avoid circular dependency when importing AirflowStack
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from stack import AirflowStack


class RdsAirflowMetadataDb(rds.DatabaseInstance):
    """
    Creates a Postgres database to be used for Airflow Metadata
    """

    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-metadata-rds-instance"

        super().__init__(
            stack,
            id=self.object_name,
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_4
            ),
            database_name="airflow",
            instance_type=ec2.InstanceType("t3.micro"),
            vpc=stack.vpc_airflow,
            instance_identifier=self.object_name,
            port=5432,
            vpc_placement=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
            subnet_group=RdsAirflowMetadataDbSubnetGroup(stack),
            parameter_group=RdsAirflowMetadataDbParameterGroup(stack),
            security_groups=[Ec2AirflowMetadataDbSecurityGroup(stack)],
            removal_policy=stack.default_removal_policy,
            **kwargs,
        )


class Ec2AirflowMetadataDbSecurityGroup(ec2.SecurityGroup):
    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-metadata-rds-security-group"
        super().__init__(
            stack,
            id=self.object_name,
            vpc=stack.vpc_airflow,
            allow_all_outbound=True,
            security_group_name=self.object_name,
        )

        # Whitelist Database Access to IPs
        for ip in stack.whitelisted_ips:
            self.add_ingress_rule(peer=ec2.Peer.ipv4(ip), connection=ec2.Port.tcp(5432))

        for subnet in stack.vpc_airflow.private_subnets:
            self.add_ingress_rule(
                peer=ec2.Peer.ipv4(subnet.ipv4_cidr_block), connection=ec2.Port.tcp(5432)
            )


class RdsAirflowMetadataDbSubnetGroup(rds.SubnetGroup):
    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-metadata-rds-subnet-group"
        super().__init__(
            stack,
            id=self.object_name,
            description="Place RDS on public subnet",
            vpc=stack.vpc_airflow,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC),
        )


class RdsAirflowMetadataDbParameterGroup(rds.ParameterGroup):
    def __init__(self, stack: AirflowStack, **kwargs) -> None:
        self.object_name = f"{stack.deploy_env}-airflow-metadata-rds-parameter-group"
        super().__init__(
            stack,
            id=self.object_name,
            description="Parameter group of Airflow Metadata DB.",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_4
            ),
            parameters={"max_connections": "100"},
        )
