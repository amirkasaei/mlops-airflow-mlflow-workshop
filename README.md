# mlops-airflow-mlflow-workshop

A minimal workshop about **Airflow orchestration** and **MLflow experiment tracking and model lifecycle**. After a brief recap, we raise the problem: manual model runs are hard to coordinate, compare, and trace.

## Workshop flow

Introduce the Airflow DAG and its task order. Implement each task, logging training results to MLflow. Compare accuracy, register the winner, and assign `candidate`. Then run the complete DAG and inspect its results in MLflow.

The ML stays simple: Iris, Logistic Regression, and Random Forest. The existing notebook provides a reference for the training and MLflow operations.

## Structure

```text
requirements.txt   MLflow notebook dependencies
notebooks/         Reference notebook
dags/              Airflow workshop DAG
docs/              Setup and workshop guides
```

## Quick start

Open this folder in VS Code. Start with [Airflow setup for Windows, Linux, or macOS](docs/01-airflow-setup.md). Then follow [the first DAG task](docs/02-airflow-dag.md). Currently, only `load_data` is implemented; later steps will add splitting, training, comparison, and registration.

| Order | Guide |
| --- | --- |
| 1 | [Airflow setup](docs/01-airflow-setup.md) |
| 2 | [First DAG task](docs/02-airflow-dag.md) |
| 3 | [Notebook Python setup](docs/03-python-setup.md) |
| 4 | [MLflow setup](docs/04-mlflow-setup.md) |
| 5 | [MLflow workflow reference](docs/05-mlflow-workflow.md) |
| 6 | [Model Registry](docs/06-model-registry.md) |

Current checkpoint: `load_data` has run successfully in Airflow. The next task to add is `split_data`. The complete MLflow notebook remains a reference; its training and registration steps have not yet been integrated into the DAG.
