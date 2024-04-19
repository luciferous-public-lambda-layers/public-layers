import json
from dataclasses import dataclass, field
from tomllib import load
from typing import Optional

from jsonschema import validate

from public_layers.utils.variables import MAPPING_ARCHITECTURES, RUNTIMES


@dataclass(frozen=True)
class BuildOptions:
    name: str
    arch: str
    runtime_version: str
    module: str


@dataclass(frozen=True)
class Module:
    name: str
    version: str
    is_individual_runtimes: bool
    is_individual_architectures: bool
    layer_name: Optional[str] = field(default=None)
    extras: list[str] = field(default_factory=list)

    def convert(self) -> list[BuildOptions]:
        prefix = "LuciferousPublicLayers"
        module_name_base = self.name if self.layer_name is None else self.layer_name

        all_architectures = list(MAPPING_ARCHITECTURES.keys())

        install_target = self.name
        if len(self.extras) > 0:
            install_target += "[" + ",".join(self.extras) + "]"
        install_target += f"=={self.version}"

        pattern = (self.is_individual_runtimes, self.is_individual_architectures)
        result = []

        if pattern == (False, False):
            result.append(
                BuildOptions(
                    name=f"{prefix}-{module_name_base}",
                    arch=all_architectures[0],
                    runtime_version=RUNTIMES[0],
                    module=install_target,
                )
            )
        elif pattern == (True, False):
            result += [
                BuildOptions(
                    name=f"{prefix}-{module_name_base}-Python{runtime}",
                    arch=all_architectures[0],
                    runtime_version=runtime,
                    module=install_target,
                )
                for runtime in RUNTIMES
            ]
        elif pattern == (False, True):
            result += [
                BuildOptions(
                    name=f"{prefix}-{module_name_base}-{v}",
                    arch=k,
                    runtime_version=RUNTIMES[0],
                    module=install_target,
                )
                for k, v in MAPPING_ARCHITECTURES.items()
            ]
        else:  # pattern == (True, True)
            result += [
                BuildOptions(
                    name=f"{prefix}-{module_name_base}-Python{runtime}-{v}",
                    arch=k,
                    runtime_version=runtime,
                    module=install_target,
                )
                for k, v in MAPPING_ARCHITECTURES.items()
                for runtime in RUNTIMES
            ]

        return result


@dataclass(init=False)
class Config:
    modules: list[Module]

    def __init__(self):
        with open("modules.toml", "rb") as f:
            data = load(f)

        with open("schema.json") as f:
            schema = json.load(f)

        validate(data, schema)
        self.modules = [Module(**x) for x in data["module"]]

    def convert(self) -> list[BuildOptions]:
        result = []

        for module in self.modules:
            result += module.convert()

        return result
