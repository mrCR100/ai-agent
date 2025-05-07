#!/bin/bash

set -x

docker run -d --network=host -p 5000:5000 ai-agent

