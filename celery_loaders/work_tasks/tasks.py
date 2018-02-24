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

    log.info(("task - {} - done")
             .format(label))

    return True
# end of do_some_work
