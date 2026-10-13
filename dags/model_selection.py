"""Main Iris workflow: load the dataset, then make a shared train/test split."""

from datetime import datetime, timezone

from airflow.sdk import dag, task


# Define the workflow. schedule=None means we trigger it from the Airflow UI.
@dag(
    dag_id="iris_model_selection",
    schedule=None,
    start_date=datetime(2025, 1, 1, tzinfo=timezone.utc),
    catchup=False,
    tags=["workshop-main"],
    doc_md=(
        "## Main Iris workflow\n"
        "Current steps: **load_data → split_data**. "
        "Training and MLflow integration will be added next. "
        "The separate **workshop-demo** DAGs demonstrate Airflow features."
    ),
)
def iris_model_selection():
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

    @task
    def split_data(data):
        from sklearn.model_selection import train_test_split

        # Keep 20% of the rows for testing. A fixed seed makes the split repeatable.
        # Stratification keeps the three flower classes balanced in both groups.
        X_train, X_test, y_train, y_test = train_test_split(
            data["X"],
            data["y"],
            test_size=0.2,
            random_state=42,
            stratify=data["y"],
        )
        print(f"Split Iris: {len(X_train)} training rows, {len(X_test)} test rows.")

        # Both future model-training tasks will use this same split.
        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test,
            "feature_names": data["feature_names"],
            "target_names": data["target_names"],
        }

    # Passing the first task's output creates the dependency automatically.
    data = load_data()
    split_data(data)


# Create the DAG definition so Airflow can discover it in the dags folder.
iris_model_selection()
