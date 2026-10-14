# Retry after a temporary failure

[Walkthrough index](../09-code-walkthrough.md) | [Previous](02-failure.md) | [Next](04-parallel.md)

**Source:** [retry.py](../../dags/demos/retry.py).

Distinguish a task from its separate execution attempts. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Allow one retry

The task decorator is `@task(retries=1, retry_delay=timedelta(seconds=5))`.

One retry allows up to two attempts. Airflow waits until the five-second retry delay has passed before the next attempt becomes eligible; scheduling can add some delay.

## Fail only the first attempt

```python
context = get_current_context()
attempt = context["ti"].try_number
print(f"Attempt number: {attempt}")

if attempt == 1:
    raise ConnectionError("Simulated temporary problem: the first attempt fails.")
```

get_current_context provides this task instance's runtime information. try_number identifies the attempt. Attempt 1 raises the simulated error; attempt 2 skips that branch, succeeds, and allows finish to run. A fresh DAG run starts with a new first attempt.

## What to observe

Open [demo_03_retry](http://localhost:8080/dags/demo_03_retry). Inspect Up for retry and the separate log attempts, not just the final green state.

Screenshot and UI steps: [retry demo](../04-airflow-demo.md#3-retry).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](02-failure.md) | [Next](04-parallel.md)
