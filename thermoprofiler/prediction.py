import pandas as pd
import joblib
import os

from . import config
from .model_selector import row_model_number_with_mape

# Load a trained model from disk
def load_model(rock_type_id, model_type, property, model_number):
    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id].capitalize()  # e.g., "CLASTICS" → "Clastics"

    try:
        model_type_folder = config.MODEL_TYPE_FOLDER_NAMES[model_type.upper()]
    except KeyError:
        raise ValueError(f"Unknown model type '{model_type}'. Valid types: {list(config.MODEL_TYPE_FOLDER_NAMES.keys())}")

    filename = config.generate_model_filename(model_number)
    path = config.MODEL_PATH_TEMPLATE.format(
        base_path=config.MODEL_BASE_PATH,
        rock_type=rock_type,
        model_type=model_type_folder,
        property=property,
        filename=filename
    )

    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found at: {path}")

    return joblib.load(path)


# Predict all thermal properties (TC, SHC, TD) for the input DataFrame
def predict_all_properties(df, model_type="XGBOOST"):
    df = df.copy()
    df["Rock_type"] = pd.to_numeric(df["Rock_type"], errors="coerce").astype("Int64")

    # Step 1: Select best model and MAPE for each property
    for prop in config.OUTPUT_PROPERTIES:
        results = df.apply(
            lambda row: row_model_number_with_mape(row, model_type=model_type, prop=prop),
            axis=1,
            result_type="expand"
        )
        df[f"model_number_{prop}"] = results[0]
        df[f"mape_{prop}"] = results[1]

    # Step 2: Initialize empty prediction columns
    predictions = {prop: pd.Series(index=df.index, dtype=float) for prop in config.OUTPUT_PROPERTIES}

    # Step 3: Predict per property using grouped model numbers
    for prop in config.OUTPUT_PROPERTIES:
        model_col = f"model_number_{prop}"
        for (rock_type_id, model_number), group in df.groupby(["Rock_type", model_col]):
            if pd.isna(model_number) or pd.isna(rock_type_id):
                continue

            try:
                model_number = int(model_number)
                log_cols = config.LOG_COMBINATIONS[model_number]

                # Ensure all required logs are present in the group
                missing_logs = [col for col in log_cols if col not in group.columns]
                if missing_logs:
                    print(f"Skipping model {model_number} for {prop}: missing logs {missing_logs}")
                    continue

                X = group[log_cols]
                if X.isnull().any(axis=1).all():
                    continue  # Skip if all inputs are NaN

                model = load_model(rock_type_id, model_type, prop, model_number)
                y_pred = model.predict(X)

                predictions[prop].loc[group.index] = y_pred
            except Exception as e:
                print(f"Error predicting {prop} for model {model_number}, rock_type {rock_type_id}: {e}")

        df[prop] = predictions[prop]

    return df
