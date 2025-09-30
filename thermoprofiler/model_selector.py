import pandas as pd
import joblib
import os
from . import config


def load_model(rock_type_id, model_type, property_name, model_number):
    """
    Constructs path to the joblib model and loads it.
    """
    if rock_type_id not in config.ROCK_TYPE_MAPPING:
        raise ValueError(f"Invalid rock type ID: {rock_type_id}")

    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    model_folder = config.MODEL_TYPE_FOLDER_NAMES.get(model_type.upper())
    if model_folder is None:
        raise ValueError(f"Unknown model type: {model_type}")

    filename = config.generate_model_filename(model_number)
    model_path = config.MODEL_PATH_TEMPLATE.format(
        base_path=config.MODEL_BASE_PATH,
        rock_type=rock_type,
        model_type=model_folder,
        property=property_name,
        filename=filename
    )
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    return joblib.load(model_path)


def row_model_number_with_mape(row, model_type, prop):
    """
    Select the best model (lowest MAPE) given available logs.
    Falls back to raw-log model if no optimal is found.
    Returns: (model_number, mape, source)
    """
    best_model = None
    best_mape = float("inf")
    rock_type_id = row.get("Rock_type")

    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        return None, None, "NONE"

    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    available_logs = [col for col in config.VALID_LOG_COLUMNS if col in row and not pd.isna(row[col])]

    mape_key = f"BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_{prop}"
    mape_data = getattr(config, mape_key)[model_type][rock_type]

    for model_number, required_logs in config.LOG_COMBINATIONS.items():
        if all(log in available_logs for log in required_logs):
            current_mape = mape_data.get(model_number, float("inf"))
            if current_mape < best_mape:
                best_mape = current_mape
                best_model = model_number

    # fallback to raw logs if no optimal model found
    if best_model is None:
        best_model = config.get_model_number(available_logs)
        return best_model, None, "RAW"

    return best_model, best_mape, "MAPE"


def model_number_from_logs(row):
    """
    Return model number that exactly reflects the available logs in the row.
    """
    available_logs = [col for col in config.VALID_LOG_COLUMNS if col in row and not pd.isna(row[col])]
    return config.get_model_number(available_logs)
