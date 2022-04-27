#!/bin/bash

set -m

/iris-main "$@" &

/usr/irissys/dev/Cloud/ICM/waitISC.sh

cd ${SRC_PATH}/src/python/

${PYTHON_PATH} -m gunicorn --bind "0.0.0.0:8080" wsgi:app &

fg %1