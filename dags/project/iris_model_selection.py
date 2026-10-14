"""Main project: Airflow runs five notebooks; the notebooks contain the ML code."""

from datetime import datetime, timezone
from pathlib import Path

from airflow.sdk import dag, get_current_context, task

# Locate the project folder.
# This DAG is two folders below the root, which contains notebooks/ and outputs/.
PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dag(
    dag_id="iris_model_selection",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    max_active_runs=1,
    tags=["workshop-main"],
    doc_md=(
        "## Iris model selection\n"
        "Each task runs one notebook from **notebooks/**. "
        "Load and split data, train both approaches, compare accuracy, "
        "and register the winner with the **candidate** alias."
    ),
)
def iris_model_selection():
    @task(retries=0)
    def run_notebook(notebook_file):
        import papermill as pm

        # Identify the current workflow execution.
        # Its run ID gives all five notebook tasks the same separate output folder.
        context = get_current_context()
        run_id = context["run_id"]
        folder_name = run_id.replace(":", "_").replace("+", "_")
        run_path = PROJECT_ROOT / "outputs" / folder_name
        run_path.mkdir(parents=True, exist_ok=True)

        input_path = PROJECT_ROOT / "notebooks" / notebook_file
        output_path = run_path / notebook_file
        print("Executing notebook:", input_path)

        # Execute the notebook with Papermill.
        # Inject its inputs, use the registered kernel, and forward printed output to
        # Airflow logs.
        pm.execute_notebook(
            input_path=str(input_path),
            output_path=str(output_path),
            parameters={
                "project_root": str(PROJECT_ROOT),
                "run_dir": str(run_path),
                "workflow_run_id": run_id,
            },
            kernel_name="mlops-workshop-airflow",
            cwd=str(PROJECT_ROOT),
            log_output=True,
        )
        print("Executed copy:", output_path)
        return str(output_path)

    # Create the five task nodes.
    # Each call uses the same runner with a different notebook and visible task ID.
    load_and_split = run_notebook.override(task_id="load_and_split")(
        "01_load_and_split.ipynb"
    )
    train_logistic = run_notebook.override(task_id="train_logistic")(
        "02_train_logistic.ipynb"
    )
    train_random_forest = run_notebook.override(task_id="train_random_forest")(
        "03_train_random_forest.ipynb"
    )
    compare_models = run_notebook.override(task_id="compare_models")(
        "04_compare_models.ipynb"
    )
    register_candidate = run_notebook.override(task_id="register_candidate")(
        "05_register_candidate.ipynb"
    )

    # Set the execution dependencies.
    # Training shares one split; comparison waits for both models before registration
    # starts.
    load_and_split >> [train_logistic, train_random_forest]
    [train_logistic, train_random_forest] >> compare_models >> register_candidate


iris_model_selection()
