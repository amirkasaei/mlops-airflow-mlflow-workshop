# Logistic regression with training histories

[Walkthrough index](../09-code-walkthrough.md) | [Previous](08-load-and-split.md) | [Next](10-train-forest.md)

**Source:** [02_train_logistic.ipynb](../../notebooks/02_train_logistic.ipynb).

Connect incremental training to numeric MLflow curves. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Prepare the model

Read the shared split and select the experiment. Fit StandardScaler only on training rows. SGDClassifier(loss="log_loss") trains logistic regression incrementally; the saved pipeline combines classifier and scaler so reloading handles the original input columns.

## Train one epoch at a time

```python
for step in range(1, epochs + 1):
    # Train one epoch.
    # partial_fit updates the existing classifier using one pass through the
    # training rows.
    started = perf_counter()
    classifier.partial_fit(X_train_scaled, y_train, classes=[0, 1, 2])
    training_seconds += perf_counter() - started
```

The enclosing start_run context keeps all 30 epochs in one training attempt. Parameters record its settings; workflow_run_id links it to Airflow. After each update, the notebook calculates training/test predictions, probabilities, accuracy, and log loss.

```python
mlflow.log_metrics(metrics, step=step, synchronous=True)
```

Repeated names with new steps create real numeric histories. The print line also exposes progress in Airflow Logs. training_seconds accumulates fitting time only.

## Save the result

Inside the same run, evaluation.json summarizes final scores, confusion_matrix.png visualizes test mistakes, and log_model saves the fitted pipeline, signature, and example inputs. logistic_result.json passes its run ID/model URI to comparison. Model preparation, final printouts, and handoff have separate cells for readability.

## Start a run and record its settings

The scikit-learn `partial_fit` call trains the classifier. Our MLflow calls explicitly record the settings and results we choose; MLflow does not calculate the accuracy or loss in this loop.

```python
with mlflow.start_run(run_name="logistic-regression") as run:
    # The notebook's parameter logging, training loop, and model logging go here.
    ...
```

`run_name` is a readable label shown in the Runs list. `run` is the returned active-run object; `run.info.run_id` is the unique ID used later to retrieve this attempt. The indented code belongs to this run. Leaving the block successfully marks it `FINISHED`; an exception escaping the block marks it `FAILED`. One run contains all 30 epochs, so we get one history per metric.

| Command in the notebook | What it records | Where to inspect it |
| --- | --- | --- |
| `mlflow.log_params({...})` | A dictionary of fixed settings, including `epochs`, `eta0`, the scaler, and split settings. | Run Overview: Parameters. |
| `mlflow.set_tag("workflow_run_id", split["execution_id"])` | A label connecting this attempt to its matching forest run and Airflow execution. | Run Overview: Tags; use it when selecting runs to compare. |
| `mlflow.set_tag("progress_unit", "epoch")` | A label explaining what the metric step means. | Run Overview: Tags. |

Parameters describe how we configured training; metrics are measured numeric results; tags are descriptive labels. `log_params` saves the settings already used by scikit-learn. It does not configure the classifier, and a parameter's value cannot be changed within the same run.

## Understand each metric checkpoint

```python
mlflow.log_metrics(metrics, step=step, synchronous=True)
```

`metrics` is our dictionary of numeric results. `step` identifies the epoch, from 1 through 30. `synchronous=True` waits for this write to complete before proceeding. Calling it repeatedly with the same metric names and new steps stores a history, rather than just printing a score.

| Key in `metrics` | Meaning | Interpretation |
| --- | --- | --- |
| `train_accuracy` / `test_accuracy` | Fraction of correct predictions on training / held-out rows. | Higher is better; compare models using test accuracy. |
| `train_log_loss` / `test_log_loss` | Error based on predicted class probabilities. | Lower is better; confident wrong predictions are penalized. |
| `training_seconds` | Accumulated time spent fitting through this epoch. | Shows training duration, excluding logging and plotting. |
| `accuracy` | The same value as `test_accuracy`. | Retained for the later candidate verification check. |

Run Overview shows the latest values. **Model metrics** shows the numeric histories. The Airflow Logs show our separate `print(...)` output; printing alone would not create MLflow curves.

## Save files and the fitted model

| Call | Arguments and result |
| --- | --- |
| `mlflow.log_dict({...}, "evaluation.json")` | Serialize our final evaluation dictionary as a JSON artifact with that filename. |
| `mlflow.log_figure(plot.figure_, "confusion_matrix.png")` | Save the matplotlib figure as an image artifact with that filename. |
| `mlflow.sklearn.log_model(...)` | Save the fitted scikit-learn pipeline and its model metadata; return a `ModelInfo` object. |

The first two files appear under run **Artifacts**. Their filenames are names inside MLflow's artifact storage. In contrast, `logistic_result.json` is written by Python to our local execution folder for the next Airflow task; it is not uploaded by these calls.

```python
model_info = mlflow.sklearn.log_model(
    sk_model=model,
    name="model",
    signature=infer_signature(X_test, predictions),
    input_example=X_train.head(3),
)
```

- `sk_model`: the already fitted pipeline, including its scaler. Saving does not train again.
- `name`: the logged model's label. This is separate from the registered model name used later.
- `signature`: the expected input and output structure. `infer_signature` derives column names/types and prediction types from the supplied examples; it does not fit or score the model.
- `input_example`: three sample input rows saved to illustrate the model's expected input.

`model_info.model_uri` is the address of the saved model. We pass it to registration later. `run.info.run_id` identifies the training record; these two values serve different purposes. In MLflow 3, open the run's **Logged models** entry to inspect the model files, signature, and example. Logging a model saves it; registration later creates a named, numbered version.

API reference: [MLflow run and logging functions](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.html), [scikit-learn model logging](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html).

## What to observe

In MLflow open logistic-regression: Overview for settings/tags, Model metrics for epoch curves, and Artifacts for evaluation files. These curves are not image artifacts.

Code and screenshots: [training-history guide](../06-mlflow-workflow.md#3-log-real-training-progress-and-view-curves).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](08-load-and-split.md) | [Next](10-train-forest.md)
