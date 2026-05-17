import joblib
import pandas as pd
import os
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# ==============================
# PATH SETUP
# ==============================

current_dir = os.path.dirname(__file__)

project_root = os.path.abspath(
    os.path.join(current_dir, "..")
)

# ==============================
# LOAD MODELS
# ==============================

model = joblib.load(
    os.path.join(
        project_root,
        "models",
        "model.pkl"
    )
)

scaler = joblib.load(
    os.path.join(
        project_root,
        "models",
        "scaler.pkl"
    )
)

encoder = joblib.load(
    os.path.join(
        project_root,
        "models",
        "label_encoder.pkl"
    )
)

feature_names = joblib.load(
    os.path.join(
        project_root,
        "models",
        "feature_names.pkl"
    )
)

# ==============================
# REMOVE UNWANTED FEATURES
# ==============================

REMOVE_COLUMNS = [

    "Flow ID",

    "Source IP",

    "Destination IP",

    "Timestamp",

    "Label"
]

# ==============================
# PREDICTION FUNCTION
# ==============================

def predict(data):

    try:

        # Convert input to dataframe
        df = pd.DataFrame([data])

        # Remove unnecessary columns
        for col in REMOVE_COLUMNS:

            if col in df.columns:

                df.drop(
                    col,
                    axis=1,
                    inplace=True
                )

        # Keep only numeric features
        df = df.select_dtypes(
            include=[np.number]
        )

        # Replace infinity values
        df.replace(
            [np.inf, -np.inf],
            np.nan,
            inplace=True
        )

        # Fill NaN values
        df.fillna(
            0,
            inplace=True
        )

        # Add missing columns
        for col in feature_names:

            if col not in df.columns:

                df[col] = 0

        # Remove unknown extra columns
        df = df[
            feature_names
        ]

        # Scale features
        scaled = scaler.transform(df)

        # Predict
        pred = model.predict(
            scaled
        )

        # Decode label
        label = encoder.inverse_transform(
            pred
        )

        return label[0]

    except Exception as e:

        print(
            "Prediction Error:",
            e
        )

        return "UNKNOWN"