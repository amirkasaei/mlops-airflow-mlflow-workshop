# MLflow setup

## Purpose

Save training results locally and view them in your browser.

## What we use

- **SQLite** stores MLflow records in one file: `mlflow.db`.
- **MLflow UI** is the browser interface for viewing those records.
- Saved model files go into `mlartifacts/`, separately from the database.

SQLite is included with Python. You do not need to install it or start a database server. MLflow creates the database file and its tables automatically.

## Steps

### 1. Prepare the environment

Complete [Python environment setup](01-python-setup.md). Keep a terminal open at the project root with `mlops-workshop-env` activated.

### 2. Create the local MLflow records

Open `notebooks/01_mlflow_basics.ipynb` with that environment selected as its kernel. Run the imports cell, then the cells under **Find the project folder**, **Configure tracking**, and **Select the experiment**.

These setup cells tell MLflow to use `mlflow.db` in the project root and create or select the experiment `iris-model-comparison`. They print the database location and experiment name. No model has been trained by this step.

### 3. Start the browser interface

From the activated project-root terminal, run this command on Windows, Linux, or macOS:

```sh
python -m mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

This starts the UI using the same `mlflow.db` file. `127.0.0.1` means your own computer; `5000` is the port used by the browser.

### 4. Open MLflow

Leave the command running and open [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Expected result

Under **Experiments**, you should see `iris-model-comparison`. Training runs will appear as you execute the later notebook cells; refresh the browser to see updates.

## Important notes

Run the UI command from the project root so it opens the correct database. Keep its terminal open; Ctrl+C stops the UI without deleting results. If the page cannot open, check that the command is still running and has not reported an error. If this project's UI already opens, reuse it instead of starting a second server.
