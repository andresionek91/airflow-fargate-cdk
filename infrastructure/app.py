from aws_cdk import core

from infrastructure.cdk.stack import AirflowStack

app = core.App()
AirflowStack(app)
app.synth()
