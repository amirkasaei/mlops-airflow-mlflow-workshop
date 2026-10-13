# Explain model registration and tracing

Use this guide after comparing the models. All excerpts come from [05_register_candidate.ipynb](../notebooks/project/05_register_candidate.ipynb), which Airflow runs as **register_candidate**. The full notebook remains the runnable source.

## 1. Register the already trained winner

**Purpose:** give the saved winning model a numbered registry version.

After reading winner.json and checking its execution ID:

```python
model_version = mlflow.register_model(winner["model_uri"], registered_model_name)
print("Registered model:", model_version.name)
print("Version:", model_version.version)
```

`winner["model_uri"]` points to the model already saved by its training notebook. `registered_model_name` is **iris-pipeline-classifier**. `register_model` creates a version under that name and keeps its source run identifiable. No retraining happens here.

## 2. Assign the candidate alias

**Purpose:** provide a stable name for the selected version.

```python
client.set_registered_model_alias(
    name=registered_model_name, alias="candidate", version=model_version.version
)
candidate = client.get_model_version_by_alias(registered_model_name, "candidate")
print("Candidate version:", candidate.version)
```

`set_registered_model_alias` points **candidate** to the new version. `get_model_version_by_alias` reads that mapping back. Future runs can move the alias while retaining old numbered versions. Assigning an alias does not deploy a model.

**In MLflow:** select **Model registry > iris-pipeline-classifier**. Find candidate in the Aliases column and open its version to inspect the source model/run. The screenshot shows the existing workflow's selected version; your version number increases on later registrations.

![Registry versions and the candidate alias from the completed pipeline](images/mlflow-model-alias.png)

## 3. Trace loading and prediction during verification

**Purpose:** inspect what happened inside candidate verification, with timing and actual inputs/outputs.

A **trace** records the complete instrumented operation. A **span** is one timed step within it. This notebook creates:

```text
verify_candidate
|-- load_candidate
`-- predict_candidate
```

From the notebook's verification cell (after importing MLflow sklearn and accuracy_score):

```python
candidate_uri = f"models:/{registered_model_name}@candidate"
X_test = pd.DataFrame(split["X_test"], columns=split["feature_names"], dtype="float64")

# Each Airflow notebook has its own process: select the trace storage experiment.
mlflow.set_experiment(experiment_name)

# Link this verification trace to the winner without reopening its training run.
with mlflow.start_span(name="verify_candidate", run_id=winner["run_id"]) as verification:
    verification.set_inputs({"model_uri": candidate_uri, "version": str(candidate.version)})
    mlflow.update_current_trace(tags={"workflow_run_id": split["execution_id"]})

    with mlflow.start_span(name="load_candidate") as loading:
        loading.set_inputs({"model_uri": candidate_uri})
        candidate_model = mlflow.sklearn.load_model(candidate_uri)
        # Store model identity rather than serializing a Python model into the trace.
        loading.set_outputs({
            "model_type": winner["model_type"],
            "version": str(candidate.version),
            "source_run_id": candidate.run_id,
        })

    with mlflow.start_span(name="predict_candidate") as predicting:
        # Iris is public and tiny: record the actual rows and predictions.
        predicting.set_inputs({"rows": X_test.to_dict(orient="records")})
        candidate_predictions = candidate_model.predict(X_test)
        predicting.set_outputs({"predictions": candidate_predictions.tolist()})

    candidate_accuracy = accuracy_score(split["y_test"], candidate_predictions)
    assert candidate.run_id == winner["run_id"]
    assert candidate_accuracy == winner["accuracy"]
    verification.set_outputs({"accuracy": candidate_accuracy, "verified": True})

trace_id = verification.trace_id
# Finish exporting the trace before the notebook task exits.
mlflow.flush_trace_async_logging()
```

| Code | What it produces |
| --- | --- |
| `mlflow.set_experiment(experiment_name)` | Stores traces in the project experiment; each Airflow notebook uses a separate Python process |
| Root `start_span(..., run_id=winner["run_id"])` | One verify_candidate trace linked to the winning training run |
| `update_current_trace(tags=...)` | Workflow ID for finding the corresponding Airflow execution |
| Nested `start_span` blocks | Child spans for loading and prediction, with their durations |
| `set_inputs` / `set_outputs` | Inspectable model references, actual Iris rows, predictions, and verification result |
| Two assertions | Checks that the candidate is from the winning run and reproduces its accuracy |
| `flush_trace_async_logging()` | Completes pending trace writes before the notebook exits |

The loading span records model identity rather than serializing a Python model into the trace. The prediction span records the actual 30 public Iris input rows and their predictions. The root records verified accuracy. The trace adds no new training run.

**In MLflow:** open **Experiments > iris-pipeline-comparison > Traces**. Open the row whose input contains the candidate model URI. The viewer shows verify_candidate with its two children. Inspect status and duration, then select a span to view Inputs / Outputs and Attributes. Match the workflow tag or trace ID if there are several rows.

![Real verify_candidate trace with loading and prediction spans](images/mlflow-candidate-trace.png)

**What to explain from this screenshot:** verification succeeded; loading and prediction were timed separately; the root inputs identify candidate version 6 and its outputs show accuracy 0.9 and verified=true. Selecting predict_candidate reveals the input rows and predicted classes.

If loading, prediction, or verification raises an exception, the open affected spans record errors and the exception still reaches Airflow. We do not deliberately fail this main workflow; use the separate Airflow failure demo for that exercise.

## 4. Find the saved verification record

The notebook saves candidate.json under `outputs/<Airflow-run-folder>/`. It contains model name, version, alias, winning run ID, accuracy, and trace ID. The Airflow registration log prints the same trace ID. These generated files remain outside Git.

For the completed example, Random Forest is candidate version 6 with test accuracy 0.9. Versions, durations, and IDs change on subsequent runs. The screenshots are real local outputs, not mockups.

Training histories are under **Model metrics**; verification execution is under **Traces**; saved evaluation files are under **Artifacts**. See [the MLflow workflow guide](06-mlflow-workflow.md) for training and comparison, or [the main project walkthrough](08-main-project.md) for execution instructions.
