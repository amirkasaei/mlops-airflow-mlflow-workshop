"""Meeting example 3: a temporary failure succeeds on the second attempt."""

from datetime import datetime, timedelta, timezone

from airflow.sdk import dag, get_current_context, task


@dag(
    dag_id="demo_03_retry",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    is_paused_upon_creation=True,
    tags=["workshop-demo"],
)
def retry_demo():
    # One retry means up to two attempts. Wait long enough to observe Up for retry.
    @task(retries=1, retry_delay=timedelta(seconds=5))
    def temporary_failure():
        context = get_current_context()
        attempt = context["ti"].try_number
        print(f"Attempt number: {attempt}")

        if attempt == 1:
            raise ConnectionError("Simulated temporary problem: the first attempt fails.")

        print("The second attempt succeeded.")

    @task(retries=0)
    def finish():
        print("The workflow continued after the retry succeeded.")

    temporary_failure() >> finish()


retry_demo()
