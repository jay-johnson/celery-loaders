#!/bin/bash

if [[ -e ~/.venvs/celeryloaders/bin/activate ]]; then
    source ~/.venvs/celeryloaders/bin/activate
fi

cd celery_loaders
num_workers=4
log_level=DEBUG
worker_module=celery_worker
worker_name="default@%h"

if [[ "${NUM_WORKERS}" != "" ]]; then
    num_workers=$NUM_WORKERS
fi
if [[ "${LOG_LEVEL}" != "" ]]; then
    log_level=$LOG_LEVEL
fi
if [[ "${WORKER_MODULE}" != "" ]]; then
    worker_module=$WORKER_MODULE
fi
if [[ "${WORKER_NAME}" != "" ]]; then
    worker_name=$WORKER_NAME
fi

echo ""
echo "Starting Workers=${worker_module}"
echo "celery worker -A ${worker_module} -c ${num_workers} -l ${log_level} -n ${worker_name}"
celery worker -A $worker_module -c ${num_workers} -l ${log_level} -n ${worker_name}
echo ""
