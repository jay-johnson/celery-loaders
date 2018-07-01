Examples for Celery Applications and Task Loading
=================================================

This is an example for running Celery applications that demonstrates how to load multiple task modules from different files using environment variables. It also shows how to utilize a ``get celery config`` approach that allows for decoupling inclusion of tasks from the initialization of the Celery application. It also includes a derived Celery task called ``CustomTask`` for showing how to handle ``on_success`` and ``on_failure`` task control events. I find this easier to manage my Celery workers and the applications that publish tasks to them.

This is not an official Celery project, it is just examples I use to test my workers and tasks.

I hope you find it valuable.

Install
-------

::

    pip install celery-loaders

Start Redis
-----------

This is only needed if redis is not running already on port 6739. It also requires having docker and docker-compose available to your user.

::

    ./run-redis.sh

Start Celery Worker
-------------------

Please run this from the base repository directory or the module paths to the Celery tasks will fail.

::

    ./run-celery-loaders-worker.sh 
    Starting Worker=celery_worker
    celery worker -A celery_worker -c 1 -l INFO -n default@%h
    2018-02-24 13:01:49,843 - worker - INFO - start - worker
    2018-02-24 13:01:49,843 - worker - INFO - broker=redis://localhost:6379/9 backend=redis://localhost:6379/10 include_tasks=['celery_loaders.work_tasks.tasks', 'celery_loaders.work_tasks.always_fails_tasks']
    2018-02-24 13:01:49,844 - get_celery_app - INFO - creating celery app=worker tasks=['celery_loaders.work_tasks.tasks', 'celery_loaders.work_tasks.always_fails_tasks']
    2018-02-24 13:01:49,845 - worker - INFO - starting celery
    
    -------------- default@dev v4.1.0 (latentcall)
    ---- **** ----- 
    --- * ***  * -- Linux-4.13.0-16-generic-x86_64-with-Ubuntu-17.10-artful 2018-02-24 13:01:49
    -- * - **** --- 
    - ** ---------- [config]
    - ** ---------- .> app:         worker:0x7f384346e550
    - ** ---------- .> transport:   redis://localhost:6379/9
    - ** ---------- .> results:     redis://localhost:6379/10
    - *** --- * --- .> concurrency: 1 (prefork)
    -- ******* ---- .> task events: OFF (enable -E to monitor tasks in this worker)
    --- ***** ----- 
    -------------- [queues]
                    .> celery           exchange=celery(direct) key=celery
                    

    [tasks]
    . celery_loaders.work_tasks.always_fails_tasks.always_fails
    . celery_loaders.work_tasks.tasks.do_some_work

    2018-02-24 13:01:49,956 - celery.worker.consumer.connection - INFO - Connected to redis://localhost:6379/9
    2018-02-24 13:01:49,963 - celery.worker.consumer.mingle - INFO - mingle: searching for neighbors
    2018-02-24 13:01:50,981 - celery.worker.consumer.mingle - INFO - mingle: all alone
    2018-02-24 13:01:51,013 - celery.apps.worker - INFO - default@dev ready.

Run Success and Failure Tests
-----------------------------

Run this in another terminal with the ``celery_loaders`` pip available to the python 3 runtime.

::

    ./run-celery-loaders-tests.py 
    2018-02-24 13:01:56,768 - worker - INFO - start - worker
    2018-02-24 13:01:56,768 - worker - INFO - broker=redis://localhost:6379/9 backend=redis://localhost:6379/10 include_tasks=['celery_loaders.work_tasks.tasks', 'celery_loaders.work_tasks.always_fails_tasks']
    2018-02-24 13:01:56,768 - worker - INFO - broker=redis://localhost:6379/9 backend=redis://localhost:6379/10
    2018-02-24 13:01:56,769 - get_celery_app - INFO - creating celery app=worker tasks=['celery_loaders.work_tasks.tasks', 'celery_loaders.work_tasks.always_fails_tasks']
    2018-02-24 13:01:56,781 - worker - INFO - calling task - success testing
    2018-02-24 13:01:56,822 - worker - INFO - calling task=celery_loaders.work_tasks.tasks.do_some_work - success job_id=3dcd5066-46fe-43cc-b0c6-8cff5499a7b1
    2018-02-24 13:01:56,822 - worker - INFO - calling task - failure testing
    2018-02-24 13:01:56,823 - worker - INFO - calling task=celery_loaders.work_tasks.always_fails_tasks.always_fails - failure job_id=c6f91e65-f541-40ad-9226-eaf97b223723
    2018-02-24 13:01:56,823 - worker - INFO - end - worker

Confirm the Celery Worker Processed the Tasks
---------------------------------------------

::

    2018-02-24 13:01:56,822 - celery.worker.strategy - INFO - Received task: celery_loaders.work_tasks.tasks.do_some_work[3dcd5066-46fe-43cc-b0c6-8cff5499a7b1]  
    2018-02-24 13:01:56,824 - tasks - INFO - task - do_some_work - start work_dict={'user_id': 1}
    2018-02-24 13:01:56,824 - tasks - INFO - task - do_some_work - done
    2018-02-24 13:01:56,828 - custom_task - INFO - custom_task SUCCESS - retval=True task_id=3dcd5066-46fe-43cc-b0c6-8cff5499a7b1 args=[{'user_id': 1}] kwargs={}
    2018-02-24 13:01:56,828 - celery.app.trace - INFO - Task celery_loaders.work_tasks.tasks.do_some_work[3dcd5066-46fe-43cc-b0c6-8cff5499a7b1] succeeded in 0.004043873999762582s: True
    2018-02-24 13:01:57,007 - celery.worker.strategy - INFO - Received task: celery_loaders.work_tasks.always_fails_tasks.always_fails[c6f91e65-f541-40ad-9226-eaf97b223723]  
    2018-02-24 13:01:57,009 - always_fails_tasks - INFO - task - always_fails - start work_dict={'test_failure': 'Should fail now 2018-02-24T13:01:56.781481'}
    2018-02-24 13:01:57,010 - custom_task - ERROR - custom_task FAIL - exc=Should fail now 2018-02-24T13:01:56.781481 args=[{'test_failure': 'Should fail now 2018-02-24T13:01:56.781481'}] kwargs={}
    2018-02-24 13:01:57,010 - celery.app.trace - ERROR - Task celery_loaders.work_tasks.always_fails_tasks.always_fails[c6f91e65-f541-40ad-9226-eaf97b223723] raised unexpected: Exception('Should fail now 2018-02-24T13:01:56.781481',)
    Traceback (most recent call last):
    File "/home/jay/.venvs/celeryloaders/lib/python3.6/site-packages/celery/app/trace.py", line 374, in trace_task
        R = retval = fun(*args, **kwargs)
    File "/home/jay/.venvs/celeryloaders/lib/python3.6/site-packages/celery/app/trace.py", line 629, in __protected_call__
        return self.run(*args, **kwargs)
    File "/opt/redten/stack/jwt/webapp/celery_examples/build/lib/celery_loaders/work_tasks/always_fails_tasks.py", line 32, in always_fails
        "simulating a failure"))
    Exception: Should fail now 2018-02-24T13:01:56.781481

Debug a Celery Task from the Command Line
-----------------------------------------

#.  Start a named Celery Task and pass in data from a file containing a testing JSON payload

    ::

        ./run-celery-task.py -f tests/data/user_lookup_test.json -t celery_loaders.work_tasks.tasks.do_some_work -w 5.0
        2018-02-26 00:11:50,192 - run-celery-task - INFO - start - run-celery-task
        2018-02-26 00:11:50,192 - run-celery-task - INFO - connecting Celery=run-celery-task broker=redis://localhost:6379/9 backend=redis://localhost:6379/10 tasks=['celery_loaders.work_tasks.tasks']
        2018-02-26 00:11:50,192 - get_celery_app - INFO - creating celery app=run-celery-task tasks=['celery_loaders.work_tasks.tasks']
        2018-02-26 00:11:50,207 - run-celery-task - INFO - app.broker_url=redis://localhost:6379/9 calling task=celery_loaders.work_tasks.tasks.do_some_work data={'user_id': 1}
        2018-02-26 00:11:50,264 - run-celery-task - INFO - calling task=celery_loaders.work_tasks.tasks.do_some_work - started job_id=561c80bc-0bab-4387-a842-4372d11c8291
        2018-02-26 00:11:50,264 - run-celery-task - INFO - task=561c80bc-0bab-4387-a842-4372d11c8291 - waiting seconds=5.0 for results
        2018-02-26 00:11:50,268 - run-celery-task - INFO - task=celery_loaders.work_tasks.tasks.do_some_work - success job_id=561c80bc-0bab-4387-a842-4372d11c8291 task_result={'job_results': 'some response key=c60adfdc-e27c-41f4-8440-666be599ab4a'}
        2018-02-26 00:11:50,268 - run-celery-task - INFO - end - run-celery-task

#.  Verify the Worker Processed the Task

    ::

        2018-02-26 00:11:50,265 - celery.worker.strategy - INFO - Received task: celery_loaders.work_tasks.tasks.do_some_work[561c80bc-0bab-4387-a842-4372d11c8291]  
        2018-02-26 00:11:50,266 - tasks - INFO - task - do_some_work - start work_dict={'user_id': 1}
        2018-02-26 00:11:50,266 - tasks - INFO - task - {'job_results': 'some response key=c60adfdc-e27c-41f4-8440-666be599ab4a'} - result=do_some_work done
        2018-02-26 00:11:50,267 - custom_task - INFO - custom_task SUCCESS - retval={'job_results': 'some response key=c60adfdc-e27c-41f4-8440-666be599ab4a'} task_id=561c80bc-0bab-4387-a842-4372d11c8291 args=[{'user_id': 1}] kwargs={}
        2018-02-26 00:11:50,268 - celery.app.trace - INFO - Task celery_loaders.work_tasks.tasks.do_some_work[561c80bc-0bab-4387-a842-4372d11c8291] succeeded in 0.001375271000142675s: {'job_results': 'some response key=c60adfdc-e27c-41f4-8440-666be599ab4a'}

Development
-----------

::

    virtualenv -p python3 ~/.venvs/celeryloaders && source ~/.venvs/celeryloaders/bin/activate && pip install -e .
    
Run tests

::

    python setup.py test    

Linting
-------

::

    flake8 .
    pycodestyle .

License
=======

Apache 2.0

