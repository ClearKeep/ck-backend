#!/usr/bin/env bash

python3 -m grpc_tools.protoc -I. protos/stream.proto --python_out=. --grpclib_python_out=.
