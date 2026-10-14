# Trigger parameters and task output

[Walkthrough index](../09-code-walkthrough.md) | [Previous](04-parallel.md) | [Next](06-scheduling.md)

**Source:** [parameters.py](../../dags/demos/parameters.py).

Pass a run input into a task, then pass its result to another task. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Trigger-form input

The DAG's params dictionary defines student_name with Param. Its default is Student, its type is string, and minLength=1 prevents an empty value. This becomes a field in Airflow's Trigger form.

## Read the input at runtime

```python
context = get_current_context()
name = context["params"]["student_name"]
return f"Hello, {name}!"
```

The task reads the value for this execution and returns the greeting. The f-string inserts name into the text.

## Connect the returned result

```python
message = make_message()
display_message(message)
```

While building the DAG, message represents a future result, not the actual greeting. At execution time Airflow saves the returned string as XCom and supplies it to display_message. This also creates their dependency.

## What to observe

Open [demo_05_parameters](http://localhost:8080/dags/demo_05_parameters), enter a name in Trigger, then inspect display_message Logs. This run parameter is different from a model setting logged with MLflow log_params.

Screenshot and UI steps: [parameters demo](../04-airflow-demo.md#5-parameters-and-task-output).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](04-parallel.md) | [Next](06-scheduling.md)
