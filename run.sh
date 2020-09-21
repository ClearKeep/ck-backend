#!/bin/bash

export PYTHONPATH=./

ARG=$1
if [ ${#ARG} -gt 0 ]; then
    if [ $ARG == '-p' ] || [ $ARG == '-proto' ]; then
        docker run --rm -v $(pwd):$(pwd) -w $(pwd) znly/protoc --plugin=protoc-gen-grpc=/usr/bin/grpc_python_plugin --python_out=. --grpc_out=. --proto_path=. ./proto/*.proto
        echo "gen protobuf file success"
    else
        pipenv run python app.py
    fi
else
    pipenv run python app.py
fi