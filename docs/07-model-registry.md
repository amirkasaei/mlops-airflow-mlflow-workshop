# Model Registry

Read this guide after completing model comparison and winner selection.

## Purpose

Give the winning saved model a name and version that can be traced to its training run.

## What this covers

- **Registered model:** `iris-classifier`, the shared name for our selected models.
- **Version:** a numbered saved model under that name.
- **Alias:** `candidate`, a movable name pointing to the selected version.

## How to proceed

Run the notebook's registration cell, then its alias cell, then its reload verification cell. These depend on the earlier training and selection cells. There is no additional installation or terminal command.

## Expected result

Open **Models** in the MLflow UI and select `iris-classifier`. You should see a numbered version with the `candidate` alias. The final verification cell reloads it and checks its accuracy.

## Important notes

Registration saves a new version reference without retraining. Repeating registration creates another version. Moving `candidate` preserves previous versions. This step does not deploy a model.
