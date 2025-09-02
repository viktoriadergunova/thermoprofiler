import numpy as np
import pandas as pd
from . import config


def row_model_number(row):
    """Assign model number to a single row based on available logs."""
    available = [c for c in config.VALID_LOG_COLUMNS if c in row.index and pd.notna(row[c])]
    for num, combo in config.LOG_COMBINATIONS.items():
        if available == combo:
            return num
    return np.nan

def assign_model_numbers(df):
    """
    Assigns model_number column to the DataFrame.
    Drops rows without valid model_number.
    """
    df = df.copy()
    df["model_number"] = df.apply(row_model_number, axis=1)
    df = df.dropna(subset=["model_number"]).copy()
    df["model_number"] = df["model_number"].astype(int)
    return df
