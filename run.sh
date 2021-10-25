#!/bin/bash

export PYTHONPATH=./

ARG=$1
if [ ${#ARG} -gt 0 ]; then
    if [ $ARG == '-p' ] || [ $ARG == '-proto' ]; then
        sh proto/gen.sh
        echo "gen protobuf file success"
    else
        python app.py
    fi
else
    python app.py
fi