# Random Forest checkpoints

[Walkthrough index](../09-code-walkthrough.md) | [Previous](09-train-logistic.md) | [Next](11-compare-models.md)

**Source:** [03_train_random_forest.ipynb](../../notebooks/03_train_random_forest.ipynb).

Track a second approach using the same data and logging contract. Read the named blocks in the source; imports, comments, and closing brackets do not need a separate explanation here.

## Keep the same experiment and inputs

The connection/data cells follow the logistic notebook's pattern. This task creates its own random-forest run, while using the identical split and workflow ID.

## Add trees incrementally

RandomForestClassifier(warm_start=True) retains existing trees. The loop increases the total by ten until 100:

```python
for step in range(trees_per_checkpoint, total_trees + 1, trees_per_checkpoint):
    model.set_params(n_estimators=step)
    started = perf_counter()
    model.fit(X_train, y_train)
    training_seconds += perf_counter() - started
```

After each fit, the same accuracy/log-loss calculation and log_metrics call records this checkpoint. The Step axis is total trees, not epochs. Log loss evaluates predicted probabilities; it is not the criterion used to grow the trees.

## Save the forest

The final evaluation, confusion matrix, and model are logged just as for logistic regression. skops_trusted_types explicitly permits the tree type from our own fitted forest for serialization. forest_result.json passes its source run and model URI to comparison.

## Read the MLflow commands in this notebook

This notebook repeats the logging pattern from [logistic regression](09-train-logistic.md#start-a-run-and-record-its-settings). It creates a separate run in the same experiment so the two approaches can be compared.

| Call / argument | Meaning here |
| --- | --- |
| `mlflow.start_run(run_name="random-forest")` | Start the forest's training record, with this readable name in the Runs list. |
| `mlflow.log_params({...})` | Record the planned 100 trees, checkpoint interval, `warm_start`, depth, and shared split settings. |
| `mlflow.set_tag("workflow_run_id", ...)` | Attach the same execution label as the logistic run. |
| `mlflow.set_tag("progress_unit", "trees")` | Explain that steps count trees. |
| `mlflow.log_metrics(metrics, step=step, synchronous=True)` | Save the six calculated scores/timings after each fit and wait for the write. |

The parameter `n_estimators=100` records the final training plan. The metric steps `10, 20, ..., 100` record its progress. We do not repeatedly change that stored parameter: scikit-learn's `model.set_params(n_estimators=step)` changes the actual model during training.

`model.fit(...)` grows the forest; `log_metrics(...)` stores the results we calculate afterward. MLflow does not automatically discover these checkpoints. **Model metrics** shows ten points per metric because our loop makes ten logging calls.

## Understand the saved model arguments

`log_dict` saves final scores as `evaluation.json`; `log_figure` saves `confusion_matrix.png`. Both appear under the run's **Artifacts**. Their meanings are the same as in the [logistic model guide](09-train-logistic.md#save-files-and-the-fitted-model).

`mlflow.sklearn.log_model(...)` saves the fitted forest, its inferred input/output signature, and sample input rows. It returns `model_info`; `model_info.model_uri` is saved in `forest_result.json` alongside `run.info.run_id`.

The forest also passes `skops_trusted_types=["sklearn.tree._tree.Tree"]`. This records that the tree object type from our own trained forest is trusted when loading the skops-saved model. It is a model serialization setting, not a training parameter or accuracy metric.

The saved model is visible through **Logged models**. It becomes a registry version only if it wins the comparison and the registration notebook registers its URI.

API reference: [scikit-learn model logging arguments](https://mlflow.org/docs/latest/api_reference/python_api/mlflow.sklearn.html).

## What to observe

Open random-forest in MLflow and inspect its ten numeric checkpoints. Compare final scores with logistic regression; equal step numbers have different meanings across the two approaches.

Metric definitions and screenshots: [training-history guide](../06-mlflow-workflow.md#3-log-real-training-progress-and-view-curves).

[Walkthrough index](../09-code-walkthrough.md) | [Previous](09-train-logistic.md) | [Next](11-compare-models.md)
