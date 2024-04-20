import json
from dataclasses import dataclass, field
from re import Pattern, compile
from tomllib import load
from typing import Optional

from jsonschema import validate

from public_layers.utils.variables import MAPPING_ARCHITECTURES, RUNTIMES

pattern_non_alpha_numeric: Pattern = compile(r"[^0-9a-zA-Z]")


@dataclass(frozen=True)
class BuildOptions:
    name: str
    arch: str
    runtime_version: str
    module: str
    logical_id: str


@dataclass(frozen=True)
class Module:
    name: str
    layer_name: str
    version: str
    is_individual_runtimes: bool
    is_individual_architectures: bool
    extras: list[str] = field(default_factory=list)

    def convert(self) -> list[BuildOptions]:
        prefix = "LuciferousPublicLayers"
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
                    name=f"{prefix}-{self.layer_name}",
                    arch=all_architectures[0],
                    runtime_version=RUNTIMES[0],
                    module=install_target,
                    logical_id=pattern_non_alpha_numeric.sub(
                        "", f"{prefix}-{self.layer_name}"
                    ),
                )
            )
        elif pattern == (True, False):
            result += [
                BuildOptions(
                    name=f"{prefix}-{self.layer_name}-Python{runtime}",
                    arch=all_architectures[0],
                    runtime_version=runtime,
                    module=install_target,
                    logical_id=pattern_non_alpha_numeric.sub(
                        "", f"{prefix}-{self.layer_name}-Python{runtime}"
                    ),
                )
                for runtime in RUNTIMES
            ]
        elif pattern == (False, True):
            result += [
                BuildOptions(
                    name=f"{prefix}-{self.layer_name}-{v}",
                    arch=k,
                    runtime_version=RUNTIMES[0],
                    module=install_target,
                    logical_id=pattern_non_alpha_numeric.sub(
                        "", f"{prefix}-{self.layer_name}-{v}"
                    ),
                )
                for k, v in MAPPING_ARCHITECTURES.items()
            ]
        else:  # pattern == (True, True)
            result += [
                BuildOptions(
                    name=f"{prefix}-{self.layer_name}-Python{runtime}-{v}",
                    arch=k,
                    runtime_version=runtime,
                    module=install_target,
                    logical_id=pattern_non_alpha_numeric.sub(
                        "", f"{prefix}-{self.layer_name}-Python{runtime}-{v}"
                    ),
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
