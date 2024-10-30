from rq import Queue
from redis import Redis
import time
from rq.job import Job

# Connect to Redis server
redis_conn = Redis()

# Create a queue
queue = Queue(connection=redis_conn)


def example_task(n):
    """A simple task that sleeps for n seconds."""
    print(f"Task started: sleeping for {n} seconds")
    time.sleep(n)
    print("Task completed")
    return f"Slept for {n} seconds"


def get_task_result(job_id):
    job = Job.fetch(job_id, connection=redis_conn)
    if job.is_finished:
        return job.result
    elif job.is_failed:
        return f"Task failed: {job.exc_info}"
    else:
        return f"Task is {job.get_status()}"


def list_all_jobs():
    """List all jobs in the queue."""
    jobs = queue.jobs
    job_list = []
    for job in jobs:
        job_list.append(
            {
                "id": job.id,
                "status": job.get_status(),
                "result": job.result if job.is_finished else None,
            }
        )
    return job_list
