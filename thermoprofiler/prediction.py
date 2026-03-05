import sys
import sklearn
import pandas as pd

from . import config
from .model_selector import (
    row_model_number_with_mape,
    load_model,
    model_number_from_logs,
)

print("RUNNING:", sys.executable, "sklearn:", sklearn.__version__)


def _lookup_mape_for_model(rock_type_id, model_type, prop, model_number):
    """
    Return the stored MAPE for a given (model_type, rock_type, prop, model_number).
    If not available, returns pd.NA.
    """
    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        return pd.NA
    if pd.isna(model_number):
        return pd.NA

    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    model_type_key = str(model_type).upper()

    mape_key = f"BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_{prop}"
    try:
        mape_table = getattr(config, mape_key)
        mape_data = mape_table[model_type_key][rock_type]
    except Exception:
        return pd.NA

    try:
        return mape_data.get(int(model_number), pd.NA)
    except Exception:
        return pd.NA


def predict_all_properties(df, model_type="XGBOOST", selection_mode="MAPE", verbose=False, add_paths=True):
    selection_mode = str(selection_mode).upper()
    if selection_mode not in {"MAPE", "ALL_LOGS"}:
        raise ValueError(f"selection_mode must be 'MAPE' or 'ALL_LOGS', got: {selection_mode}")

    df = df.copy()
    df["Rock_type"] = pd.to_numeric(df["Rock_type"], errors="coerce").astype("Int64")

    # compute ALL_LOGS model_number once (independent of prop)
    all_logs_model_number = df.apply(model_number_from_logs, axis=1)

    # Step 1: choose model numbers + attach MAPE for the chosen model (even in ALL_LOGS mode)
    for prop in config.OUTPUT_PROPERTIES:
        if selection_mode == "MAPE":
            results = df.apply(
                lambda row: row_model_number_with_mape(row, model_type=model_type, prop=prop),
                axis=1,
                result_type="expand",
            )
            df[f"model_number_{prop}"] = results[0]
            df[f"expected_mape_{prop}"] = results[1]      # MAPE of the selected (best) model
            df[f"model_source_{prop}"] = results[2]       # "MAPE"/"RAW"/"NONE"
        else:
            df[f"model_number_{prop}"] = all_logs_model_number
            # MAPE of the selected ALL_LOGS model (not "best", but still meaningful)
            df[f"expected_mape_{prop}"] = df.apply(
                lambda r: _lookup_mape_for_model(r.get("Rock_type"), model_type, prop, r.get(f"model_number_{prop}")),
                axis=1,
            )
            df[f"model_source_{prop}"] = "ALL_LOGS"

        # will be filled during prediction
        df[f"Logs_used_{prop}"] = pd.NA
        if add_paths:
            df[f"model_path_{prop}"] = pd.NA

    # Step 2: predict per prop using the chosen model_number_{prop}
    for prop in config.OUTPUT_PROPERTIES:
        pred_col = f"{prop}_prediction"
        df[pred_col] = pd.NA

        for (rock_type_id, model_number), group in df.groupby(["Rock_type", f"model_number_{prop}"]):
            if pd.isna(model_number) or pd.isna(rock_type_id):
                continue

            try:
                model_number = int(model_number)
                log_cols = config.LOG_COMBINATIONS[model_number]

                if any(col not in group.columns for col in log_cols):
                    continue

                X = group[log_cols]
                X_clean = X.dropna()
                if X_clean.empty:
                    continue

                model, model_path, used_model_number = load_model(
                    rock_type_id=rock_type_id,
                    model_type=model_type,
                    property_name=prop,
                    model_number=model_number,
                    verbose=False,
                )

                if verbose:
                    print(f"[{selection_mode}] rock={rock_type_id} prop={prop} model={used_model_number} path={model_path}")
                    print(f"[{selection_mode}] logs_used={log_cols}")

                y_pred = model.predict(X_clean)
                df.loc[X_clean.index, pred_col] = y_pred

                # store logs used + path for all rows in that group (even those dropped can be left NA)
                df.loc[group.index, f"Logs_used_{prop}"] = ",".join(log_cols)
                if add_paths:
                    df.loc[group.index, f"model_path_{prop}"] = model_path

            except Exception as e:
                print(f"[{selection_mode}] Error predicting {prop} with model {model_number} (rock {rock_type_id}): {e}")

    return df
