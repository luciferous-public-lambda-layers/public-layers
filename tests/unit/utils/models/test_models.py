import public_layers.utils.models.models as index
import pytest


class TestModuleConvert:
    @pytest.mark.parametrize(
        "module, expected",
        [
            (
                index.Module(
                    name="tmp",
                    version="0.1.1",
                    is_individual_runtimes=False,
                    is_individual_architectures=False,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    )
                ],
            ),
            (
                index.Module(
                    name="tmp",
                    layer_name="TmpModule",
                    version="0.1.1",
                    is_individual_architectures=False,
                    is_individual_runtimes=False,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-TmpModule",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    )
                ],
            ),
            (
                index.Module(
                    name="tmp",
                    version="0.1.1",
                    extras=["aaa"],
                    is_individual_runtimes=False,
                    is_individual_architectures=False,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp[aaa]==0.1.1",
                    ),
                ],
            ),
            (
                index.Module(
                    name="tmp",
                    version="0.1.1",
                    extras=["aaa", "ccc", "bbb"],
                    is_individual_runtimes=False,
                    is_individual_architectures=False,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp[aaa,ccc,bbb]==0.1.1",
                    ),
                ],
            ),
            (
                index.Module(
                    name="tmp",
                    version="0.1.1",
                    is_individual_runtimes=True,
                    is_individual_architectures=False,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.12",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.11",
                        arch="amd64",
                        runtime_version="3.11",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.10",
                        arch="amd64",
                        runtime_version="3.10",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.9",
                        arch="amd64",
                        runtime_version="3.9",
                        module="tmp==0.1.1",
                    ),
                ],
            ),
            (
                index.Module(
                    name="tmp",
                    version="0.1.1",
                    is_individual_runtimes=False,
                    is_individual_architectures=True,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-X86_64",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Arm64",
                        arch="arm64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    ),
                ],
            ),
            (
                index.Module(
                    name="tmp",
                    version="0.1.1",
                    is_individual_runtimes=True,
                    is_individual_architectures=True,
                ),
                [
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.12-X86_64",
                        arch="amd64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.11-X86_64",
                        arch="amd64",
                        runtime_version="3.11",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.10-X86_64",
                        arch="amd64",
                        runtime_version="3.10",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.9-X86_64",
                        arch="amd64",
                        runtime_version="3.9",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.12-Arm64",
                        arch="arm64",
                        runtime_version="3.12",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.11-Arm64",
                        arch="arm64",
                        runtime_version="3.11",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.10-Arm64",
                        arch="arm64",
                        runtime_version="3.10",
                        module="tmp==0.1.1",
                    ),
                    index.BuildOptions(
                        name="LuciferousPublicLayers-tmp-Python3.9-Arm64",
                        arch="arm64",
                        runtime_version="3.9",
                        module="tmp==0.1.1",
                    ),
                ],
            ),
        ],
    )
    def test_normal(self, module, expected):
        actual = module.convert()
        assert set(actual) == set(expected)