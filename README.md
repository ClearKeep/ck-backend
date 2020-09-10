
# ClearKeep

## Setup keycloak local

> docker run -d -p 8080:8080 -e KEYCLOAK_USER=admin -e
> KEYCLOAK_PASSWORD=admin quay.io/keycloak/keycloak:11.0.1

Admin management console
> localhost:8080

## install package management pipenv

https://pypi.org/project/pipenv/

## Run project
> pipenv install
> sh run.sh

## Generated protobuf file
From root project

> docker run --rm -v $(pwd):$(pwd) -w $(pwd) znly/protoc --plugin=protoc-gen-grpc=/usr/bin/grpc_python_plugin --python_out=. --grpc_out=. --proto_path=. ./proto/*.proto
