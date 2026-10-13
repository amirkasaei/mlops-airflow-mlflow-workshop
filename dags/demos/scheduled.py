"""Meeting example 6: the scheduler creates runs without a manual trigger."""

from datetime import datetime, timedelta, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="demo_06_scheduled",
    schedule=timedelta(seconds=20),  # Make a run eligible every 20 seconds.
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,  # Do not create runs for every interval since the start date.
    is_paused_upon_creation=True,  # Students explicitly enable this demonstration.
    max_active_runs=1,
    tags=["workshop-demo"],
)
def scheduled_demo():
    @task(retries=0)
    def report_time():
        print("The scheduler started this task.")
        print("Current UTC time:", datetime.now(timezone.utc).isoformat())

    report_time()


scheduled_demo()
