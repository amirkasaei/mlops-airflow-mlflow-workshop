# Python setup

## Purpose

Check Python first, understand our environments, and prepare the notebook environment in VS Code. Both Airflow and MLflow execute Python code.

## Check Python first

Use Python 3.12, 3.13, or 3.14 for this workshop. If Python is missing, install one of these versions from [Python.org](https://www.python.org/downloads/) or your Linux distribution's package manager.

**Windows PowerShell:**

```powershell
python --version
```

**Linux/macOS:**

```sh
python3 --version
```

## Which environment is used?

| Environment | Location | Purpose |
| --- | --- | --- |
| Notebook | `mlops-workshop-env/` in the project folder | Run notebook cells using the VS Code kernel |
| Airflow | `~/mlops-airflow-workshop/mlops-workshop-env` | Run DAG tasks; on Windows this environment is inside WSL |

The commands below prepare the notebook environment. The next guide, [Airflow setup](02-airflow-setup.md), prepares its separate environment in WSL, Linux, or macOS. A Windows environment cannot be reused inside WSL.

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
