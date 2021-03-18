from aws_cdk import core


class AirflowStack(core.Stack):
    def __init__(
        self,
        scope: core.Construct,
        **kwargs,
    ) -> None:
        super().__init__(scope, id=f"{self.deploy_env.value}-airflow-stack", **kwargs)
