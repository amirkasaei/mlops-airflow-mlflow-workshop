# mlops-airflow-mlflow-workshop

A minimal workshop about Airflow orchestration and MLflow experiment tracking and model lifecycle. After a brief recap, we address a practical problem: manual model runs are hard to coordinate, compare, and trace.

## Current checkpoint

- **Airflow examples:** separate workflows demonstrate success, failure, retry, parallel tasks, parameters, and a 20-second schedule.
- **Main Airflow workflow:** `iris_model_selection` currently runs `load_data -> split_data` as Python tasks.
- **MLflow notebook:** the complete reference trains two classifiers on Iris, compares accuracy, registers the winner, and assigns `candidate`.

The main DAG does not yet execute notebooks or train models. Next, finalize the notebook-based design and its execution dependency before adding that integration.

## Structure

```text
dags/model_selection.py         Main Iris workflow
dags/demos/                     Separate Airflow teaching examples
notebooks/01_mlflow_basics.ipynb MLflow reference notebook
docs/                           Setup and walkthroughs
requirements.txt                Notebook dependencies
```

## Quick start

Open the project folder in VS Code. Begin with [Python setup](docs/01-python-setup.md), then follow [Airflow setup](docs/02-airflow-setup.md), then inspect the main workflow using [the DAG and UI guide](docs/03-airflow-dag.md). Use [the meeting walkthrough](docs/04-airflow-demo.md) to run the examples one at a time.

In Airflow, filter by `workshop-main` for the project or `workshop-demo` for the teaching examples. Pause the scheduling example when finished.

## Guides

| Order | Guide |
| --- | --- |
| 1 | [Python setup and environments](docs/01-python-setup.md) |
| 2 | [Airflow setup: Windows, Linux, and macOS](docs/02-airflow-setup.md) |
| 3 | [Define tasks, connect them, and use the UI](docs/03-airflow-dag.md) |
| 4 | [Meeting examples and expected results](docs/04-airflow-demo.md) |
| 5 | [MLflow storage and UI](docs/05-mlflow-setup.md) |
| 6 | [MLflow notebook walkthrough](docs/06-mlflow-workflow.md) |
| 7 | [Model Registry and candidate alias](docs/07-model-registry.md) |
