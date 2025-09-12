# Configuration for ThermoProfiler package
# Defines rock type mappings, log combinations, model types, and model file paths
import os

ROCK_TYPE_MAPPING = {1: "EVAPORITES", 2: "CARBONATES", 3: "CLASTICS"}
REVERSE_ROCK_TYPE_MAPPING = {"EVAPORITES": 1, "CARBONATES": 2, "CLASTICS": 3}

VALID_LOG_COLUMNS = {"RHOB", "PHIN", "VSH", "VP"}

MODEL_TYPE_FOLDER_NAMES = {
    "XGBOOST": "XGBoost",
    "ADABOOST": "AdaBoost",
    "RF": "RF",
    "LINEAR": "Linear"
}

BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_TC = {
    "RF": {
        "EVAPORITES": {
            15: 7.2, 11: 7.5, 14: 7.3, 8: 8.5, 5: 9.2, 2: 9.8, 9: 8.9,
            12: 8.9, 13: 14.9, 10: 15.5, 7: 17.4, 4: 17.8, 6: 18.1,
            1: 19.9, 3: 22.0
        },
        "CARBONATES": {
            15: 5.2, 14: 5.5, 12: 5.3, 10: 5.6, 9: 6.7, 4: 6.8,
            13: 5.1, 11: 7.2, 7: 7.7, 6: 6.3, 5: 6.2, 1: 7.5,
            2: 9.0, 3: 27.0, 8: 7.2
        },
        "CLASTICS": {
            15: 7.7, 14: 9.8, 13: 8.8, 12: 10.3, 11: 6.8, 10: 8.3,
            9: 9.6, 8: 9.1, 7: 7.4, 6: 9.8, 5: 11.9, 4: 15.4,
            3: 23.9, 2: 12.4, 1: 15.4
        }
    },
    "XGBOOST": {
        "EVAPORITES": {
            15: 6.3, 14: 6.8, 9: 6.9, 11: 7.3, 12: 8.8, 5: 9.1, 8: 8.6,
            2: 10.1, 1: 19.9, 4: 17.8, 6: 18.1, 7: 17.3, 10: 15.6,
            13: 14.5, 3: 21.0
        },
        "CARBONATES": {
            15: 5.4, 14: 5.4, 13: 5.1, 12: 5.0, 11: 6.6, 10: 5.7,
            9: 6.0, 8: 7.2, 7: 6.2, 6: 6.3, 5: 7.1, 4: 6.8,
            3: 18.5, 2: 8.6, 1: 7.6
        },
        "CLASTICS": {
            15: 6.8, 14: 9.3, 13: 8.0, 12: 8.2, 11: 6.5, 10: 8.8,
            9: 9.2, 8: 10.6, 7: 7.4, 6: 9.4, 5: 11.9, 4: 15.3,
            3: 22.6, 2: 13.5, 1: 15.4
        }
    },
    "ADABOOST": {
        "EVAPORITES": {
            14: 10.0, 11: 10.1, 15: 10.1, 12: 10.2, 9: 10.4, 5: 10.4,
            2: 10.6, 1: 20.1, 4: 18.1, 6: 19.0, 7: 18.1, 8: 10.1,
            10: 17.0, 13: 16.9, 3: 22.0
        },
        "CARBONATES": {
            15: 6.5, 14: 7.6, 13: 7.2, 12: 7.5, 11: 7.6, 10: 7.6,
            9: 8.1, 8: 8.8, 7: 7.6, 6: 7.8, 5: 7.9, 4: 8.1,
            3: 24.0, 2: 9.1, 1: 8.0
        },
        "CLASTICS": {
            15: 7.7, 14: 11.2, 13: 8.9, 12: 10.6, 11: 8.6, 10: 11.3,
            9: 10.5, 8: 11.1, 7: 9.3, 6: 9.8, 5: 11.5, 4: 15.4,
            3: 22.3, 2: 13.1, 1: 15.2
        }
    },
    "LINEAR": {
        "EVAPORITES": {
            11: 9.2, 15: 9.2, 14: 9.5, 8: 10.0, 5: 10.1, 12: 10.1,
            9: 10.5, 2: 10.9, 1: 20.3, 4: 18.2, 6: 18.4, 7: 18.2,
            10: 16.4, 13: 16.4, 3: 22.0
        },
        "CARBONATES": {
            15: 6.6, 14: 5.1, 13: 9.7, 12: 9.6, 11: 9.5, 10: 9.5,
            9: 8.6, 8: 8.5, 7: 7.6, 6: 7.1, 5: 6.8, 4: 8.6,
            3: 6.5, 2: 9.1, 1: 8.5
        },
        "CLASTICS": {
            15: 10.5, 14: 11.0, 13: 8.9, 12: 14.4, 11: 7.7, 10: 11.3,
            9: 13.6, 8: 14.8, 7: 9.2, 6: 12.4, 5: 13.4, 4: 15.4,
            3: 21.2, 2: 13.6, 1: 15.8
        }
    }
}


BEST_MODEL_NUMBERS_BY_TYPE_AND_ROCK_SHC = {
    "RF": {
        "CARBONATES": {
            15: 0.5,
            14: 0.8,
            13: 0.9,
            12: 0.8,
            11: 0.7,
            10: 0.9,
            9: 2.0,
            8: 1.6,
            7: 2.2,
            6: 5.8,
            5: 6.5,
            4: 6.8,
            3: 9.2,
            2: 8.2,
            1: 5.8
        },
        "CLASTICS": {
            15: 2.2,
            14: 2.3,
            13: 3.3,
            12: 3.3,
            11: 4.4,
            10: 4.3,
            9: 4.2,
            8: 4.5,
            7: 5.1,
            6: 9.3,
            5: 10.1,
            4: 10.3,
            3: 13.3,
            2: 9.3,
            1: 9.8
        }
    },
    "XGBOOST": {
        "CARBONATES": {
            15: 0.7,
            14: 0.7,
            13: 0.8,
            12: 0.8,
            11: 0.8,
            10: 0.9,
            9: 2.3,
            8: 1.8,
            7: 2.3,
            6: 5.8,
            5: 6.4,
            4: 6.9,
            3: 9.2,
            2: 8.2,
            1: 5.8
        },
        "CLASTICS": {
            15: 0.7,
            14: 0.7,
            13: 0.9,
            12: 1.2,
            11: 2.2,
            10: 2.3,
            9: 2.0,
            8: 2.3,
            7: 2.6,
            6: 5.4,
            5: 6.0,
            4: 6.2,
            3: 9.3,
            2: 9.8,
            1: 9.9
        }
    },
    "ADABOOST": {
        "CARBONATES": {
            15: 0.8,
            14: 1.0,
            13: 1.0,
            12: 1.0,
            11: 1.1,
            10: 1.2,
            9: 2.4,
            8: 1.9,
            7: 2.6,
            6: 6.2,
            5: 6.6,
            4: 6.7,
            3: 9.3,
            2: 9.1,
            1: 5.7
        },
        "CLASTICS": {
            15: 0.7,
            14: 0.9,
            13: 1.1,
            12: 1.1,
            11: 2.3,
            10: 2.3,
            9: 2.2,
            8: 2.3,
            7: 2.8,
            6: 6.6,
            5: 6.8,
            4: 6.9,
            3: 9.2,
            2: 9.1,
            1: 9.2
        }
    },
    "LINEAR": {
        "CARBONATES": {
            15: 1.7,
            14: 1.9,
            13: 2.1,
            12: 2.2,
            11: 2.3,
            10: 2.6,
            9: 2.9,
            8: 3.4,
            7: 4.2,
            6: 6.3,
            5: 6.5,
            4: 6.7,
            3: 9.1,
            2: 9.6,
            1: 5.8
        },
        "CLASTICS": {
            15: 0.7,
            14: 0.9,
            13: 1.1,
            12: 1.2,
            11: 2.3,
            10: 2.4,
            9: 2.4,
            8: 2.6,
            7: 3.0,
            6: 6.4,
            5: 6.6,
            4: 6.8,
            3: 9.6,
            2: 9.3,
            1: 10.0
        }
    }
}

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

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_BASE_PATH = os.path.abspath(os.path.join(PACKAGE_ROOT, "..", "compiled_models"))
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
