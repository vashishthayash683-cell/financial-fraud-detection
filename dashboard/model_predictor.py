import json
from pathlib import Path

import joblib
import pandas as pd


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "models" / "final_fraud_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "models" / "preprocessor.pkl"
METADATA_PATH = BASE_DIR / "models" / "final_model_metadata.json"


# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load(MODEL_PATH)

preprocessor = joblib.load(PREPROCESSOR_PATH)


# =========================================================
# LOAD MODEL METADATA
# =========================================================

threshold = 0.70

if METADATA_PATH.exists():

    try:

        with open(METADATA_PATH, "r") as file:

            metadata = json.load(file)

        if "threshold" in metadata:

            threshold = float(
                metadata["threshold"]
            )

        elif "fraud_threshold" in metadata:

            threshold = float(
                metadata["fraud_threshold"]
            )

    except Exception:

        threshold = 0.70


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_transaction(transaction_data):

    input_df = pd.DataFrame(
        [transaction_data]
    )

    # Apply the exact preprocessing pipeline
    processed_data = preprocessor.transform(
        input_df
    )

    # Fraud probability
    fraud_probability = model.predict_proba(
        processed_data
    )[0][1]

    # Apply selected threshold
    prediction = (
        fraud_probability >= threshold
    )

    if prediction:

        result = "Fraud"

    else:

        result = "Normal"

    return {
        "prediction": result,
        "fraud_probability": fraud_probability,
        "threshold": threshold
    }