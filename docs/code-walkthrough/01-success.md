# Sequential success

[Walkthrough index](../09-code-walkthrough.md) | [Next](02-failure.md)

**Source:** [success.py](../../dags/demos/success.py).

Define a DAG, create two tasks, and put them in order. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Workflow and tasks

`@dag` makes success_demo a workflow factory. Its settings name the DAG, require manual triggering, and start newly discovered demos paused. The bottom success_demo() call creates the definition when Airflow imports the file; it does not execute the task bodies.

`@task(retries=0)` makes each inner function an Airflow job with no automatic retries. The print calls appear in task Logs. The three-second sleeps simulate work so Running is visible.

## Dependencies

```python
first_task() >> second_task()
```

During graph construction these calls create task nodes. The arrow requires first_task to succeed before second_task becomes eligible. During a run, Airflow executes their function bodies.

## What to observe

Open [demo_01_success](http://localhost:8080/dags/demo_01_success). Inspect Code and Graph. In a selected run, both tasks should succeed in order; their Logs contain the printed messages.

**Remember:** defining a task and executing a task are different events. See [the DAG/UI guide](../03-airflow-dag.md) for the full example and screenshot.

[Walkthrough index](../09-code-walkthrough.md) | [Next](02-failure.md)
