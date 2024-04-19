from dataclasses import dataclass
from os import makedirs
from shutil import rmtree

from public_layers.utils.models import Config, BuildOptions
from public_layers.utils.variables import ARCHITECTURES

DIR_DIST = "dist"
SHEBANG = "#!/usr/bin/env bash\n\n"


def main():
    create_dist()
    config = Config()
    options = config.convert()
    commands_amd64 = [convert(x) for x in options if x.arch == ARCHITECTURES[0]]
    commands_arm64 = [convert(x) for x in options if x.arch == ARCHITECTURES[1]]

    with open(f"{DIR_DIST}/amd64.sh", "w") as f:
        f.write(SHEBANG + "\n".join(commands_amd64))

    with open(f"{DIR_DIST}/arm64.sh", "w") as f:
        f.write(SHEBANG + "\n".join(commands_arm64))


def create_dist():
    makedirs(DIR_DIST, exist_ok=True)
    rmtree(DIR_DIST)
    makedirs(DIR_DIST)


def convert(option: BuildOptions) -> str:
    return " ".join(
        [
            "./build.sh",
            f"--name {option.name}",
            f"--arch {option.arch}",
            f"--runtime-version {option.runtime_version}",
            f"--module {option.module}",
        ]
    )
