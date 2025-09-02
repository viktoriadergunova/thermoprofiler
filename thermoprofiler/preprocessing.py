import pandas as pd
import numpy as np
from . import config

def clean_log_dataframe(df):
    """Clean raw well-log dataframe for model use."""
    df = df.copy()
    df = df.rename(columns=lambda c: c.strip())

    # Convert and clean log values
    for col in config.VALID_LOG_COLUMNS:
        if col in df.columns:
            s = df[col].astype(str).str.strip()
            s = s.str.replace(",", ".", regex=False)
            s = pd.to_numeric(s, errors="coerce")
            s = s.where(~(s <= -9), np.nan)
            df[col] = s

    # Normalize PHIN and VSH
    if "PHIN" in df.columns and df["PHIN"].dropna().max() > 1.5:
        df["PHIN"] = df["PHIN"] / 100.0
    if "VSH" in df.columns and df["VSH"].dropna().max() > 1.5:
        df["VSH"] = df["VSH"] / 100.0

    # Drop rows where *all* log columns are NaN
    log_cols = list(config.VALID_LOG_COLUMNS.intersection(df.columns))
    if log_cols:
        df = df.dropna(subset=log_cols, how="all")
    return df
