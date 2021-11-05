from cdk.stack import AirflowStack
from aws_cdk import core

from config import deploy_env, default_tags, whitelisted_ips, default_removal_policy


class AirflowApp(core.App):
    def __init__(self):
        super().__init__()
        self.deploy_env = deploy_env
        self.whitelisted_ips = whitelisted_ips
        self.default_removal_policy = default_removal_policy
        self.default_tags = default_tags

    def apply_default_tags(self, stack):
        for tag in self.default_tags:
            core.Tags.of(stack).add(key=tag.get("key"), value=tag.get("value"))


airflow_app = AirflowApp()

airflow_stack = AirflowStack(airflow_app)
airflow_app.apply_default_tags(airflow_stack)

airflow_app.synth()
