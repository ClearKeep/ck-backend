# syntax = docker/dockerfile:1.3
# Must have this syntax line for pip cache to work, buildkit



# This is a Multi-stage build



# How to run
# sudo DOCKER_BUILDKIT=1  docker build -t clearkeep-main-module   --progress=plain    -f ./.docker/clearkeep-main-module-multi-stage.dockerfile .
# sudo DOCKER_BUILDKIT=1  docker run --rm --name clearkeep-main-module \
#            --mount type=bind,source="$(pwd)",target=/clearkeep-main-module-source  \
#            -p 5000:5000 clearkeep-main-module




# TODO: Working on the things, bind mount the source, not working

# sudo DOCKER_BUILDKIT=1  docker run --rm  --add-host=postgres-db:10.0.255.157   --name clearkeep-main-module             --mount type=bind,source="$(pwd)",target=/clearkeep-main-module-source       -p 5000:5000 clearkeep-main-module

# sudo DOCKER_BUILDKIT=1  docker run --rm  --add-host=postgres-db:10.0.255.157   --name clearkeep-main-module             --mount type=bind,source="$(pwd)",target=/clearkeep-main-module-source-code       -p 5000:5000 clearkeep-main-module





# First stage
FROM python:3.8 AS builder
COPY requirements.txt .






# TODO: RS Why not in the requirements.txt ?
#     dbapi = dialect_cls.dbapi(**dbapi_args)
#   File "/root/.local/lib/python3.8/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py", line 778, in dbapi
#     import psycopg2
#   File "/root/.local/lib/python3.8/site-packages/psycopg2/__init__.py", line 51, in <module>
#     from psycopg2._psycopg import (                     # noqa
# ImportError: libpq.so.5: cannot open shared object file: No such file or directory

# RUN --mount=type=cache,target=/root/.cache \
#     pip install --user psycopg2

RUN --mount=type=cache,target=/root/.cache \
    pip install --user psycopg2




# install dependencies to the local user directory (eg. /root/.local)
RUN --mount=type=cache,target=/root/.cache \
    pip install --user -r requirements.txt









# Second stage



# Must have this `$ export DOCKER_BUILDKIT=1`

FROM python:3.8-slim
WORKDIR /clearkeep-main-module-source-code

# copy only the dependencies installation from the 1st stage image
COPY --from=builder /root/.local /root/.local
COPY ./ ./



# update PATH environment variable
ENV PATH=/root/.local:$PATH




# TODO: RS Why not in the requirements.txt ?
#     dbapi = dialect_cls.dbapi(**dbapi_args)
#   File "/root/.local/lib/python3.8/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py", line 778, in dbapi
#     import psycopg2
#   File "/root/.local/lib/python3.8/site-packages/psycopg2/__init__.py", line 51, in <module>
#     from psycopg2._psycopg import (                     # noqa
# ImportError: libpq.so.5: cannot open shared object file: No such file or directory

# RUN --mount=type=cache,target=/root/.cache \
#     pip install --user psycopg2

# RUN --mount=type=cache,target=/root/.cache \
#     pip install psycopg2





# TODO: make sure this ok
# generate protobuf
RUN sh protos/gen.sh


EXPOSE 5000


ENV ENV=local-from-clk328-c18-group-chat-thanh-max-prod-2

CMD [ "python", "./app_http.py" ]
CMD [ "python", "./app_grpc.py" ]



