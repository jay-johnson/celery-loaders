#!/usr/bin/env python

import os
from celery import signals
from celery_loaders.log.setup_logging import build_colorized_logger
from celery_loaders.work_tasks.get_celery_app import get_celery_app


# Disable celery log hijacking
# https://github.com/celery/celery/issues/2509
@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


name = "worker"
log = build_colorized_logger(name=name)

log.info(("start - {}")
         .format(name))

broker_url = os.getenv(
    "WORKER_BROKER_URL",
    "redis://localhost:6379/9").strip().lstrip()
backend_url = os.getenv(
    "WORKER_BACKEND_URL",
    "redis://localhost:6379/10").strip().lstrip()

# comma delimited list of task module files:
tasks_str = os.getenv(
    "WORKER_TASKS",
    ("celery_loaders.work_tasks.tasks,"
     "celery_loaders.work_tasks.always_fails_tasks"))
include_tasks = tasks_str.split(",")

ssl_options = {}
transport_options = {}

log.info(("broker={} backend={} include_tasks={}")
         .format(
            broker_url,
            backend_url,
            include_tasks))

# Get the Celery app from the project's get_celery_app module
app = get_celery_app(
    name=name,
    auth_url=broker_url,
    backend_url=backend_url,
    include_tasks=include_tasks)

log.info("starting celery")
app.start()

log.info(("end - {}")
         .format(name))
