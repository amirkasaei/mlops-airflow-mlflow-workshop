# Parallel branches

[Walkthrough index](../09-code-walkthrough.md) | [Previous](03-retry.md) | [Next](05-parameters.md)

**Source:** [parallel.py](../../dags/demos/parallel.py).

Understand independent jobs and the task that joins them. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Build a fork and join

```python
start = prepare()
jobs = [job_a(), job_b()]
end = finish()
start >> jobs >> end
```

prepare makes both jobs eligible. job_a and job_b have no dependency on one another, so they can run independently. finish waits for both to succeed. The eight-second sleeps simulate work so their timing can overlap visibly.

## What to observe

Open [demo_04_parallel](http://localhost:8080/dags/demo_04_parallel). Use Graph for the fork/join and Gantt for actual overlap. The graph permits parallel work; available executor slots determine whether it overlaps in a particular run.

Screenshot and UI steps: [parallel demo](../04-airflow-demo.md#4-parallel-work).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](03-retry.md) | [Next](05-parameters.md)
