#!/usr/bin/env python

import os
import datetime
from celery import signals
from celery_loaders.log.setup_logging import build_colorized_logger
from celery_loaders.work_tasks.get_celery_app import get_celery_app


# Disable celery log hijacking
# https://github.com/celery/celery/issues/2509
@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


name = "run-tests"
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

log.info(("broker={} backend={}")
         .format(
             broker_url,
             backend_url))

# Get the Celery app project's get_celery_app
app = get_celery_app(
    name=name,
    auth_url=broker_url,
    backend_url=backend_url,
    include_tasks=include_tasks)

# if you want to discover tasks in other directories:
# app.autodiscover_tasks(["some_dir_name_with_tasks"])

user_lookup_data = {
    "user_id": 1
}
failure_test_data = {
    "test_failure": "Should fail now {}".format(
                        datetime.datetime.now().isoformat())
}

log.info("calling task - success testing")
path_to_tasks = "celery_loaders.work_tasks.tasks"
task_name = ("{}.do_some_work").format(
                path_to_tasks)
job_id = app.send_task(
    task_name,
    (user_lookup_data,))
log.info(("calling task={} - success job_id={}")
         .format(
             task_name,
             job_id))

log.info("calling task - failure testing")
path_to_tasks = "celery_loaders.work_tasks.always_fails_tasks"
fails_task_name = ("{}.always_fails").format(
                    path_to_tasks)
job_id = app.send_task(
    fails_task_name,
    (failure_test_data,))
log.info(("calling task={} - failure job_id={}")
         .format(
             fails_task_name,
             job_id))

log.info(("end - {}")
         .format(name))
