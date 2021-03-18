from aws_cdk import core
from configs import deploy_env, default_removal_policy
from components.ecs import ECSTaskRole, ECSLogGroup


class AirflowStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        **kwargs,
    ) -> None:
        self.deploy_env = deploy_env
        self.default_removal_policy = default_removal_policy
        super().__init__(scope, id=f"{self.deploy_env}-airflow-stack", **kwargs)

        ECSTaskRole(self, deploy_env=self.deploy_env)
        ECSLogGroup(
            self,
            deploy_env=self.deploy_env,
            default_removal_policy=default_removal_policy,
        )
