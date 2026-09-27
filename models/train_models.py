"""
Model Training & Continual Learning Pipeline
Trains Linear Regression (Final Marks) and Decision Tree (Pass/Fail)
Saves models using joblib and records exact test evaluation metrics in JSON format.
"""

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import json
import joblib
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier

from ml.preprocessing import prepare_datasets, clamp_marks, FEATURE_COLUMNS
from ml.evaluation import evaluate_regression, evaluate_classification
from database.mongodb import get_verified_records_for_retraining


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "student_dataset.csv")
MODELS_DIR = os.path.join(BASE_DIR, "models")
REGRESSION_MODEL_PATH = os.path.join(MODELS_DIR, "linear_regression.pkl")
CLASSIFIER_MODEL_PATH = os.path.join(MODELS_DIR, "decision_tree.pkl")
METRICS_PATH = os.path.join(MODELS_DIR, "model_metrics.json")


def load_combined_dataset():
    """
    Load base synthetic dataset and append verified student records
    from MongoDB if available (continual learning feedback loop).
    """
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Base dataset not found at {DATA_PATH}. Run data/generate_dataset.py first.")

    df = pd.read_csv(DATA_PATH)
    initial_count = len(df)

    # Check MongoDB for newly completed student records
    verified_records = get_verified_records_for_retraining()
    new_rows = []
    for r in verified_records:
        try:
            prev = float(r.get("previous_marks", 0))
            internal = float(r.get("internal_marks", 0))
            att = float(r.get("attendance", 0))
            hours = float(r.get("study_hours", 0))
            final_m = float(r.get("actual_final_marks", 0))
            pf = 1 if final_m >= 16.0 else 0

            new_rows.append({
                "student_id": r.get("student_id", "LIVE_USER"),
                "subject": r.get("subject", "General"),
                "previous_marks": prev,
                "internal_marks": internal,
                "attendance": att,
                "study_hours": hours,
                "final_marks": final_m,
                "pass_fail": pf
            })
        except Exception:
            continue

    if new_rows:
        df_new = pd.DataFrame(new_rows)
        df = pd.concat([df, df_new], ignore_index=True)
        print(f"Incorporated {len(new_rows)} verified student records into training dataset.")

    return df, initial_count, len(new_rows)


def train_and_evaluate_models():
    """
    Train Linear Regression and Decision Tree models on 80/20 train-test split.
    Save serialized models and evaluation metrics.
    """
    os.makedirs(MODELS_DIR, exist_ok=True)
    df, initial_count, verified_count = load_combined_dataset()

    data_splits = prepare_datasets(df, test_size=0.2, random_state=42)
    X_train = data_splits["X_train"]
    X_test = data_splits["X_test"]
    y_reg_train = data_splits["y_reg_train"]
    y_reg_test = data_splits["y_reg_test"]
    y_clf_train = data_splits["y_clf_train"]
    y_clf_test = data_splits["y_clf_test"]

    # 1. Model 1: Linear Regression (Final Marks Prediction)
    reg_model = LinearRegression()
    reg_model.fit(X_train, y_reg_train)

    y_reg_pred_raw = reg_model.predict(X_test)
    y_reg_pred = clamp_marks(y_reg_pred_raw)
    reg_metrics = evaluate_regression(y_reg_test, y_reg_pred)

    # 2. Model 2: Decision Tree Classifier (Pass / Fail Prediction)
    clf_model = DecisionTreeClassifier(max_depth=5, min_samples_leaf=5, random_state=42)
    clf_model.fit(X_train, y_clf_train)

    y_clf_pred = clf_model.predict(X_test)
    clf_metrics = evaluate_classification(y_clf_test, y_clf_pred)

    # Save models
    joblib.dump(reg_model, REGRESSION_MODEL_PATH)
    joblib.dump(clf_model, CLASSIFIER_MODEL_PATH)

    # Prepare metrics report
    metrics_report = {
        "dataset_summary": {
            "total_records": len(df),
            "base_synthetic_records": initial_count,
            "live_verified_records": verified_count,
            "train_records": len(X_train),
            "test_records": len(X_test),
            "passing_threshold": 16.0
        },
        "linear_regression": {
            "metrics": reg_metrics,
            "coefficients": dict(zip(FEATURE_COLUMNS, [round(float(c), 4) for c in reg_model.coef_])),
            "intercept": round(float(reg_model.intercept_), 4)
        },
        "decision_tree": {
            "metrics": clf_metrics,
            "feature_importances": dict(zip(FEATURE_COLUMNS, [round(float(fi), 4) for fi in clf_model.feature_importances_]))
        }
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics_report, f, indent=4)

    print("\n--- Model Training Completed Successfully ---")
    print(f"Linear Regression -> MAE: {reg_metrics['mae']}, MSE: {reg_metrics['mse']}, R²: {reg_metrics['r2']}")
    print(f"Decision Tree     -> Accuracy: {clf_metrics['accuracy']}, Precision: {clf_metrics['precision']}, Recall: {clf_metrics['recall']}, F1: {clf_metrics['f1_score']}")
    print(f"Saved models to: {REGRESSION_MODEL_PATH} and {CLASSIFIER_MODEL_PATH}")

    return metrics_report


if __name__ == "__main__":
    train_and_evaluate_models()
