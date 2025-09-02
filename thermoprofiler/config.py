# Configuration for ThermoProfiler package
# Defines rock type mappings, log combinations, model types, and model file paths

ROCK_TYPE_MAPPING = {1: "EVAPORITES", 2: "CARBONATES", 3: "CLASTICS"}
REVERSE_ROCK_TYPE_MAPPING = {"EVAPORITES": 1, "CARBONATES": 2, "CLASTICS": 3}

VALID_LOG_COLUMNS = {"RHOB", "PHIN", "VSH", "VP"}

VALID_MODEL_TYPES = ["ADABOOST", "LINEAR", "RF", "XGBBOOST"]
DEFAULT_MODEL_TYPE = "XGBBOOST"

LOG_COMBINATIONS = {
    1: ["RHOB"],
    2: ["PHIN"],
    3: ["VSH"],
    4: ["VP"],
    5: ["RHOB", "PHIN"],
    6: ["RHOB", "VSH"],
    7: ["RHOB", "VP"],
    8: ["PHIN", "VSH"],
    9: ["PHIN", "VP"],
    10: ["VSH", "VP"],
    11: ["RHOB", "PHIN", "VSH"],
    12: ["RHOB", "PHIN", "VP"],
    13: ["RHOB", "VSH", "VP"],
    14: ["PHIN", "VSH", "VP"],
    15: ["RHOB", "PHIN", "VSH", "VP"]
}

MODEL_BASE_PATH = "compiled_models"
MODEL_PATH_TEMPLATE = "{base_path}/{rock_type}/{model_type}/{property}/{filename}"

OUTPUT_PROPERTIES = ["TC", "SHC", "TD"]
OUTPUT_COLUMNS = ["thermal_conductivity", "specific_heat_capacity", "thermal_diffusivity"]

def generate_model_filename(model_number):
    """Generate model file name from model number (1 to 15)."""
    return f"{model_number}.joblib"

def get_model_number(log_columns):
    """Map sorted log columns to model number (1 to 15) or None if invalid."""
    sorted_columns = sorted(col.upper() for col in log_columns)
    for model_number, columns in LOG_COMBINATIONS.items():
        if sorted_columns == columns:
            return model_number
    return None

def is_valid_rock_type(rock_type_id):
    """Check if rock_type_id is valid (1, 2, or 3)."""
    return rock_type_id in ROCK_TYPE_MAPPING
