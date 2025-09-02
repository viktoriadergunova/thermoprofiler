import os 
import config 

# Function to get model paths based on rock type and model type
def get_models_paths(rock_type_id, model_type, log_columns):
    # Validate inputs: Check rock_type and model_type
    if not config.is_valid_rock_type(rock_type_id):
        raise ValueError(f"Invalid rock type ID: {rock_type_id}. Must be 1, 2, or 3.")
    
    model_type = model_type.upper() if model_type else config.DEFAULT_MODEL_TYPE
    if model_type not in config.VALID_MODEL_TYPES:
        raise ValueError(f"Invalid model type: {model_type}. Must be one of {config.VALID_MODEL_TYPES}.")
    
    model_number = config.get_model_number(log_columns)
    if model_number is None:
        raise ValueError(f"Invalid log columns: {log_columns}. Must be a combination of {list(config.VALID_LOG_COLUMNS)}.")
    
    rock_type = config.ROCK_TYPE_MAPPING[rock_type_id]
    filename = config.generate_model_filename(model_number)

    paths = {}
    for property in config.OUTPUT_PROPERTIES:
        path = config.MODEL_PATH_TEMPLATE.format(
            base_path=config.MODEL_BASE_PATH,
            rock_type=rock_type,
            model_type=model_type,
            property=property,
            filename=filename
        )
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model not found: {path}")
        paths[property] = path
    
    return paths