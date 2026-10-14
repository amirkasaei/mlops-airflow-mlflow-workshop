"""Meeting example 2: a failed task prevents its dependent task from running."""

from datetime import datetime, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="demo_02_failure",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    is_paused_upon_creation=True,
    tags=["workshop-demo"],
)
def failure_demo():
    @task(retries=0)
    def prepare():
        print("Preparation succeeded.")

    @task(retries=0)
    def fail_on_purpose():
        # Demonstrate task failure.
        # An exception stops this task; printing an error alone would not fail it.
        raise ValueError("Intentional workshop failure: this task always fails.")

    @task(retries=0)
    def finish():
        print("This cannot run because its required upstream task failed.")

    # Require successful upstream tasks.
    # The default rule prevents finish from executing after the intentional failure.
    prepare() >> fail_on_purpose() >> finish()


failure_demo()
