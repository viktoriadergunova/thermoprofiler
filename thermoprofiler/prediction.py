import pandas as pd
import joblib
from . import config
import os

def load_model(rock_type_id, model_type, property, model_number):
    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id].capitalize()  # "CLASTICS" → "Clastics"
    
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
    print("Trying to load model at path:", path)
    print("Exists:", os.path.exists(path))
    print("Full path:", os.path.abspath(path))

    return joblib.load(path)


def predict_all_properties(df, model_type="XGBOOST"):
    """
    Predict TC, SHC, and TD for each row in the dataframe based on its model_number and Rock_type.
    """
    df = df.copy()

    # Clean Rock_type column to ensure it's numeric
    df["Rock_type"] = pd.to_numeric(df["Rock_type"], errors="coerce").astype("Int64")

    predictions = {
        "TC": pd.Series(index=df.index, dtype=float),
        "SHC": pd.Series(index=df.index, dtype=float),
        "TD": pd.Series(index=df.index, dtype=float),
    }

    for (rock_type_id, model_number), group in df.groupby(["Rock_type", "model_number"]):
        log_cols = config.LOG_COMBINATIONS[model_number]
        X = group[log_cols]

        for prop in ["TC", "SHC", "TD"]:
            model = load_model(rock_type_id, model_type, prop, model_number)
            y_pred = model.predict(X)
            predictions[prop].loc[group.index] = y_pred

    for prop in predictions:
        df[prop] = predictions[prop]

    return df
