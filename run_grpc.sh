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


source ./run_common.sh

# Use venv's python Avoid use the system-wide python
./venv/bin/python app_grpc.py


