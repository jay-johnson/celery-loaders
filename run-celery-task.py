#!/usr/bin/env python

import os
import sys
import json
import argparse
from celery import signals
from celery_loaders.log.setup_logging import build_colorized_logger
from celery_loaders.work_tasks.get_celery_app import get_celery_app


name = "run-celery-task"
log = build_colorized_logger(name=name)

parser = argparse.ArgumentParser(description="sending Celery task data")
parser.add_argument(
    "-f",
    help="task data file: path to data file",
    required=True,
    dest="data_file")
parser.add_argument(
    "-t",
    help="task name: celery_loaders.work_tasks.tasks.do_some_work",
    required=True,
    dest="task_name")
parser.add_argument(
    "-w",
    "--time-for-result",
    help="get the task's result after waiting (default 1.0 seconds)",
    required=False,
    dest="time_for_result")
args = parser.parse_args()


task_name = args.task_name
task_data = None
get_task_result = False
time_to_wait_for_result = 1.0
if args.data_file:
    if os.path.exists(args.data_file):
        task_data = json.loads(open(args.data_file).read())
# end of loading the data to send

if args.time_for_result:
    get_task_result = True
    try:
        time_to_wait_for_result = float(args.time_for_result)
    except Exception as e:
        time_to_wait_for_result = 1.0
        log.error(("Invalid time_for_result={} "
                   "please use a float or int")
                  .format(
                      args.time_for_result))
    # end of try/ex
# end of if waiting for the result

if not task_data:
    log.error(("Please provide a "
               "path to task_data file with -f <path to file>"))
    sys.exit(1)
# end of checking if there is data to send


# Disable celery log hijacking
# https://github.com/celery/celery/issues/2509
@signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    pass


log.info(("start - {}")
         .format(name))

broker_url = os.getenv(
    "BROKER_URL",
    "redis://localhost:6379/9").strip().lstrip()
backend_url = os.getenv(
    "BACKEND_URL",
    "redis://localhost:6379/10").strip().lstrip()

# comma delimited
tasks_str = os.getenv(
    "INCLUDE_TASKS",
    "celery_loaders.work_tasks.tasks")
include_tasks = tasks_str.split(",")

log.info(("connecting Celery={} "
          "broker={} backend={} tasks={}")
         .format(
            name,
            broker_url,
            backend_url,
            include_tasks))

# Get the Celery app using the celery-loaders api
app = get_celery_app(
        name,
        auth_url=broker_url,
        backend_url=backend_url,
        include_tasks=include_tasks)

log.info(("app.broker_url={} calling task={} data={}")
         .format(
            app.conf.broker_url,
            task_name,
            task_data))
task_job = app.send_task(
    task_name,
    (task_data,))
log.info(("calling task={} - started job_id={}")
         .format(
            task_name,
            task_job.id))

if get_task_result:
    log.info(("task={} - waiting seconds={} "
              "for results")
             .format(
                 task_job.id,
                 time_to_wait_for_result))
    task_job.get(timeout=time_to_wait_for_result)
    log.info(("task={} - success "
              "job_id={} task_result={}")
             .format(
                task_name,
                task_job.id,
                task_job.result))
# end of if getting task result is enabled

log.info(("end - {}")
         .format(name))

sys.exit(0)
