#!/bin/bash

set -x

script_path=$(readlink -f "${BASH_SOURCE[0]}")

check_docker_image() {
    local image="$1"
    if docker image inspect "$image" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

check_docker_image "python:langchain"
if check_docker_image "python:langchain"; then
    echo "python:langchain image already exists."
else
    echo "python:langchain image does not exist."
    "$script_path"/../build_base_image.sh
fi


docker build -t ai-agent:latest -f "$script_path"/../../docker/Dockerfile .
docker build -t ai-agent-ui:latest -f "$script_path"/../../docker/Dockerfile.ui .
