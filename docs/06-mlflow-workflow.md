# Learn MLflow through the main project

## Purpose

Learn tracking while training the two real project models. No separate MLflow lesson is required. Airflow coordinates the notebook tasks; MLflow records the model information inside them.

## What MLflow does in this project

1. Airflow starts a notebook task.
2. Scikit-learn trains the model with `model.fit(...)`.
3. Our notebook calculates results and sends them to MLflow with logging calls.
4. MLflow saves those records. Its UI lets you inspect and compare them.

An Airflow task is one workflow step. An MLflow run is one model-training record. Both model tasks can succeed even when their scores differ. Opening the MLflow UI does not train a model or automatically measure its performance.

## Where the learning code lives

| Notebook | What to learn |
| --- | --- |
| [01_load_and_split](../notebooks/project/01_load_and_split.ipynb) | Shared data split, tracking URI, and experiment |
| [02_train_logistic](../notebooks/project/02_train_logistic.ipynb) | Run, parameters, accuracy, tags, artifacts, and logged model |
| [03_train_random_forest](../notebooks/project/03_train_random_forest.ipynb) | A second approach in the same experiment |
| [04_compare_models](../notebooks/project/04_compare_models.ipynb) | Reading logged results and selecting the winner |
| [05_register_candidate](../notebooks/project/05_register_candidate.ipynb) | Model versions, alias, and reload verification |

Read one notebook section, explain its important lines, run the pipeline or relevant task, then inspect the corresponding UI page before continuing.

## 1. Tracking and experiment

The notebooks use the same root-level SQLite database. `iris-pipeline-comparison` groups their training attempts. The data notebook prepares this experiment before either training task starts; it does not create a training run.

## 2. Runs, parameters, metrics, and tags

The Logistic Regression notebook opens one run with:

```python
with mlflow.start_run(run_name="logistic-regression") as run:
```

Inside that block, `log_params` records settings. The notebook calculates named metrics and sends the dictionary to MLflow:

```python
mlflow.log_metrics(metrics, step=step, synchronous=True)
```

`workflow_run_id` links the MLflow record to the Airflow run. In MLflow, open the experiment and click `logistic-regression`. Inspect its Parameters, Metrics, Status, Run ID, and Tags.

![A real Logistic Regression run with accuracy and model settings](images/mlflow-run-details.png)

New runs also log **training_seconds**, accumulating time spent in fitting calls (`partial_fit` or `fit`). This differs from Airflow task duration, which includes notebook startup, scaling, evaluation, and saving artifacts. Durations vary with machine load; they are measurements, not fixed expected values.

### Which metrics to inspect

| Metric | Meaning | How to read it |
| --- | --- | --- |
| `train_accuracy` | Correct predictions on the 120 rows used for training | Higher is better |
| `test_accuracy` | Correct predictions on the 30 held-out rows | Higher is better; this selects the winner |
| `train_log_loss` | Probability-based error on training rows | Lower is better |
| `test_log_loss` | Probability-based error on held-out rows | Lower is better |
| `training_seconds` | Time spent fitting the model | Duration, not model quality |
| `accuracy` | Same value as `test_accuracy` | Kept for the existing winner/registry code |

Accuracy checks the chosen class. Log loss also checks the probability assigned to the true class; a confident wrong prediction is penalized heavily. We calculate log loss after fitting both models. For Random Forest it is an evaluation measure, not the criterion used to build its trees. See [scikit-learn log loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html).

A training score much better than the test score can suggest overfitting. This tiny test set supports a workshop demonstration, not a firm conclusion about generalization.

### Training progress and curves

Both notebooks now log accuracy and loss **during training**, after each real checkpoint. MLflow stores numeric values with step numbers; its Metrics page draws the history. These curves are not image artifacts.

| Model | Training method | History points | Meaning of Step |
| --- | --- | --- | --- |
| Logistic Regression | `SGDClassifier(loss="log_loss")`, with `partial_fit` | 30 | Epoch: one pass through training rows |
| Random Forest | `warm_start=True`, adding 10 trees per fit | 10 | Total trees: 10, 20, ..., 100 |

To expose progress, the logistic notebook now uses SGD-trained logistic regression instead of the earlier `LogisticRegression` estimator. It scales inputs using training rows only and saves that scaler with the classifier. Random Forest retains existing trees at each checkpoint. Its log loss is an evaluation measure, not the tree-building objective. See [SGDClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDClassifier.html).

The notebook calls `mlflow.log_metrics(metrics, step=step, synchronous=True)` inside the training loop, and prints one progress line to Airflow logs. Measurements are stored before the next step begins. MLflow's run table shows the latest values; the metric-history chart shows earlier points. See [MLflow tracking APIs](https://www.mlflow.org/docs/latest/ml/tracking/tracking-api).

Open a run's **Model metrics** tab to view its native MLflow charts against **Step**. Look for **train_log_loss**, **test_log_loss**, **train_accuracy**, and **test_accuracy**. Clicking a metric name in Overview also opens Model metrics. Use Step rather than wall-clock time to read training progress. The **Auto-refresh** control refreshes charts while a run is active.

![Actual MLflow numeric training histories from the Airflow pipeline](images/mlflow-training-history.png)

Iris trains quickly, so the run may finish before you refresh the UI. Refresh while it runs to inspect available values; the complete history remains afterward. Epochs and tree counts are different units, so compare final scores across models rather than treating their steps as equivalent. The repeatedly measured test scores demonstrate tracking; we do not tune settings using them.

## 3. Artifacts and logged models

Each training notebook logs `evaluation.json`, `confusion_matrix.png`, and its trained model. The model signature describes inputs/outputs; the small input example helps inspect it. Open the run's **Artifacts** tab, then select **confusion_matrix.png** to preview the plot. Open its logged model for model information.

In the confusion matrix, rows represent actual Iris classes and columns represent predicted classes. Numbers on the diagonal count correct predictions; numbers elsewhere count mistakes. This image evaluates the final model. Training histories are stored separately as numeric Metrics.

Parameters are settings, metrics are measurements, and artifacts are saved files. Logging a model is not the same operation as registering a version.

## 4. Compare approaches

The two model notebooks use the same 120 training rows and 30 test rows. In MLflow, select their run checkboxes and choose **Compare**. If there are older executions, choose the two runs with the same current `workflow_run_id` tag.

![MLflow comparison of the two actual training runs](images/mlflow-comparison.png)

The comparison notebook reads the final accuracy back from MLflow using the current run IDs. It rejects stale result files from another execution. Highest accuracy wins; a tie selects Logistic Regression, the first comparison row. The screenshot shows the earlier estimator; the current SGD training method can produce different scores and a different winner.

After triggering a fresh Airflow run, compare **train_accuracy**, **test_accuracy**, **train_log_loss**, **test_log_loss**, and **training_seconds** for its two training runs. Test accuracy still determines the winner. The comparison notebook displays the same metrics in its output table. Inspect each run's confusion matrix separately in Artifacts.

### Click through the results

1. Open [MLflow](http://localhost:5000), then **Experiments → iris-pipeline-comparison → Runs**. If the UI shows a Model training mode selector, use it; otherwise go directly to Experiments.
2. Open a new `logistic-regression` run. Overview lists the latest metric values; **Model metrics** shows the full histories against Step. The `progress_unit` tag identifies epochs or trees.
3. Open **Artifacts → evaluation.json** for the same values in a saved file, then **confusion_matrix.png** for the plot.
4. Return to Runs, select the matching Logistic Regression and Random Forest checkboxes, and click **Compare** to view their metrics side by side.
5. Use **Model registry → iris-pipeline-classifier** to inspect the selected version and candidate alias.

The run-details and training-history screenshots show the updated code executed through Airflow. The comparison screenshot shows the earlier verification run. Older records do not acquire new metrics, histories, or plots when notebook code changes. A fresh DAG run creates records with the current code.

## 5. Model lifecycle

The final notebook registers the saved winner, assigns `candidate`, and reloads it to verify the source run and accuracy. It also records a real MLflow trace for loading and predicting with that candidate. Continue with [the registry and tracing guide](07-model-registry.md).

## Important notes

Triggering the Airflow DAG records task execution and model results. Running notebooks manually records MLflow results when their logging cells execute, but does not create an Airflow run. Follow [guide 08](08-main-project.md) for the correct kernel and execution order.

The optional [MLflow basics reference](../notebooks/mlflow/01_mlflow_basics.ipynb) remains available if you want all operations in a single notebook. The main project is the workshop path.
