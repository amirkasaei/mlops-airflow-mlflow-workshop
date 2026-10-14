"""Meeting example 6: the scheduler creates runs without a manual trigger."""

from datetime import datetime, timedelta, timezone

from airflow.sdk import dag, task


@dag(
    dag_id="demo_06_scheduled",
    # Let the scheduler create periodic runs; no manual trigger is required.
    schedule=timedelta(seconds=20),
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    # Start with current intervals rather than all intervals since start_date.
    catchup=False,
    # Keep the demo paused until students explicitly enable scheduling.
    is_paused_upon_creation=True,
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
