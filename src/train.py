import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt

from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

from sklearn.utils.class_weight import compute_sample_weight

# ==============================
# CREATE DIRECTORIES
# ==============================

os.makedirs("models", exist_ok=True)
os.makedirs("logs", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ==============================
# TRAIN FUNCTION
# ==============================

def train():

    print("\nLoading datasets...")

    # Load processed data
    X_train = pd.read_csv(
        "data/processed/X_train.csv"
    )

    X_test = pd.read_csv(
        "data/processed/X_test.csv"
    )

    y_train = pd.read_csv(
        "data/processed/y_train.csv"
    ).values.ravel()

    y_test = pd.read_csv(
        "data/processed/y_test.csv"
    ).values.ravel()

    print(f"\nTraining Samples: {len(X_train)}")
    print(f"Testing Samples: {len(X_test)}")

    # ==============================
    # CLASS BALANCING
    # ==============================

    print("\nCalculating class weights...")

    sample_weights = compute_sample_weight(
        class_weight="balanced",
        y=y_train
    )

    # ==============================
    # XGBOOST MODEL
    # ==============================

    print("\nInitializing XGBoost...")

    xgb_model = XGBClassifier(

        n_estimators=300,

        max_depth=10,

        learning_rate=0.05,

        subsample=0.8,

        colsample_bytree=0.8,

        objective="multi:softmax",

        random_state=42,

        eval_metric="mlogloss",

        tree_method="hist",

        n_jobs=-1
    )

    # ==============================
    # RANDOM FOREST MODEL
    # ==============================

    print("\nInitializing Random Forest...")

    rf_model = RandomForestClassifier(

        n_estimators=200,

        max_depth=20,

        random_state=42,

        n_jobs=-1
    )

    # ==============================
    # ENSEMBLE MODEL
    # ==============================

    ensemble_model = VotingClassifier(

        estimators=[

            ("xgb", xgb_model),

            ("rf", rf_model)
        ],

        voting="hard"
    )

    # ==============================
    # TRAINING
    # ==============================

    print("\nTraining Started...")

    ensemble_model.fit(
        X_train,
        y_train
    )

    print("\nTraining Completed")

    # ==============================
    # PREDICTION
    # ==============================

    print("\nGenerating Predictions...")

    predictions = ensemble_model.predict(
        X_test
    )

    # ==============================
    # EVALUATION
    # ==============================

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print(f"\nAccuracy: {accuracy * 100:.2f}%")

    report = classification_report(
        y_test,
        predictions,
        zero_division=0
    )

    print("\nClassification Report:\n")
    print(report)

    cm = confusion_matrix(
        y_test,
        predictions
    )

    print("\nConfusion Matrix:\n")
    print(cm)

    # ==============================
    # SAVE REPORT
    # ==============================

    with open(
        "reports/classification_report.txt",
        "w"
    ) as f:

        f.write(report)

    # ==============================
    # SAVE CONFUSION MATRIX
    # ==============================

    plt.figure(figsize=(10, 7))

    plt.imshow(cm)

    plt.title("Confusion Matrix")

    plt.colorbar()

    plt.xlabel("Predicted")

    plt.ylabel("Actual")

    plt.savefig(
        "reports/confusion_matrix.png"
    )

    plt.close()

    # ==============================
    # FEATURE IMPORTANCE
    # ==============================

    print("\nGenerating Feature Importance...")

    try:

        trained_xgb = ensemble_model.named_estimators_["xgb"]

        feature_importance = pd.DataFrame({

            "Feature":
                X_train.columns,

            "Importance":
                trained_xgb.feature_importances_
        })

        feature_importance = feature_importance.sort_values(

            by="Importance",

            ascending=False
        )

        # Save CSV
        feature_importance.to_csv(

            "reports/feature_importance.csv",

            index=False
        )

        # Plot
        plt.figure(figsize=(12, 8))

        plt.barh(

            feature_importance["Feature"][:20],

            feature_importance["Importance"][:20]
        )

        plt.xlabel("Importance")

        plt.ylabel("Features")

        plt.title("Top 20 Important Features")

        plt.savefig(
            "reports/feature_importance.png"
        )

        plt.close()

        print("\nFeature Importance Saved")

    except Exception as e:

        print("\nFeature Importance Error:", e)

    # ==============================
    # SAVE MODEL
    # ==============================

    joblib.dump(

        ensemble_model,

        "models/model.pkl"
    )

    print("\nModel Saved Successfully")

    print("\nReports Saved Successfully")

    print("\nProject Training Completed 🚀")

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    train()