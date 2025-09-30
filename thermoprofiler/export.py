import os
import pandas as pd
import lasio
from lasio import CurveItem

def export_to_txt(df: pd.DataFrame, filename: str, sep: str = ","):
    """
    Export predictions to a TXT/CSV file (tab-delimited by default).
    """
    try:
        df.to_csv(filename, sep=sep, index=False)
        print(f"Predictions exported to TXT: {os.path.abspath(filename)}")
    except Exception as e:
        print(f"TXT export failed: {e}")
        raise


def export_to_las(df: pd.DataFrame, filename: str, depth_col="Depth"):
    """
    Export DataFrame to LAS file.
    """
    try:
        las = lasio.LASFile()

        if depth_col not in df.columns:
            raise ValueError(f"{depth_col} not found in DataFrame")

        # Ensure depth is numeric
        depth = pd.to_numeric(df[depth_col], errors="coerce")
        if depth.isna().all():
            raise ValueError("Depth column could not be converted to numeric values")

        # Add depth curve
        las.curves.append(CurveItem(mnemonic=depth_col, data=depth.values, unit="m", descr="Depth"))

        # Add only numeric columns
        for col in df.columns:
            if col == depth_col:
                continue
            values = pd.to_numeric(df[col], errors="coerce")
            if values.notna().any():
                las.curves.append(CurveItem(mnemonic=col, data=values.values, unit="", descr=col))

        # Write LAS file
        las.write(filename, version=2.0, wrap=False)
        print(f"LAS file saved: {os.path.abspath(filename)}")

    except Exception as e:
        print(f"LAS export failed: {e}")
        raise
