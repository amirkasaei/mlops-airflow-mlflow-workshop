# First DAG task: load data

## Purpose

Create the first real step of the workshop pipeline and see it as a task in Airflow. For this checkpoint, the DAG contains only `load_data`.

## How the DAG is made

Open [dags/model_selection.py](../dags/model_selection.py) in VS Code. The code has these six parts:

1. Import `dag` and `task` from `airflow.sdk`.
2. Put `@dag` above `model_selection()` to define the workflow. Its UI name is `iris_model_selection`.
3. Set `schedule=None` for manual triggering and `catchup=False` to skip historical scheduled runs. The fixed UTC start date gives the workflow a clear starting point.
4. Put `@task` above `load_data()` to create a task with its own status and logs. It loads the built-in Iris dataset and prints its size.
5. Call `load_data()` inside the workflow to add its task node. Its return value contains feature measurements (`X`), class labels (`y`), and their names as simple lists.
6. Call `model_selection()` at the bottom of the file so Airflow can discover the DAG.

These calls define the workflow. Airflow executes the task body when you trigger a run. One DAG file can contain several separate task functions; each will appear as a separate box in the UI.

## Dependency setup

The task runs in the Airflow environment configured in [Airflow setup](01-airflow-setup.md). Use Ubuntu WSL on Windows, a Linux terminal on Linux, or Terminal on macOS. Install the task dependency with the same commands on all three:

```sh
source ~/mlops-airflow-workshop/mlops-workshop-env/bin/activate
```

```sh
python -m pip install "apache-airflow==3.3.2" "scikit-learn==1.9.1"
```

Airflow stays pinned while the task dependency is added.

## Run it in the UI

1. Keep Airflow running as described in [Airflow setup](01-airflow-setup.md).
2. Open [http://localhost:8080](http://localhost:8080) and log in.
3. Wait for `iris_model_selection` to appear in the DAG list, then open it.
4. Unpause the DAG if it is paused and select **Trigger DAG**.
5. Open the resulting run and select its `load_data` task.
6. Open the task's logs.

## Expected result

The task succeeds and its log contains:

```text
Loaded Iris: 150 rows, 4 features.
```

The graph contains one task box: `load_data`. Its small returned dictionary is stored by Airflow as a task output, called an XCom. We will use it for the next task later.

## Important notes

Save the file inside `dags/`, which Airflow is configured to scan. Discovery may take a short time. Use the Airflow UI to execute the DAG. Stop here before adding `split_data`; no training or MLflow logging happens yet.
