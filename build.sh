#!/usr/bin/env bash

set -xeuo pipefail

usage() {
  cat <<'EOT'
build.sh --name LAYER_DIR_NAME --arch [amd64|arm64] --runtime-version RUNTIME_VERSION --module MODULE_NAME_VERSION

  --name LAYER_DIR_NAME directory having codes
  --arch [amd64|arm64] architecture
  --runtime-version RUNTIME_VERSION python runtime version (default: 3.12) (ex: 3.12, 3.9)
  --module MODULE_NAME_VERSION use module (ex: zstd==1.5.5.1)
EOT
}

layer_name=""
architecture=""
module=""
runtime_version="3.12"

for args in "$@"; do
  case $args in
    '--name')
      layer_name=$2
      ;;
    '--arch')
      architecture=$2
      ;;
    '--runtime-version')
      runtime_version=$2
      ;;
    '--module')
      module=$2
      ;;
    '--help')
      usage
      exit 0
      ;;
  esac
  shift
done

if [[ -z "${layer_name}" || -z "${architecture}" || -z "${runtime_version}" || -z "${module}" ]]; then
  usage
  exit 1
fi

if [[ "${architecture}" != "amd64" && "${architecture}" != "arm64" ]]; then
  echo "invalid architecture: ${architecture}"
  usage
  exit 1
fi

mkdir -p "layers/${layer_name}"

docker container run \
  --name "${layer_name}" \
  --platform "linux/${architecture}" \
  "public.ecr.aws/sam/build-python${runtime_version}:latest" \
  pip install "${module}" -t /tmp/python

docker container cp "${layer_name}:/tmp/python" "layers/${layer_name}/"
docker container rm "${layer_name}"
