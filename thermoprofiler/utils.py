# thermoprofiler/utils.py
import re
import pandas as pd

def to_multiindex_columns(df, props=("TC","SHC","TD")):
    tuples = []
    for c in df.columns:
        m = re.match(rf"^({'|'.join(props)})_prediction$", c)
        if m:
            tuples.append(("prediction", m.group(1)))
            continue

        m = re.match(rf"^(.*)_({'|'.join(props)})$", c)
        if m:
            tuples.append((m.group(1), m.group(2)))
        else:
            tuples.append((c, ""))

    df2 = df.copy()
    df2.columns = pd.MultiIndex.from_tuples(tuples, names=["metric", "prop"])
    return df2
