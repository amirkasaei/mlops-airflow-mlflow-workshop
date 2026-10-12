# MLflow workflow

## Purpose

Learn how MLflow records training attempts and helps select a model.

## What this covers

The code is in `notebooks/01_mlflow_basics.ipynb`. It loads Iris, trains Logistic Regression and Random Forest, records both runs, compares accuracy, and registers the winner.

Use this notebook as a reference while implementing the corresponding Airflow tasks. The workshop starts with the DAG and introduces these MLflow operations as each task is built.

## How to proceed

1. Complete [Python setup](03-python-setup.md) and [MLflow setup](04-mlflow-setup.md).
2. Open the notebook and select the `mlops-workshop-env` kernel.
3. Run the imports cell, then **Find the project folder** and **Configure tracking**, using Shift+Enter.
4. Pause and understand where MLflow stores its records before continuing.
5. Continue with **Select the experiment**, then one section at a time: run, parameters, metrics, logged model, second run, comparison, and selection.
6. Read [Model Registry](06-model-registry.md) when you reach registration.

Use the actual notebook cells for code. No additional terminal commands are needed here. During the guided walkthrough, wait until the current section is understood before running the next section.

## Expected result

The experiment cell selects `iris-model-comparison`. Later training cells add runs to it. The comparison uses only the two runs created in the current execution.

## Important notes

Both models use the same data split. Higher accuracy wins; a tie favors Logistic Regression. Earlier runs remain visible, and full notebook reruns add new records. This small dataset keeps attention on MLflow rather than ML complexity.
