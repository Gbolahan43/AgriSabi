import aws_cdk as cdk
from stacks.database_stack import DatabaseStack

app = cdk.App()

env = cdk.Environment(region="us-east-1") # Hardcoded for prototyping Nova Sonic

# Deploy the DynamoDB Session History Stack
DatabaseStack(app, "AgriSabiDatabaseStack", env=env)

# Bedrock and Lambda stacks would be initialized here...

app.synth()
