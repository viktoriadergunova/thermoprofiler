

# ThermoProfiler

ThermoProfiler is a Python package for predicting **thermal rock properties** from well logs using machine learning models.  
It supports multiple model types (`XGBOOST`, `ADABOOST`, `RF`, `LINEAR`)
## Features
- Predicts:
  - Thermal Conductivity (`TC`)  
  - Specific Heat Capacity (`SHC`)  
  - Thermal Diffusivity (`TD`)  
- Dual prediction strategy:
  - **MAPE-optimal** → best available log combination (lowest uncertainty).  
  - **Raw logs** → exactly matches the available logs.  
- Provides **uncertainty estimates** (MAPE %) for each prediction.  


---

## Installation
Clone and install dependencies:

```bash
git clone https://github.com/yourusername/thermoprofiler.git
cd thermoprofiler
pip install -r requirements.txt
```

Requirements:
- `numpy==1.25.2`  
- `pandas>=1.5.3`  
- `scikit-learn==1.2.1`  
- `joblib>=1.2.0`  

---

## Usage Example

```python
import pandas as pd
from thermoprofiler.preprocessing import clean_log_dataframe
from thermoprofiler.prediction import predict_all_properties

# Load your well log dataset
df = pd.read_csv("input_logs.csv")

# Preprocess (standardize column names, clean missing values)
df = clean_log_dataframe(df)

# Run predictions
results = predict_all_properties(df, model_type="XGBOOST")

print(results.head())
```

---

## Output Columns

The returned `DataFrame` contains the following new columns for each property (`TC`, `SHC`, `TD`):

- `model_number_{prop}` → MAPE-optimal model number used.  
- `uncertainty_{prop}` → Uncertainty (MAPE %) for the optimal model.  
- `model_number_raw_{prop}` → Model number reflecting the actual available logs.  
- `{prop}_prediction` → Prediction using the MAPE-optimal model.  
- `{prop}_prediction_raw` → Prediction using the raw-log model.  

---

## Example Output (abbreviated)

| Depth | Rock_type | model_number_TC | uncertainty_TC | model_number_raw_TC | TC_prediction | TC_prediction_raw |
|-------|-----------|-----------------|----------------|----------------------|---------------|-------------------|
| 1000  | 3 (Clastics) | 15 | 7.7 | 11 | 2.15 | 2.05 |
| 1005  | 2 (Carbonates) | 12 | 5.3 | 5 | 2.42 | 2.38 |

---

## Input Requirements
- **Logs accepted**: `RHOB`, `PHIN`, `VSH`, `VP`.  
- Rock type column required:  
  - `1` = Evaporites  
  - `2` = Carbonates  
  - `3` = Clastics  
- Missing logs handled automatically → falls back to the available combination.  

---

## Model Files
- Models are stored in `compiled_models/{ROCK_TYPE}/{MODEL_TYPE}/{PROPERTY}/`.  
- Format: `joblib` files.  
- Model numbers (1–15) correspond to predefined log combinations (see `config.py`).  

### Log Combination Reference

| Model # | Logs Used                     |
|---------|-------------------------------|
| 1       | `['RHOB']`                    |
| 2       | `['PHIN']`                    |
| 3       | `['VSH']`                     |
| 4       | `['VP']`                      |
| 5       | `['RHOB', 'PHIN']`            |
| 6       | `['RHOB', 'VSH']`             |
| 7       | `['RHOB', 'VP']`              |
| 8       | `['PHIN', 'VSH']`             |
| 9       | `['PHIN', 'VP']`              |
| 10      | `['VSH', 'VP']`               |
| 11      | `['RHOB', 'PHIN', 'VSH']`     |
| 12      | `['RHOB', 'PHIN', 'VP']`      |
| 13      | `['RHOB', 'VSH', 'VP']`       |
| 14      | `['PHIN', 'VSH', 'VP']`       |
| 15      | `['RHOB', 'PHIN', 'VSH', 'VP']` |

---

## References
If you use this package, please cite:  
-  https://doi.org/10.1093/gji/ggaf260
-  

---
