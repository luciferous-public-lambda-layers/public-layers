from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from constructs import Construct


class PublicLayersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
