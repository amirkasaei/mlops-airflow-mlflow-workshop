# mlops-airflow-mlflow-workshop

A minimal workshop about Airflow orchestration and MLflow experiment tracking and model lifecycle. We briefly recap the concepts, raise the problem of manual model runs, and implement a repeatable model-selection workflow.

## Project

Airflow runs five notebooks: load and split Iris, train Logistic Regression and Random Forest independently, compare accuracy, then register the winner and assign `candidate`. Training logs numeric accuracy/loss histories to MLflow: epochs for SGD-trained logistic regression and tree counts for Random Forest. The notebooks contain the ML code; the DAG defines execution and dependencies.

```text
dags/project/                  Main notebook workflow
dags/demos/                    Separate Airflow teaching examples
notebooks/project/             Five pipeline notebooks
notebooks/mlflow/              Optional MLflow reference notebook
docs/                          Instructions and real UI screenshots
requirements.txt               Notebook dependencies
requirements-airflow.txt       Airflow plus notebook dependencies
```

## Quick start

Open the folder in VS Code. Follow Python and Airflow setup, rehearse the demo examples, then follow [the main project walkthrough](docs/08-main-project.md). Start the pipeline from Airflow to monitor its tasks. A manual notebook execution logs to MLflow but does not create an Airflow run.

The main pipeline was validated end-to-end on Ubuntu WSL2. All five tasks succeeded, and the candidate reloaded with the winning accuracy. Linux/macOS setup instructions use the same workflow; those platforms have not been executed here.

## Guides

| Order | Guide |
| --- | --- |
| 1 | [Python and notebook environments](docs/01-python-setup.md) |
| 2 | [Airflow setup: Windows, Linux, macOS](docs/02-airflow-setup.md) |
| 3 | [Define DAGs and use the UI](docs/03-airflow-dag.md) |
| 4 | [Airflow demo exercises](docs/04-airflow-demo.md) |
| 5 | [Open MLflow locally](docs/05-mlflow-setup.md) |
| 6 | [Learn MLflow through the project](docs/06-mlflow-workflow.md) |
| 7 | [Model versions and candidate](docs/07-model-registry.md) |
| 8 | [Run the notebook pipeline](docs/08-main-project.md) |
