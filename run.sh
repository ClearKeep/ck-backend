#!/bin/bash

#export PYTHONPATH=./
#
#ARG=$1
#if [ ${#ARG} -gt 0 ]; then
#    if [ $ARG == '-p' ] || [ $ARG == '-proto' ]; then
#        sh proto/gen.sh
#        echo "gen protobuf file success"
#    else
#        python app.py
#    fi
#else
#    python app.py
#fi


echo "REMEMBER!!! generate protobuf files"
export PYTHONPATH=./
export PYTHONUNBUFFERED=1
export ENV=development
export GRPC_VERBOSITY=DEBUG
export GRPC_TRACE=tcp,http


python app_grpc.py
python app_http.py


