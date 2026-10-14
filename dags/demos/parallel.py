"""Meeting example 4: independent tasks can run together before a final task."""

from datetime import datetime, timezone
from time import sleep

from airflow.sdk import dag, task


@dag(
    dag_id="demo_04_parallel",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    is_paused_upon_creation=True,
    tags=["workshop-demo"],
)
def parallel_demo():
    @task(retries=0)
    def prepare():
        print("Both independent jobs can now start.")

    @task(retries=0)
    def job_a():
        print("Job A started.")
        # Simulate work.
        # The delay lets students compare the two jobs' execution times.
        sleep(8)
        print("Job A finished.")

    @task(retries=0)
    def job_b():
        print("Job B started.")
        sleep(8)
        print("Job B finished.")

    @task(retries=0)
    def finish():
        print("Both jobs succeeded; the workflow can finish.")

    start = prepare()
    jobs = [job_a(), job_b()]
    end = finish()
    start >> jobs >> end


parallel_demo()
