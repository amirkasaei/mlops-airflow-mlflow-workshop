"""Meeting example 1: two tasks finish successfully in order."""

from datetime import datetime, timezone
from time import sleep

from airflow.sdk import dag, task


@dag(
    dag_id="demo_01_success",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    is_paused_upon_creation=True,
    tags=["workshop-demo"],
)
def success_demo():
    @task(retries=0)
    def first_task():
        print("First task is running.")
        # Simulate a short job.
        # The delay makes the Running state visible during the demonstration.
        sleep(3)
        print("First task finished.")

    @task(retries=0)
    def second_task():
        print("Second task starts after the first succeeds.")
        sleep(3)
        print("Second task finished.")

    # Set the task order.
    # second_task becomes eligible only after first_task succeeds.
    first_task() >> second_task()


success_demo()
