# Code walkthrough index

Use these short guides for your own preparation. Each explains one file through its important code blocks, with a source link and a UI connection. Read the demos first, then the main DAG, then the notebooks. Use [workshop-teaching.md](workshop-teaching.md) for the student presentation.

## Airflow demos

| Order | Explanation | Source |
| --- | --- | --- |
| 1 | [Sequential success](code-walkthrough/01-success.md) | [success.py](../dags/demos/success.py) |
| 2 | [Failure and blocked work](code-walkthrough/02-failure.md) | [failure.py](../dags/demos/failure.py) |
| 3 | [Retry after a temporary failure](code-walkthrough/03-retry.md) | [retry.py](../dags/demos/retry.py) |
| 4 | [Parallel branches](code-walkthrough/04-parallel.md) | [parallel.py](../dags/demos/parallel.py) |
| 5 | [Trigger parameters and task output](code-walkthrough/05-parameters.md) | [parameters.py](../dags/demos/parameters.py) |
| 6 | [Scheduled workflow runs](code-walkthrough/06-scheduling.md) | [scheduled.py](../dags/demos/scheduled.py) |

## Main project

| Order | Explanation | Source |
| --- | --- | --- |
| 7 | [Orchestrating the five notebooks](code-walkthrough/07-main-dag.md) | [iris_model_selection.py](../dags/project/iris_model_selection.py) |
| 8 | [One shared dataset and experiment](code-walkthrough/08-load-and-split.md) | [01_load_and_split.ipynb](../notebooks/01_load_and_split.ipynb) |
| 9 | [Logistic regression with training histories](code-walkthrough/09-train-logistic.md) | [02_train_logistic.ipynb](../notebooks/02_train_logistic.ipynb) |
| 10 | [Random Forest checkpoints](code-walkthrough/10-train-forest.md) | [03_train_random_forest.ipynb](../notebooks/03_train_random_forest.ipynb) |
| 11 | [Compare final results and select](code-walkthrough/11-compare-models.md) | [04_compare_models.ipynb](../notebooks/04_compare_models.ipynb) |
| 12 | [Register, alias, and trace verification](code-walkthrough/12-register-candidate.md) | [05_register_candidate.ipynb](../notebooks/05_register_candidate.ipynb) |

## How to use a guide

Open the source beside its explanation. Read one block, explain its purpose in your own words, then inspect the corresponding UI result when useful. Previous/Next links keep the learning sequence clear. Running a demo is optional while studying the code.

The five notebook guides also explain the MLflow calls: their arguments, returned records or models, and the UI location of their results. Start with the connection and experiment commands in [One shared dataset and experiment](code-walkthrough/08-load-and-split.md#understand-the-connection-commands), then follow Next.

Start with [Sequential success](code-walkthrough/01-success.md).

## Other references

- [Airflow UI and DAG basics](03-airflow-dag.md)
- [Airflow demo screenshots](04-airflow-demo.md)
- [MLflow code and screenshots](06-mlflow-workflow.md)
- [Registry and tracing](07-model-registry.md)
- [Main project execution](08-main-project.md)
- [Repository overview](../README.md)

requirements.txt defines notebook dependencies; requirements-airflow.txt adds Airflow. The .gitignore keeps environments and generated records outside Git. The project source and teaching screenshots remain in the repository.
