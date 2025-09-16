# thermoprofiler/model_selector.py

import pandas as pd
from . import config 

def row_model_number(row, model_type):
    # Select the optimal model number for a rowbased on available logs and smallest Mape for the given model type 

    rock_type_id = row["Rock_type"]
    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        return None 
    
    rock_type = config.ROCK_TYPE_MAPPING [rock_type_id]
    model_type = model_type.upper()

    if model_type not in config.VALID_MODEL_TYPES:
        model_type = config.DEFAULT_MODEL_TYPE  # Fall back XGBOOST 


    available_logs = [col.upper() for col in config.VALID_LOG_COLUMNS if col in row.index and not pd.isna(row[col])]
    
    # Initialize best model and MAPE
    best_model = None
    best_mape = float("inf")

    # Check all model combinations
    for model_number, log_combo in config.LOG_COMBINATIONS.items():
        # Ensure all logs in the combo are available
        if all(log in available_logs for log in log_combo):
            # Evaluate MAPE for each property
            for prop in config.OUTPUT_PROPERTIES:
                mape_key = f"BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_{prop}"
                if hasattr(config, mape_key):
                    mape_data = getattr(config, mape_key).get(model_type, {})
                    rock_mape = mape_data.get(rock_type, {})
                    current_mape = rock_mape.get(model_number, float("inf"))
                    # Take the minimum MAPE across properties as the deciding factor
                    if current_mape < best_mape:
                        best_mape = current_mape
                        best_model = model_number

    return best_model