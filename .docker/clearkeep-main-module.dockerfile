

# sudo DOCKER_BUILDKIT=1  docker build -t clearkeep-main-module   --progress=plain    -f ./.docker/clearkeep-main-module.dockerfile .
# sudo DOCKER_BUILDKIT=1  docker run --name clearkeep-main-module \
#            --mount type=bind,source="$(pwd)",target=/clearkeep-main-module-source  \
#            -p 5000:5000 clearkeep-main-module



# Must have this `$ export DOCKER_BUILDKIT=1`
# Must have this syntax line for pip cache to work, buildkit
# syntax = docker/dockerfile:1.3
FROM python:3.8



# During development, our application’s dependencies change less frequently than the Python code. 
# Because of this, we choose to install the dependencies in a layer preceding the code one. 
# Therefore we copy the dependencies file and install them and then we copy the source code. 
# This is the main reason why we isolated the source code to a dedicated directory in our project structure
# copy the dependencies file to the working directory
COPY requirements.txt .



#RUN pip install -r requirements.txt
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt



COPY . /clearkeep-main-module-source
WORKDIR /clearkeep-main-module-source



# setup library

# TODO: Want to pin pip version
RUN pip install --upgrade pip






# TODO: RS Why not in the requirements.txt ?
RUN pip install psycopg2

# TODO: make sure this ok
# generate protobuf
RUN sh protos/gen.sh


EXPOSE 5000


ENV ENV=local-from-clk328-c18-group-chat-thanh-max-prod

# start application
CMD python ./app_grpc.py
CMD python ./app_http.py
