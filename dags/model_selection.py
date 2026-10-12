"""Workshop DAG: build the model-selection workflow one task at a time."""

from datetime import datetime, timezone

from airflow.sdk import dag, task


# Define the workflow. schedule=None means we trigger it from the Airflow UI.
@dag(
    dag_id="iris_model_selection",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
)
def model_selection():
    # Airflow treats this function as a separate task with its own status and logs.
    @task
    def load_data():
        from sklearn.datasets import load_iris

        # Iris is bundled with scikit-learn, so no download is needed.
        iris = load_iris()
        print(f"Loaded Iris: {len(iris.data)} rows, {len(iris.feature_names)} features.")

        # Simple lists let Airflow pass this tiny dataset to the next task later.
        return {
            "X": iris.data.tolist(),
            "y": iris.target.tolist(),
            "feature_names": iris.feature_names,
            "target_names": iris.target_names.tolist(),
        }

    # Create the task node. Airflow executes its body when the DAG is triggered.
    load_data()


# Create the DAG definition so Airflow can discover it in the dags folder.
model_selection()
