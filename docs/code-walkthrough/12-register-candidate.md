# Register, alias, and trace verification

[Walkthrough index](../09-code-walkthrough.md) | [Previous](11-compare-models.md)

**Source:** [05_register_candidate.ipynb](../../notebooks/05_register_candidate.ipynb).

Make the selected saved model identifiable and verify its predictions. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Register the saved winner

Read winner.json and check its execution ID against the shared split. register_model uses its existing model URI and creates a numbered version under iris-pipeline-classifier. It does not train again.

## Assign and reload candidate

set_registered_model_alias points candidate at the new version; get_model_version_by_alias reads it back. Older numbered versions remain. models:/iris-pipeline-classifier@candidate loads the currently selected version, including its scaler when logistic regression wins.

## Trace the check

The notebook explicitly selects the experiment because each Airflow notebook has a separate Python process. It then records:

```text
verify_candidate
|-- load_candidate
`-- predict_candidate
```

The root links to the winning run and carries workflow identity. Child spans record model identity, actual Iris inputs/predictions, and timing. Assertions check the source run and reproduced accuracy. An escaping exception records an error and still fails the Airflow task.

Flush trace writes before leaving the notebook. candidate.json saves version, alias, run ID, accuracy, and trace ID together.

## Understand registration and the alias

```python
model_version = mlflow.register_model(winner["model_uri"], registered_model_name)
client.set_registered_model_alias(
    name=registered_model_name, alias="candidate", version=model_version.version
)
candidate = client.get_model_version_by_alias(registered_model_name, "candidate")
candidate_uri = f"models:/{registered_model_name}@candidate"
```

| Call | Inputs and result |
| --- | --- |
| `register_model(model_uri, name)` | Take the winner's already saved model address and add a version under `iris-pipeline-classifier`. Create the named registry entry if needed. Return a `ModelVersion` record. |
| `set_registered_model_alias(name=..., alias=..., version=...)` | Point `candidate` at the returned version number under that registered name. It updates the alias; it does not create another version. |
| `get_model_version_by_alias(name, alias)` | Resolve the alias and return its current `ModelVersion` record. We use `candidate.version` and `candidate.run_id` to check what was selected. |

Every registration creates a new numbered version. Moving `candidate` keeps older versions available. The alias is our workshop label for the selected model; it has no automatic approval or deployment behavior.

`winner["model_uri"]` addresses the model saved during training. `models:/iris-pipeline-classifier@candidate` addresses whichever registered version currently holds that alias. Keeping a stable alias lets loading code stay the same when the selected version changes.

Inside the verification block, `mlflow.sklearn.load_model(candidate_uri)` retrieves the saved model and returns a usable scikit-learn predictor. We then call its ordinary `predict(X_test)` method. Registration, alias assignment, and loading do not retrain it.

## Understand the tracing commands

A **trace** records one operation; a **span** records one timed part of it. Here the operation is candidate verification, with separate parts for loading and prediction. Training progress is already stored as metric histories.

```python
mlflow.set_experiment(experiment_name)
with mlflow.start_span(name="verify_candidate", run_id=winner["run_id"]) as verification:
    verification.set_inputs({"model_uri": candidate_uri, "version": str(candidate.version)})
    mlflow.update_current_trace(tags={"workflow_run_id": split["execution_id"]})
    # The notebook's nested load and prediction spans go here.
    ...
```

- `set_experiment`: select where this process stores the trace. A previous notebook's selection is not inherited.
- `start_span`: begin a timed block and return a span object. The outer span creates the trace; calls nested inside it create child spans. Leaving each `with` block ends its span.
- `name`: the label shown in the trace viewer. `run_id`: link the root operation to the existing winning training run without opening another training run. We also select the experiment explicitly to keep the trace destination clear in our notebook setup.
- `set_inputs({...})`: record what entered that span. The root gets model identity, the loading span gets its model URI, and the prediction span gets the actual test rows.
- `set_outputs({...})`: record what came out. The loading span records the resolved version/source; prediction records predicted labels; the root records accuracy and successful verification.
- `update_current_trace(tags={...})`: attach our workflow label to the whole trace so it can be related to this Airflow execution.

The `assert` statements are ordinary Python checks, not MLflow commands. They confirm the candidate comes from the selected run and reproduces its accuracy. An exception escaping a span records an error; escaping the notebook also causes Airflow to mark the task failed.

After the root block ends, `verification.trace_id` identifies the whole recorded operation. `mlflow.flush_trace_async_logging()` waits for pending trace logging to complete before the notebook process exits. It does not run verification again. We store the trace ID with the version and scores in `candidate.json`.

In **Model registry**, inspect versions and `candidate`. In the experiment's **Traces**, open `verify_candidate` to inspect the span tree, durations, recorded inputs/outputs, and status. See the [registry and trace screenshots](../07-model-registry.md).

API reference: [MLflow registration and tracing functions](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html), [client version and alias methods](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.client.html), [scikit-learn model loading](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html).

## What to observe

In Model registry, inspect candidate and its source run. In the experiment's Traces page, open verify_candidate and its children. Numeric training histories remain under Model metrics, not Traces.

Full tracing code and screenshots: [registry/tracing guide](../07-model-registry.md).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](11-compare-models.md)
