import aws_cdk.core as core
from aws_cdk import aws_ec2 as ec2


class AirflowVPC(ec2.Vpc):
    """
    Creates role to be assumed by ECS tasks
    """

    def __init__(self, scope: core.Construct, **kwargs) -> None:
        self.deploy_env = scope.deploy_env
        self.object_name = f"ec2-{self.deploy_env}-airflow-vpc"
        super().__init__(
            scope,
            id=self.object_name,
            vpn_gateway=False,
            nat_gateways=0,
        )
