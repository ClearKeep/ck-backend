
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

then

> sh run.sh

## Generated protobuf file
From root project

> sh run.sh -p
