# Model versions and candidate

## Purpose

Keep the winning model traceable to its training run and give it a stable lookup name.

## Code and configuration

The work is in [05_register_candidate.ipynb](../notebooks/project/05_register_candidate.ipynb), executed by Airflow's `register_candidate` task.

- Registered model: **iris-pipeline-classifier**.
- Version: a numbered reference to the winning saved model.
- Alias: **candidate**, pointing to the version selected by this completed workflow.

The notebook registers `winner["model_uri"]`, rather than retraining. Its `set_registered_model_alias` call assigns the alias, then it reloads `models:/iris-pipeline-classifier@candidate` and checks the original run and accuracy.

## Inspect the UI

1. Complete the main pipeline and open [MLflow](http://localhost:5000) in Model training mode.
2. Select **Model registry**, then **iris-pipeline-classifier**.
3. Open a numbered version to inspect the source model/run.
4. Find **candidate** in the Aliases column.

![Registered pipeline model with the candidate alias](images/mlflow-model-alias.png)

## Expected result

A numbered version has the candidate alias. `candidate.json` in the Airflow run's output folder records its name, version, source run, verified accuracy, and verification trace ID.

## Inspect the verification trace

The same registration notebook now instruments its candidate check. A **trace** is the complete verification operation; its **spans** are timed steps inside it:

```text
verify_candidate
├── load_candidate
└── predict_candidate
```

1. Trigger a fresh main DAG run and wait for registration to finish.
2. Open MLflow → **Experiments → iris-pipeline-comparison → Traces**. If the UI requires switching to an LLMs/GenAI view to show Traces, switch views and select the same experiment; no LLM is involved in this example.
3. Open the row whose input contains the candidate model URI. Its trace viewer shows **verify_candidate** as the root. Match the trace ID printed in the Airflow registration log or saved in `candidate.json` if there are several.
4. Inspect the root's status and duration. Its inputs identify the alias/version; its outputs show verified accuracy. The trace links to the winning training run, and its `workflow_run_id` tag identifies the workflow execution.
5. Select **load_candidate** to inspect the model URI and loaded model identity.
6. Select **predict_candidate** to inspect the actual 30 Iris input rows and their predicted classes, along with timing.

![Actual candidate verification trace with loading and prediction spans](images/mlflow-candidate-trace.png)

`mlflow.start_span(...)` creates the nested spans. `set_inputs` and `set_outputs` record their data. The notebook explicitly selects the project experiment with `mlflow.set_experiment(experiment_name)`, because every Airflow notebook starts in a separate Python process. The root uses `run_id=winner["run_id"]` to link the trace to the existing winning run, without adding another training run. Closing the root exports the trace; the notebook flushes pending writes before exiting.

If loading, prediction, or verification raises an exception, the affected open span records the error and the exception still reaches Airflow. We do not deliberately fail the main project. The separate Airflow failure demo remains the failure exercise. See [MLflow manual tracing](https://mlflow.org/docs/latest/genai/tracing/app-instrumentation/manual-tracing).

Training loss/accuracy histories belong under **Model metrics**. This verification belongs under **Traces**. The confusion matrix belongs under **Artifacts**. The trace screenshot shows a real Airflow execution with candidate version 6; version numbers change on future registrations. Older executions do not gain traces retroactively.

## Important notes

Each registration adds a version. Assigning candidate moves the alias while preserving older versions. This does not deploy a model. The source artifact files must remain accessible from the runtime platform that saved them. One main DAG run is active at a time to keep selection orderly.

The screenshot is from a real validated local run; its version number will differ after additional registrations.
