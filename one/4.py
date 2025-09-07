import mlflow
from mlflow import MlflowClient
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

#######  创建实验
# client = MlflowClient(tracking_uri="http://127.0.0.1:5000")
#
# # Provide an Experiment description that will appear in the UI
# experiment_description = (
#     "This is the grocery forecasting project. "
#     "This experiment contains the produce models for apples."
# )
#
# # Provide searchable tags that define characteristics of the Runs that
# # will be in this Experiment
# experiment_tags = {
#     "project_name": "grocery-forecasting",
#     "store_dept": "produce",
#     "team": "stores-ml",
#     "project_quarter": "Q3-2023",
#     "mlflow.note.content": experiment_description,
# }
#
# # Create the Experiment, providing a unique name
# produce_apples_experiment = client.create_experiment(
#     name="Apple_Models", tags=experiment_tags
# )

mlflow.set_tracking_uri("http://127.0.0.1:5000")

# Sets the current active experiment to the "Apple_Models" experiment and
# returns the Experiment metadata
apple_experiment = mlflow.set_experiment("Apple_Models")

# Define a run name for this iteration of training.
# If this is not set, a unique name will be auto-generated for your run.
run_name = "apples_rf_test"

# Define an artifact path that the model will be saved to.
artifact_path = "rf_apples"

from three import data
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Split the data into features and target and drop irrelevant date field and target field
X = data.drop(columns=["date", "demand"])
y = data["demand"]

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

params = {
    "n_estimators": 100,
    "max_depth": 6,
    "min_samples_split": 10,
    "min_samples_leaf": 4,
    "bootstrap": True,
    "oob_score": False,
    "random_state": 888,
}

# Train the RandomForestRegressor
rf = RandomForestRegressor(**params)

# Fit the model on the training data
rf.fit(X_train, y_train)

# Predict on the validation set
y_pred = rf.predict(X_val)

# Calculate error metrics
mae = mean_absolute_error(y_val, y_pred)
mse = mean_squared_error(y_val, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_val, y_pred)

# Assemble the metrics we're going to write into a collection
metrics = {"mae": mae, "mse": mse, "rmse": rmse, "r2": r2}

# Initiate the MLflow run context
with mlflow.start_run(run_name=run_name) as run:
    # Log the parameters used for the model fit
    mlflow.log_params(params)

    # Log the error metrics that were calculated during validation
    mlflow.log_metrics(metrics)

    # Log an instance of the trained model for later use
    mlflow.sklearn.log_model(sk_model=rf, input_example=X_val, name=artifact_path)