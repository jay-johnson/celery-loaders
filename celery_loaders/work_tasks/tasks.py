import uuid
from celery.task import task
from celery_loaders.log.setup_logging import build_colorized_logger
from celery_loaders.work_tasks.custom_task import CustomTask


name = "tasks"
log = build_colorized_logger(name=name)


@task(
    bind=True,
    base=CustomTask,
    queue="do_some_work")
def do_some_work(
        self,
        work_dict):
    """do_some_work

    :param work_dict: dictionary for key/values
    """

    label = "do_some_work"

    log.info(("task - {} - start "
              "work_dict={}")
             .format(label,
                     work_dict))

    ret_data = {
        "job_results": ("some response key={}").format(
                            str(uuid.uuid4()))
    }

    log.info(("task - {} - result={} done")
             .format(
                 ret_data,
                 label))

    return ret_data
# end of do_some_work
