import pandas as pd
from . import config

def row_model_number(row, model_type, prop):
    """
    Select the best model number for a given row and property (TC, SHC, TD),
    based on available logs, rock type, and lowest MAPE.
    """
    rock_type_id = row.get("Rock_type")
    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        return None

    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    model_type = model_type.upper()

    if model_type not in config.VALID_MODEL_TYPES:
        model_type = config.DEFAULT_MODEL_TYPE

    available_logs = [
        col.upper()
        for col in config.VALID_LOG_COLUMNS
        if col in row.index and not pd.isna(row[col])
    ]

    best_model = None
    best_mape = float("inf")

    for model_number, required_logs in config.LOG_COMBINATIONS.items():
        if all(log in available_logs for log in required_logs):
            mape_key = f"BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_{prop}"
            if hasattr(config, mape_key):
                mape_data = getattr(config, mape_key).get(model_type, {})
                rock_mape = rock_mape = mape_data.get(rock_type, {})
                current_mape = rock_mape.get(model_number, float("inf"))

                if current_mape < best_mape:
                    best_mape = current_mape
                    best_model = model_number

    return best_model
