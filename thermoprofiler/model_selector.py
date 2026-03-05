import pandas as pd
import joblib
import os
from . import config


def load_model(rock_type_id, model_type, property_name, model_number, verbose=False):
    """
    Constructs path to the joblib model and loads it.
    Returns: (model, model_path, model_number)
    """
    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        raise ValueError(f"Invalid rock type ID: {rock_type_id}")

    model_type_key = str(model_type).upper()
    model_folder = config.MODEL_TYPE_FOLDER_NAMES.get(model_type_key)
    if model_folder is None:
        raise ValueError(f"Unknown model type: {model_type}")

    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    filename = config.generate_model_filename(model_number)

    model_path = config.MODEL_PATH_TEMPLATE.format(
        base_path=config.MODEL_BASE_PATH,
        rock_type=rock_type,
        model_type=model_folder,
        property=property_name,
        filename=filename,
    )

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    if verbose:
        print(f"[MODEL LOAD] model_number={model_number}")
        print(f"[MODEL LOAD] path={model_path}")

    model = joblib.load(model_path)
    return model, model_path, model_number


def row_model_number_with_mape(row, model_type, prop):
    """
    Select the best model (lowest MAPE) given available logs.
    Falls back to raw-log model if no optimal is found.
    Returns: (model_number, mape, source)
      - source in {"MAPE", "RAW", "NONE"}
    """
    rock_type_id = row.get("Rock_type")

    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        return None, None, "NONE"

    model_type_key = str(model_type).upper()
    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]

    # available logs in this row
    available_logs = [
        col
        for col in config.VALID_LOG_COLUMNS
        if col in row and not pd.isna(row[col])
    ]

    # pull MAPE table for this property / model_type / rock_type
    mape_key = f"BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_{prop}"
    try:
        mape_table = getattr(config, mape_key)
    except AttributeError as e:
        raise AttributeError(f"Missing config attribute: {mape_key}") from e

    try:
        mape_data = mape_table[model_type_key][rock_type]
    except KeyError as e:
        raise KeyError(
            f"Missing MAPE data for model_type={model_type_key}, rock_type={rock_type}, key={mape_key}"
        ) from e

    best_model = None
    best_mape = float("inf")

    # choose best model among those whose required logs are present
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
    available_logs = [
        col
        for col in config.VALID_LOG_COLUMNS
        if col in row and not pd.isna(row[col])
    ]
    return config.get_model_number(available_logs)


def select_and_load_model(row, model_type, prop, verbose=False):
    """
    Convenience wrapper:
      - selects model_number via MAPE (or RAW fallback)
      - loads model
    Returns: (model, model_number, model_path, source, mape)
    """
    model_number, mape, source = row_model_number_with_mape(row, model_type, prop)

    if model_number is None:
        if verbose:
            print("[MODEL SELECT] model_number=None (source=NONE)")
        return None, None, None, source, mape

    model, model_path, model_number = load_model(
        rock_type_id=row.get("Rock_type"),
        model_type=model_type,
        property_name=prop,
        model_number=model_number,
        verbose=verbose,
    )

    if verbose:
        print(f"[MODEL SELECT] source={source} mape={mape}")

    return model, model_number, model_path, source, mape
