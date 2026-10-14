# Orchestrating the five notebooks

[Walkthrough index](../09-code-walkthrough.md) | [Previous](06-scheduling.md) | [Next](08-load-and-split.md)

**Source:** [iris_model_selection.py](../../dags/project/iris_model_selection.py).

Apply the demo concepts to real model training and lifecycle steps. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Locate and define the workflow

PROJECT_ROOT finds the repository from the DAG's own path. The DAG is manually triggered, has one active run at a time, and is tagged workshop-main. No training happens when Airflow imports this definition.

## Execute one notebook per task

run_notebook gets the Airflow run ID and creates outputs/<run-folder>/. It chooses a source notebook and a separate executed copy, then calls:

```python
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
```

Papermill injects paths and workflow identity into the cell tagged parameters. The registered kernel supplies Python dependencies. log_output forwards progress to task logs. Each notebook has its own session, so JSON handoffs share data/references instead of Python variables.

## Create tasks and dependencies

The five override(task_id=...) calls reuse the runner with different visible names and notebook filenames.

```python
load_and_split >> [train_logistic, train_random_forest]
[train_logistic, train_random_forest] >> compare_models >> register_candidate
```

Both models read one split. Comparison waits for both; registration waits for comparison. A notebook exception propagates and fails its task. The returned notebook path can be stored as XCom, but this pipeline's next tasks use the JSON files instead.

## What to observe

Open [iris_model_selection](http://localhost:8080/dags/iris_model_selection), match Code to Graph, then inspect a selected run and task Logs.

Setup, screenshot, and execution steps: [main project guide](../08-main-project.md).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](06-scheduling.md) | [Next](08-load-and-split.md)
