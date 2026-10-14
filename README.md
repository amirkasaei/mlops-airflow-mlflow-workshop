# mlops-airflow-mlflow-workshop

A minimal MLOps workshop using Airflow for orchestration and MLflow for experiment tracking and model lifecycle management. The project uses Iris and two simple model approaches so the focus stays on workflow execution, traceability, and model selection.

## What the project does

Airflow executes five notebooks:

```text
load_and_split
      |
      +--> train_logistic ------+
      |                         |
      +--> train_random_forest -+
                                |
                          compare_models
                                |
                        register_candidate
```

Logistic regression is trained with SGD for 30 epochs. Random Forest is trained in ten checkpoints, adding trees up to a total of 100. Both log training/test accuracy and log loss as numeric MLflow histories, plus duration, evaluation files, a confusion matrix, and a reloadable model.

The comparison selects the highest final test accuracy. The winning model is registered as `iris-pipeline-classifier`, assigned the `candidate` alias, and reloaded for verification. MLflow traces its loading and prediction steps. The experiment is named `iris-pipeline-comparison`.

There is no deployment, Kubernetes, Celery, advanced ETL, or complex feature engineering.

## Repository structure

```text
mlops-airflow-mlflow-workshop/
|-- .gitignore
|-- README.md
|-- requirements.txt
|-- requirements-airflow.txt
|-- notebooks/
|   |-- 01_load_and_split.ipynb
|   |-- 02_train_logistic.ipynb
|   |-- 03_train_random_forest.ipynb
|   |-- 04_compare_models.ipynb
|   `-- 05_register_candidate.ipynb
|-- dags/
|   |-- project/iris_model_selection.py
|   `-- demos/                       Six separate Airflow examples
`-- docs/
    |-- 01-python-setup.md ... 09-code-walkthrough.md
    |-- code-walkthrough/            One short explanation per code file
    |-- workshop-teaching.md         Presentation sequence for the workshop
    `-- images/                      Real Airflow and MLflow screenshots
```

| Files | Purpose |
| --- | --- |
| [Main DAG](dags/project/iris_model_selection.py) | Defines five notebook tasks and their dependencies; executes them through Papermill |
| [Project notebooks](notebooks/) | Contain the data, training, logging, selection, registration, and tracing code |
| [Demo DAGs](dags/demos/) | Demonstrate success, failure, retry, parallel work, parameters, and scheduling separately |
| [requirements.txt](requirements.txt) | Notebook dependencies |
| [requirements-airflow.txt](requirements-airflow.txt) | Airflow pin plus notebook dependencies |
| [Guides](docs/) | Setup instructions, code explanations, and UI screenshots |
| [.gitignore](.gitignore) | Excludes environments, generated state, caches, and local configuration |

## Getting started

1. Follow [Python setup](docs/01-python-setup.md) and [Airflow setup](docs/02-airflow-setup.md).
2. Complete [notebook execution environment setup](docs/08-main-project.md#prepare-the-execution-environment), including the registered `mlops-workshop-airflow` kernel.
3. Start Airflow from the project root and open [http://localhost:8080](http://localhost:8080).
4. Follow [MLflow setup](docs/05-mlflow-setup.md) and open [http://localhost:5000](http://localhost:5000).
5. Trigger `iris_model_selection` using [the main project instructions](docs/08-main-project.md#run-from-airflow). Inspect the newest task instances and corresponding MLflow records.

On Windows, run Airflow, these project notebooks, and the MLflow UI inside Ubuntu WSL2. On Linux/macOS, use the normal terminal. Use the same runtime platform for training and viewing model artifacts. A Windows-native virtual environment is separate from its WSL counterpart.

The local environment is named `mlops-workshop-env`. Activation commands for a project-local environment are:

**Windows PowerShell:**

```powershell
.\mlops-workshop-env\Scripts\Activate.ps1
```

**Linux/macOS:**

```sh
source mlops-workshop-env/bin/activate
```

The Airflow setup guide uses a separate environment outside the repository; activate that runtime with `source ~/mlops-airflow-workshop/mlops-workshop-env/bin/activate`. The setup guides explain environment creation and dependency installation. In VS Code, select the interpreter and notebook kernel separately; on Windows use a WSL window for the project notebooks.

Running notebook cells manually logs to MLflow when their logging code executes, but creates no Airflow task instance. Use Airflow to demonstrate the integrated workflow.

## Documentation

Use [workshop-teaching.md](docs/workshop-teaching.md) to present to students. It contains slide-style sections with code links, key explanations, screenshots, and prompts for switching to each live UI. Use [the code walkthrough index](docs/09-code-walkthrough.md) to choose a short per-file explanation for instructor preparation.

| Order | Guide |
| --- | --- |
| 1 | [Python and notebook environments](docs/01-python-setup.md) |
| 2 | [Airflow setup: Windows, Linux, macOS](docs/02-airflow-setup.md) |
| 3 | [Define DAGs and use the UI](docs/03-airflow-dag.md) |
| 4 | [Airflow demo exercises](docs/04-airflow-demo.md) |
| 5 | [Open MLflow locally](docs/05-mlflow-setup.md) |
| 6 | [MLflow code and UI results](docs/06-mlflow-workflow.md) |
| 7 | [Model versions, candidate, and tracing](docs/07-model-registry.md) |
| 8 | [Run the notebook pipeline](docs/08-main-project.md) |
| 9 | [Understand the implemented code](docs/09-code-walkthrough.md) |

## Local generated files

`outputs/<run-folder>/` contains executed notebook copies and JSON handoffs. `mlflow.db` stores experiment/registry/trace records; `mlartifacts/` stores saved model and evaluation files. Airflow's database and logs live under its configured AIRFLOW_HOME, separate from MLflow's database.

These files and the virtual environment are ignored by Git. Source notebooks stay free of saved outputs. Documentation screenshots are intentional repository files; they show real previous runs, so IDs, versions, timings, and results can differ on later executions.

## Validation

The integrated workflow has run successfully through Airflow on Ubuntu WSL2, including numeric training histories, winner registration, candidate reload, and verification tracing. Native Linux/macOS instructions have not been executed on separate machines. The guide includes separate deliberately failing Airflow examples; the main pipeline contains no simulated failure.
