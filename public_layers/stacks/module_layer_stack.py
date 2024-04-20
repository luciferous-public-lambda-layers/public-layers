from pathlib import Path

from aws_cdk import NestedStack, RemovalPolicy
from aws_cdk.aws_lambda import Architecture, Code, LayerVersion, Runtime
from constructs import Construct

from public_layers.utils.models import Module

mapping_runtimes = {
    "3.12": Runtime.PYTHON_3_12,
    "3.11": Runtime.PYTHON_3_11,
    "3.10": Runtime.PYTHON_3_10,
    "3.9": Runtime.PYTHON_3_9,
}

mapping_architectures = {"amd64": Architecture.X86_64, "arm64": Architecture.ARM_64}

all_runtimes = [
    Runtime.PYTHON_3_12,
    Runtime.PYTHON_3_11,
    Runtime.PYTHON_3_10,
    Runtime.PYTHON_3_9,
]

all_architectures = [Architecture.X86_64, Architecture.ARM_64]


class ModuleLayerStack(NestedStack):
    def __init__(self, scope: Construct, module: Module):
        super().__init__(scope, f"Layers{module.layer_name}")

        for build_option in module.convert():
            LayerVersion(
                scope=self,
                id=build_option.logical_id,
                code=Code.from_asset(
                    str(
                        Path(__file__).parent.parent.parent.joinpath(
                            "layers", build_option.name
                        )
                    )
                ),
                compatible_architectures=(
                    [mapping_architectures[build_option.arch]]
                    if module.is_individual_architectures
                    else all_architectures
                ),
                compatible_runtimes=(
                    [mapping_runtimes[build_option.runtime_version]]
                    if module.is_individual_runtimes
                    else all_runtimes
                ),
                description="",
                layer_version_name=build_option.name,
                removal_policy=RemovalPolicy.RETAIN,
            )
