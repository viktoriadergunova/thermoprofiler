import pandas as pd
from . import config
from .model_selector import (
    row_model_number_with_mape,
    load_model,
    model_number_from_logs
)

def predict_all_properties(df, model_type="XGBOOST"):
    df = df.copy()
    df["Rock_type"] = pd.to_numeric(df["Rock_type"], errors="coerce").astype("Int64")

    for prop in config.OUTPUT_PROPERTIES:
        # Step 1: Select MAPE-optimal model numbers and their MAPE values (= uncertainty)
        results = df.apply(
            lambda row: row_model_number_with_mape(row, model_type=model_type, prop=prop),
            axis=1,
            result_type="expand"
        )
        df[f"model_number_{prop}"] = results[0]
        df[f"uncertainty_{prop}"] = results[1]   # <-- renamed from mape_*

        # Step 2: Determine raw-log-reflective model numbers
        df[f"model_number_raw_{prop}"] = df.apply(model_number_from_logs, axis=1)

    for prop in config.OUTPUT_PROPERTIES:
        col_opt = f"{prop}_prediction"          # <-- clearer naming
        col_raw = f"{prop}_prediction_raw"
        df[col_opt] = pd.NA
        df[col_raw] = pd.NA

        # A. Predict using MAPE-optimal model
        for (rock_type_id, model_number), group in df.groupby(["Rock_type", f"model_number_{prop}"]):
            if pd.isna(model_number) or pd.isna(rock_type_id):
                continue
            try:
                model_number = int(model_number)
                log_cols = config.LOG_COMBINATIONS[model_number]
                if any(col not in group.columns for col in log_cols):
                    continue

                X = group[log_cols]
                if X.isnull().any(axis=1).all():
                    continue

                model = load_model(rock_type_id, model_type, prop, model_number)
                y_pred = model.predict(X)
                df.loc[group.index, col_opt] = y_pred
            except Exception as e:
                print(f"[MAPE_OPT] Error predicting {prop} with model {model_number} (rock {rock_type_id}): {e}")

        # B. Predict using raw-log-based model
        for (rock_type_id, model_number), group in df.groupby(["Rock_type", f"model_number_raw_{prop}"]):
            if pd.isna(model_number) or pd.isna(rock_type_id):
                continue
            try:
                model_number = int(model_number)
                log_cols = config.LOG_COMBINATIONS[model_number]
                if any(col not in group.columns for col in log_cols):
                    continue

                X = group[log_cols]
                if X.isnull().any(axis=1).all():
                    continue

                model = load_model(rock_type_id, model_type, prop, model_number)
                y_pred = model.predict(X)
                df.loc[group.index, col_raw] = y_pred
            except Exception as e:
                print(f"[RAW_LOGS] Error predicting {prop} with model {model_number} (rock {rock_type_id}): {e}")

    return df
