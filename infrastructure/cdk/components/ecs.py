from aws_cdk import core, aws_iam as iam, aws_logs as logs


class ECSTaskRole(iam.Role):
    """
    Creates role to be assumed by ECS tasks
    """

    def __init__(self, scope: core.Construct, deploy_env: str, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.name_convention_prefix = f"iam-{self.deploy_env}-ecs-task"
        super().__init__(
            scope,
            id=f"{self.name_convention_prefix}-role",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
            description="Role to allow ECS tasks to access ECR",
        )

        policy = iam.Policy(
            scope,
            id=f"{self.name_convention_prefix}-policy",
            policy_name=f"{self.name_convention_prefix}-policy",
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
        self.attach_inline_policy(policy)


class ECSLogGroup(logs.LogGroup):
    """
    Creates log group to be used by ECS tasks
    """

    def __init__(self, scope: core.Construct, deploy_env: str, **kwargs) -> None:
        self.deploy_env = deploy_env
        self.name_convention_prefix = f"logs-{self.deploy_env}-ecs"
        super().__init__(
            scope,
            id=f"{self.name_convention_prefix}-log-group",
            log_group_name=f"{self.name_convention_prefix}-log-group",
            removal_policy=kwargs["default_removal_policy"],
            retention=logs.RetentionDays.THREE_MONTHS,
        )
