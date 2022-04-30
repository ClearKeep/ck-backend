export PYTHONPATH=./
export PYTHONUNBUFFERED=1
export ENV=thanhpt1-vmo_dev
export GRPC_VERBOSITY=DEBUG
export GRPC_TRACE=tcp,http

echo "Generating the protobuf files, do not need to do this if the .proto files do not change"
# Use venv's python Avoid use the system-wide python
venv/bin/python -m grpc_tools.protoc -I=. protos/*.proto --python_out=. --grpc_python_out=.

venv/bin/python app_grpc.py 2>&1 | tee thanhpt1-vmo_app_grpc_console_m1.log &
venv/bin/python app_http.py 2>&1 | tee thanhpt1-vmo_app_http_console_m1.log &


# LOG=debug node t41_from_t39.js 1 $(dig +short dev1.clearkeep.org) 2>&1 | tee thanhpt1-vmo_orbit-db_console.log

# DOCKER_BUILDKIT=1 docker-compose --project-name thanhpt1-vmo-self-contained-m1  -f .docker/thanhpt1-vmo-docker-compose-2.yml down --remove-orphans --volumes


# DOCKER_BUILDKIT=1 docker-compose --project-name thanhpt1-vmo-self-contained-m1  -f .docker/thanhpt1-vmo-docker-compose-2.yml up  --remove-orphans   2>&1 | tee thanhpt1-vmo_docker-compose-console-m1.log


