#!/bin/bash

set -x
script_path=$(readlink -f "${BASH_SOURCE[0]}")
docker build -t python:langchain -f "$script_path"/../../docker/Dockerfile.base .
