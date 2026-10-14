# Failure and blocked work

[Walkthrough index](../09-code-walkthrough.md) | [Previous](01-success.md) | [Next](03-retry.md)

**Source:** [failure.py](../../dags/demos/failure.py).

Understand how an exception affects dependent tasks. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## The deliberate failure

```python
raise ValueError("Intentional workshop failure: this task always fails.")
```

prepare returns normally, but fail_on_purpose raises an unhandled exception. With retries=0 it becomes Failed immediately. Merely printing an error or returning False would still be normal completion.

## Dependencies

```python
prepare() >> fail_on_purpose() >> finish()
```

finish uses the default rule requiring upstream success. Its body is never executed after the failure; its state becomes Upstream failed. That is different from a task body executing and raising its own exception.

## What to observe

Open [demo_02_failure](http://localhost:8080/dags/demo_02_failure). Show Failed on fail_on_purpose, Upstream failed on finish, and the ValueError in the failed task's Logs. This sample always fails intentionally.

Screenshot and UI steps: [failure demo](../04-airflow-demo.md#2-failure-and-blocked-work).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](01-success.md) | [Next](03-retry.md)
