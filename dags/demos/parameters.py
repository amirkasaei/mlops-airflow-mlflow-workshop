"""Meeting example 5: choose a run parameter and pass a result between tasks."""

from datetime import datetime, timezone

from airflow.sdk import Param, dag, get_current_context, task


@dag(
    dag_id="demo_05_parameters",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    is_paused_upon_creation=True,
    tags=["workshop-demo"],
    params={
        "student_name": Param(
            "Student", type="string", minLength=1, title="Student name"
        ),
    },
)
def parameters_demo():
    @task(retries=0)
    def make_message():
        # Read the trigger parameter.
        # Airflow places this run's Student name value in the task context.
        context = get_current_context()
        name = context["params"]["student_name"]
        return f"Hello, {name}!"

    @task(retries=0)
    def display_message(message):
        # Consume the previous task's output.
        # Airflow retrieves the returned greeting through XCom and passes it as
        # message.
        print(message)

    message = make_message()
    display_message(message)


parameters_demo()
