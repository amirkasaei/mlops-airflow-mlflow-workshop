# Define and run your first Airflow DAG

## Purpose

Understand how Python code becomes a workflow and a task in Airflow. The main project workflow, `iris_model_selection`, has two tasks: `load_data` followed by `split_data`. In the Airflow DAG list, filter by **workshop-main** to find it. Its code lives in `dags/model_selection.py`; separate demonstration files live under `dags/demos/`.

## 1. Understand the two names

A **DAG** describes the whole workflow: which tasks exist and which must wait for others. A **task** is one piece of work in that workflow.

In this project:

| Thing | Python name | Name in the Airflow UI |
| --- | --- | --- |
| Workflow | `iris_model_selection` | `iris_model_selection` |
| First task | `load_data` | `load_data` |
| Second task | `split_data` | `split_data` |

The UI name of the workflow comes from `dag_id`. The task name comes from its function name.

## 2. Find the code file

Airflow reads Python files from the configured `dags/` folder. In VS Code, open [dags/model_selection.py](../dags/model_selection.py).

This file already exists; you do not need to create it again. When creating a DAG from scratch, create a `.py` file in this folder and write the workflow definition there. The notebook is a separate reference and is not executed by this DAG.

## 3. Read the complete working definition

This is the code already in our file. Read it in small parts; the explanations below identify what each part does.

```python
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
```

## 4. What defines the DAG?

`from airflow.sdk import dag, task` imports Airflow's tools for defining workflows and tasks.

`@dag(...)` sits directly above `def iris_model_selection():`. The `@` syntax is called a decorator: it gives this Python function Airflow's workflow behavior.

The settings mean:

- `dag_id="iris_model_selection"`: the workflow name shown in the UI.
- `schedule=None`: we start runs manually.
- `start_date=...`: the starting point used for scheduling. It does not immediately run the workflow.
- `catchup=False`: do not create runs for past schedule dates.

The indented code inside `iris_model_selection()` describes the tasks belonging to this workflow.

## 5. What defines the task?

`@task` sits directly above `def load_data():`. It gives this function Airflow's task behavior. Airflow can execute it separately and record its status and logs.

The function body describes the work: import the dataset loader, load Iris, print its size, and return the data. `X` contains the measurements and `y` contains the flower class labels. Lists make this tiny output easy for Airflow to save and pass to another task later.

## 6. How do we connect tasks?

The two lines inside the workflow connect our tasks:

```python
data = load_data()
split_data(data)
```

While Airflow reads the file, `data` is a reference to the first task's future output. Passing it into `split_data` tells Airflow that the second task needs that output and must wait for the first to succeed.

During a run, Airflow executes `load_data`, saves its returned dictionary, and supplies that dictionary as the `data` argument when it executes `split_data`.

The resulting graph is:

```text
load_data -> split_data
```

The final `iris_model_selection()` call creates the whole DAG definition so Airflow can discover it. These definition calls do not execute the task bodies immediately.

### What does split_data do?

Its `train_test_split` call separates the 150 rows into 120 training rows and 30 test rows. Training rows will teach the models; test rows will measure their predictions later.

- `test_size=0.2`: reserve 20% for testing.
- `random_state=42`: repeat the same split on each execution.
- `stratify=data["y"]`: keep the flower classes balanced.

The returned dictionary contains `X_train`, `X_test`, `y_train`, and `y_test`, plus the feature and class names. Both future training tasks will receive the same split.

## 7. When does the work actually run?

Saving the file lets Airflow discover the definition. Clicking **Trigger DAG** creates a run of that workflow. Airflow executes `load_data()` first. After it succeeds, Airflow passes its output into `split_data()` and executes that task.

During execution:

- Normal completion becomes **Success**.
- An unhandled Python exception becomes **Failed**.
- `print(...)` messages appear in task logs.
- The returned dictionary is saved as a small task output, called an XCom.

Defining the workflow and executing a run are separate moments.

## Dependency setup

The task executes in the Airflow environment from [Airflow setup](02-airflow-setup.md). Use Ubuntu WSL on Windows, a Linux terminal on Linux, or Terminal on macOS. If the task dependency has not been installed, run:

```sh
source ~/mlops-airflow-workshop/mlops-workshop-env/bin/activate
```

```sh
python -m pip install "apache-airflow==3.3.2" "scikit-learn==1.9.1"
```

## First visit to the UI: inspect the existing workflow

1. With Airflow running, open [http://localhost:8080](http://localhost:8080).
2. Log in using your local Airflow credentials. See [setup](02-airflow-setup.md) if you need to retrieve them.
3. Select **Dags** in the main navigation to see the available workflows.
4. Find and open **iris_model_selection**. This name matches `dag_id` in the Python file.
5. Open **Code** to see the Python definition Airflow has read.
6. Open **Graph** to see the workflow as task boxes. Our current workflow has two connected boxes: **load_data** and **split_data**.

The Code view shows the definition; the Graph view shows its structure. Merely opening these views does not execute tasks. Pause here before triggering a new run.

Later, **Runs** shows execution history. Selecting a run and then its task lets you inspect the task status and logs for that execution.

Reference: [Airflow UI overview](https://airflow.apache.org/docs/apache-airflow/3.3.2/ui.html).

## UI map: what the main views mean

A workflow definition is the plan. A **DAG run** is one execution of that plan. A **task instance** is one task inside a particular run. Always select the run you want to inspect; older runs keep their own results.

| UI view | What it shows | Use it to |
| --- | --- | --- |
| Home | Overall Airflow activity and component health | Check the system overview |
| Dags | Available workflow definitions | Find `iris_model_selection` and open it |
| Graph | Task boxes and dependency arrows | See why `split_data` waits for `load_data`; select a run to see its states |
| Grid | Tasks against runs, with status cells | Compare successful and failed executions |
| Runs | The history of workflow executions | Open the specific run you just triggered |
| Code | The Python definition Airflow read | Connect task boxes to their functions |
| Tasks | Task definitions and summary information | Review the jobs in the workflow |
| Details | Workflow or run settings and metadata | Inspect IDs and configuration |
| Logs, after selecting a task in a run | Messages and Python errors from that execution | Find what the task did or why it failed |

Intentional failure, retry, and parameter demonstrations now have their own named DAGs. The main `iris_model_selection` workflow loads and splits data normally. See the [meeting examples](04-airflow-demo.md) for the demonstration sequence.

Other administration pages can wait until a later lesson. For this checkpoint, use Graph, Runs, Grid, Code, and task Logs.

## Run the main workflow yourself

1. Keep Airflow running as described in [Airflow setup](02-airflow-setup.md).
2. Open [http://localhost:8080](http://localhost:8080) and log in.
3. Open `iris_model_selection` from the DAG list.
4. Unpause it if needed, then select **Trigger DAG**. Confirm the trigger if a form opens.
5. Open the new run. Both tasks should finish with **Success**.
6. Select `split_data` and open **Logs** to see the split sizes.

## Expected result

The graph shows `load_data -> split_data`. Their respective logs contain:

```text
Loaded Iris: 150 rows, 4 features.
Split Iris: 120 training rows, 30 test rows.
```

## Important notes

The workflow is defined in the Python file; the browser controls and displays its runs. Do not use VS Code's ordinary **Run Python File** button to execute these Airflow tasks. Stop at this two-task workflow before adding model training.
