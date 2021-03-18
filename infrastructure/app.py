from aws_cdk import core

from cdk.stack import AirflowStack

app = core.App()
AirflowStack(app)
app.synth()
