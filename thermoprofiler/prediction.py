import pandas as pd
import joblib
import os

from . import config
from .model_selector import row_model_number

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


def predict_all_properties(df, model_type="XGBOOST"):
    df = df.copy()
    df["Rock_type"] = pd.to_numeric(df["Rock_type"], errors="coerce").astype("Int64")

    # Step 1: Determine the best model number per property
    for prop in config.OUTPUT_PROPERTIES:
        df[f"model_number_{prop}"] = df.apply(
            lambda row: row_model_number(row, model_type=model_type, prop=prop),
            axis=1
        )

    # Step 2: Initialize predictions
    predictions = {prop: pd.Series(index=df.index, dtype=float) for prop in config.OUTPUT_PROPERTIES}

    # Step 3: Predict per property using grouped model numbers
    for prop in config.OUTPUT_PROPERTIES:
        for (rock_type_id, model_number), group in df.groupby(["Rock_type", f"model_number_{prop}"]):
            if pd.isna(model_number) or pd.isna(rock_type_id):
                continue

            try:
                log_cols = config.LOG_COMBINATIONS[model_number]
                X = group[log_cols]

                model = load_model(rock_type_id, model_type, prop, model_number)
                y_pred = model.predict(X)

                predictions[prop].loc[group.index] = y_pred
            except Exception as e:
                print(f"Error predicting {prop} for model {model_number}, rock_type {rock_type_id}: {e}")

        df[prop] = predictions[prop]

    return df
