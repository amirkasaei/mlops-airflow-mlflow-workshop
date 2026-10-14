# One shared dataset and experiment

[Walkthrough index](../09-code-walkthrough.md) | [Previous](07-main-dag.md) | [Next](09-train-logistic.md)

**Source:** [01_load_and_split.ipynb](../../notebooks/01_load_and_split.ipynb).

Prepare identical inputs for both model approaches. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Inputs and MLflow connection

The tagged parameters cell lets Airflow supply the project path, execution folder, and run ID. For manual execution the defaults locate the project and use outputs/manual/. The connection cell points tracking and registry operations at the same absolute mlflow.db path.

## Load, split, and save

load_iris(as_frame=True) gives named feature columns and labels. The fixed seed and stratify=y make one repeatable split: 120 training rows and 30 test rows. Both models later read exactly those rows.

split.json stores data as lists, feature names, settings, and execution identity. workflow_run_id supplies that identity under Airflow; uuid4 creates a fresh one for a manual run. Later tasks reject stale records with a different identity.

## Prepare the experiment

The final cell creates iris-pipeline-comparison only if missing, with artifacts under mlartifacts/pipeline, and selects it. This notebook creates no training run.

## Understand the connection commands

These are Python function calls from the MLflow library. They configure where later calls read and write; they do not start the UI.

```python
mlflow.set_tracking_uri(tracking_uri)
mlflow.set_registry_uri(tracking_uri)
client = MlflowClient()
```

| Call | Meaning in this project |
| --- | --- |
| `set_tracking_uri(tracking_uri)` | Choose the store for experiments, runs, parameters, metrics, and trace records. |
| `set_registry_uri(tracking_uri)` | Choose the store for registered model names, versions, and aliases. We use the same database. |
| `MlflowClient()` | Create an object for explicitly reading and updating records, such as `client.get_run(run_id)`. It uses the configured stores. |

`tracking_uri` is a connection address: `sqlite:///` followed by the absolute path to `mlflow.db`. SQLite creates a local database file; there is no database username/password here. The database holds records and references. Saved model files and other artifacts live under `mlartifacts/`. The UI must open the same database to display these records.

We configure these connections in every notebook because Airflow runs each notebook in a separate Python process. Selecting an experiment in one process does not select it in the next.

## Understand the experiment commands

```python
if client.get_experiment_by_name(experiment_name) is None:
    client.create_experiment(
        experiment_name,
        artifact_location=(project_path / "mlartifacts" / "pipeline").as_uri(),
    )
experiment = mlflow.set_experiment(experiment_name)
```

1. `get_experiment_by_name(...)` looks up the named experiment. It returns an experiment record if found, or `None` if missing.
2. `create_experiment(...)` creates that grouping and returns its ID. `artifact_location` specifies where its artifact files belong. `as_uri()` converts the absolute folder path into a file address MLflow understands. The check prevents creating the same named experiment twice.
3. `set_experiment(...)` selects the experiment for subsequent logging in this process. It returns an experiment record; `experiment.experiment_id` is its identifier. It can also create a missing experiment, but we create it explicitly first to choose the artifact folder.

An **experiment** groups related attempts; a **run** represents one attempt. This notebook prepares the grouping. The next two notebooks each start one run inside it.

API reference: [MLflow connection and experiment functions](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html), [client experiment methods](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html).

## What to observe

Airflow's load_and_split Logs show the counts and handoff folder. MLflow shows the experiment; the following two tasks create its training runs.

Code excerpts and screenshot: [experiment guide](../06-mlflow-workflow.md#1-connect-to-mlflow-and-choose-an-experiment).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](07-main-dag.md) | [Next](09-train-logistic.md)
