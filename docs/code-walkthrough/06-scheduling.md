# Scheduled workflow runs

[Walkthrough index](../09-code-walkthrough.md) | [Previous](05-parameters.md) | [Next](07-main-dag.md)

**Source:** [scheduled.py](../../dags/demos/scheduled.py).

See how the scheduler creates executions without a manual trigger. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Scheduling settings

```python
schedule=timedelta(seconds=20)
```

The schedule makes new runs eligible periodically. catchup=False avoids creating all past intervals from start_date, max_active_runs=1 allows one active run, and is_paused_upon_creation=True lets you choose when to enable the demo.

report_time simply prints the current UTC time, so its log reveals when execution occurred.

## What to observe

Open [demo_06_scheduled](http://localhost:8080/dags/demo_06_scheduled). Unpause it, observe runs whose type is scheduled without clicking Trigger, then pause it again. Scheduler overhead affects actual start times; pausing does not undo an already active run.

Screenshot and UI steps: [scheduling demo](../04-airflow-demo.md#6-scheduling).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](05-parameters.md) | [Next](07-main-dag.md)
