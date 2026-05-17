import pandas as pd
import numpy as np
import os
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def preprocess():

    df = pd.read_csv(
        "data/raw/network.csv",
        low_memory=False
    )

    print("Original Shape:", df.shape)

    # Remove spaces from column names
    df.columns = df.columns.str.strip()

    # Remove duplicates
    df.drop_duplicates(inplace=True)

    # Replace infinite values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Remove null rows
    df.dropna(inplace=True)

    print("After Cleaning:", df.shape)

    # Encode target labels
    encoder = LabelEncoder()

    df['Label'] = encoder.fit_transform(df['Label'])

    # Save encoder
    os.makedirs("models", exist_ok=True)

    joblib.dump(
        encoder,
        "models/label_encoder.pkl"
    )

    # Remove non-numeric columns
    non_numeric_columns = [
        'Flow ID',
        'Source IP',
        'Destination IP',
        'Timestamp'
    ]

    for col in non_numeric_columns:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)

    # Features and target
    X = df.drop("Label", axis=1)

    y = df["Label"]

    # Keep only numeric columns
    X = X.select_dtypes(include=[np.number])
    
    # Save feature names
    joblib.dump(
    X.columns.tolist(),
    "models/feature_names.pkl"
)

    print("Feature Shape:", X.shape)

    # Train Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Scaling
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)

    X_test = scaler.transform(X_test)

    # Save scaler
    joblib.dump(
        scaler,
        "models/scaler.pkl"
    )

    # Save processed data
    pd.DataFrame(X_train).to_csv(
        "data/processed/X_train.csv",
        index=False
    )

    pd.DataFrame(X_test).to_csv(
        "data/processed/X_test.csv",
        index=False
    )

    pd.DataFrame(y_train).to_csv(
        "data/processed/y_train.csv",
        index=False
    )

    pd.DataFrame(y_test).to_csv(
        "data/processed/y_test.csv",
        index=False
    )

    print("Preprocessing Completed Successfully")

if __name__ == "__main__":
    preprocess()