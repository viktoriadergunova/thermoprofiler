import pandas as pd
from . import config

def row_model_number_with_mape(row, model_type, prop):
    best_model = None
    best_mape = float('inf')
    rock_type_id = row.get("Rock_type")
    
    if pd.isna(rock_type_id) or rock_type_id not in config.ROCK_TYPE_MAPPING:
        return None, None
    
    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    available_logs = [col for col in config.VALID_LOG_COLUMNS if col in row and not pd.isna(row[col])]
    
    for model_number, required_logs in config.LOG_COMBINATIONS.items():
        if all(log in available_logs for log in required_logs):
            mape_key = f"BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_{prop}"
            mape_data = getattr(config, mape_key)[model_type][rock_type]
            current_mape = mape_data.get(model_number, float('inf'))
            
            if current_mape < best_mape:
                best_mape = current_mape
                best_model = model_number
    
    return best_model, best_mape
