# Compare final results and select

[Walkthrough index](../09-code-walkthrough.md) | [Previous](10-train-forest.md) | [Next](12-register-candidate.md)

**Source:** [04_compare_models.ipynb](../../notebooks/04_compare_models.ipynb).

Choose a winner from the current execution without retraining. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Read current model references

Load split.json and both result files. Their execution IDs must match, preventing a fresh run from competing with stale results. get_run reads each MLflow record; both must have FINISHED status.

copy() starts each comparison row from its model references. update() adds stored metrics. The resulting DataFrame displays two rows. MLflow's metric dictionary contains latest checkpoint values, so selection uses final scores rather than the best earlier checkpoint.

## Select and save

```python
run_filter = (
    f"attributes.run_id IN ('{logistic_result['run_id']}', "
    f"'{forest_result['run_id']}') AND attributes.status = 'FINISHED'"
)
assert logistic_run.info.experiment_id == forest_run.info.experiment_id
ranked_runs = client.search_runs(
    experiment_ids=[logistic_run.info.experiment_id],
    filter_string=run_filter,
    order_by=["metrics.test_accuracy DESC", "params.model_type ASC"],
    max_results=1,
)
assert ranked_runs, "No completed training runs matched this execution."
best_run = ranked_runs[0]
winner = comparison.loc[
    comparison["run_id"] == best_run.info.run_id
].iloc[0].to_dict()
(run_path / "winner.json").write_text(json.dumps(winner, indent=2), encoding="utf-8")
print("Winner:", winner["model_type"])
print("Accuracy:", winner["accuracy"])
print("Source run:", winner["run_id"])
```

MLflow's `client.search_runs` ranks the eligible runs by highest final `test_accuracy` and returns one result. The filter admits only this execution's two completed training run IDs, so an older or unrelated run cannot win. Sorting `params.model_type` ascending breaks ties in favor of `LogisticRegressionSGD`. Pandas retrieves the selected handoff row without ranking it. `accuracy` is an identical compatibility score used during verification. `winner.json` retains the model URI, source run, and execution identity for registration.

## Understand `client.get_run`

```python
logistic_run = client.get_run(logistic_result["run_id"])
forest_run = client.get_run(forest_result["run_id"])
```

`run_id` identifies an existing training attempt, not its display name. `get_run` reads that attempt from our configured MLflow store and returns a `Run` object. It does not train, create another run, or load the saved predictor.

| Field on the returned object | What it contains | How we use it |
| --- | --- | --- |
| `run.info.status` | The run's lifecycle status, such as `FINISHED` or `FAILED`. | Require both training attempts to have finished successfully. |
| `run.info.run_id` | Its unique identifier. | Link the result back to the original training record. |
| `run.data.params` | Stored training settings, represented as strings. | Available for inspection; selection here uses metrics. |
| `run.data.metrics` | A dictionary of latest numeric metric values. | Add final accuracy, loss, and time to the comparison table. |
| `run.data.tags` | Labels, including our workflow identity. | Inspect which execution produced the attempt. |

In this project, steps increase throughout each run, so the latest metric values are the final checkpoint scores. `run.data.metrics` is not the full training history. The earlier checkpoints remain in MLflow and are visible in **Model metrics**.

The JSON result files supply the exact run IDs from this execution. We read those two IDs rather than searching by run name, because many executions can share the names `logistic-regression` and `random-forest`.

MLflow supplies built-in comparison and ranking tools. Here we call its ranking API with our metric, eligible run IDs, and tie-break rule. Logging models alone does not automatically select, register, or promote a candidate. This notebook reads and ranks MLflow records and writes `winner.json`; it creates no additional training run. The next notebook explicitly registers the winner and assigns its alias.

API reference: [MlflowClient.get_run](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html#mlflow.client.MlflowClient.get_run).

## What to observe

In the experiment's Runs list, select two rows with the same workflow_run_id and click Compare. Inspect final test accuracy, losses, and duration. Airflow compare_models Logs show the winner; the full table is in its executed notebook.

Code and screenshot: [comparison guide](../06-mlflow-workflow.md#6-compare-the-runs-and-select-the-winner).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](10-train-forest.md) | [Next](12-register-candidate.md)
