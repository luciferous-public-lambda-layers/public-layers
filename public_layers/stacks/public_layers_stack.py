from aws_cdk import Stack  # Duration,; aws_sqs as sqs,
from constructs import Construct

from public_layers.utils.models import Config

from .module_layer_stack import ModuleLayerStack


class PublicLayersStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        config = Config()
        for module in config.modules:
            ModuleLayerStack(self, module)
