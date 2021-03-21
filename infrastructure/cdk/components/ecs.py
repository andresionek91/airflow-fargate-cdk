from aws_cdk import core, aws_iam as iam, aws_logs as logs


class ECSTaskRole(iam.Role):
    """
    Creates role to be assumed by ECS tasks
    """

    def __init__(self, scope: core.Construct, deploy_env: str, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.object_name = f"iam-{self.deploy_env}-ecs-task-role"
        super().__init__(
            scope,
            id=self.object_name,
            role_name=self.object_name,
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Role to allow ECS tasks to access ECR",
        )


class ECSTaskPolicy(iam.ManagedPolicy):
    """
    Creates role to be assumed by ECS tasks
    """

    def __init__(self, scope: core.Construct, deploy_env: str, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.object_name = f"iam-{self.deploy_env}-ecs-task-policy"
        super().__init__(
            scope,
            id=self.object_name,
            managed_policy_name=self.object_name,
            statements=[
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=[
                        "ecr:GetAuthorizationToken",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:BatchGetImage",
                    ],
                    resources=["*"],
                ),
                iam.PolicyStatement(
                    effect=iam.Effect.ALLOW,
                    actions=["logs:CreateLogStream", "logs:PutLogEvents"],
                    resources=[
                        "*",
                    ],
                ),
            ],
        )


class ECSLogGroup(logs.LogGroup):
    """
    Creates log group to be used by ECS tasks
    """

    def __init__(self, scope: core.Construct, deploy_env: str, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.object_name = f"logs-{self.deploy_env}-ecs-log-group"
        super().__init__(
            scope,
            id=self.object_name,
            log_group_name=self.object_name,
            removal_policy=kwargs["default_removal_policy"],
            retention=logs.RetentionDays.THREE_MONTHS,
        )
