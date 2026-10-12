# Python setup

## Purpose

Use a local environment for notebook dependencies and select that same environment in VS Code.

This guide is for the reference notebook. Airflow uses the separate Airflow environment described in [Airflow setup](01-airflow-setup.md).

## What is configured

The environment is named `mlops-workshop-env` and is excluded from Git. Dependencies are MLflow, scikit-learn, pandas, and ipykernel. Use Python 3.12, 3.13, or 3.14 for a consistent workshop setup; the current notebook was validated on Python 3.14.2.

## Commands

Run commands from the project root. Skip creation if the environment already exists.

**Windows PowerShell:**

```powershell
python -m venv mlops-workshop-env
```

```powershell
.\mlops-workshop-env\Scripts\Activate.ps1
```

**Linux/macOS:**

```sh
python3 -m venv mlops-workshop-env
```

```sh
source mlops-workshop-env/bin/activate
```

**Either platform, after activation:**

```sh
python -m pip install -r requirements.txt
```

```sh
python -c "import sys; print(sys.executable)"
```

If PowerShell blocks activation, install through the environment's Python directly:

```powershell
.\mlops-workshop-env\Scripts\python.exe -m pip install -r requirements.txt
```

## Expected result

The printed interpreter path points inside `mlops-workshop-env`. In VS Code, install the Microsoft Python and Jupyter extensions. Use **Python: Select Interpreter** to select this environment, then open the notebook and choose **Select Kernel > Python Environments > mlops-workshop-env**. Its first cell prints the interpreter and package versions.

## Important notes

Editor interpreter and notebook kernel are separate selections. On Windows the interpreter is `mlops-workshop-env/Scripts/python.exe`; on Linux/macOS it is `mlops-workshop-env/bin/python`. The environment is local and must stay out of the repository. No global Jupyter kernel registration is necessary.
