from typing import List
from aws_cdk import core
from components.ecs import ECSTaskRole, ECSLogGroup, ECSTaskPolicy
from components.ec2 import AirflowVPC
from components.ssm import FernetKeySecureParameter


class AirflowStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        deploy_env: str,
        default_tags: List[dict] = [],
        default_removal_policy: core.RemovalPolicy = core.RemovalPolicy.DESTROY,
        import_vpc: bool = False,
        **kwargs,
    ) -> None:
        self.deploy_env = deploy_env
        self.default_removal_policy = default_removal_policy
        self.default_tags = default_tags
        self.import_vpc = import_vpc
        self._apply_default_tags(scope)
        super().__init__(scope, id=f"{self.deploy_env}-airflow-stack", **kwargs)

        self.ecs_task_role = ECSTaskRole(self)
        self.ecs_task_policy = ECSTaskPolicy(self)
        self.ecs_task_policy.attach_to_role(self.ecs_task_role)
        self.ecs_log_group = ECSLogGroup(self)

        if self.import_vpc:
            raise NotImplementedError()
        else:
            self.airflow_vpc = AirflowVPC(self)

        self.fernet_key_secure_parameter = FernetKeySecureParameter(self)

    def _apply_default_tags(self, scope: core.Construct):
        for key, value in self.default_tags:
            core.Tags.of(scope).add(key=key, value=value)
