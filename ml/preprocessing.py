"""
Machine Learning Preprocessing Module
Extracts feature matrices, performs train-test splitting, and provides value sanitization.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = ["previous_marks", "internal_marks", "attendance", "study_hours"]
REGRESSION_TARGET = "final_marks"
CLASSIFICATION_TARGET = "pass_fail"


def get_feature_matrix(df: pd.DataFrame):
    """Extract features dataframe ensuring correct data types."""
    return df[FEATURE_COLUMNS].astype(float)


def prepare_datasets(df: pd.DataFrame, test_size=0.2, random_state=42):
    """
    Split the dataset into 80% train and 20% test sets
    with reproducible random state.
    """
    X = get_feature_matrix(df)
    y_reg = df[REGRESSION_TARGET].astype(float)
    y_clf = df[CLASSIFICATION_TARGET].astype(int)

    X_train, X_test, y_reg_train, y_reg_test = train_test_split(
        X, y_reg, test_size=test_size, random_state=random_state
    )

    _, _, y_clf_train, y_clf_test = train_test_split(
        X, y_clf, test_size=test_size, random_state=random_state
    )

    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_reg_train": y_reg_train,
        "y_reg_test": y_reg_test,
        "y_clf_train": y_clf_train,
        "y_clf_test": y_clf_test,
    }


def clamp_marks(marks_array, min_val=0.0, max_val=40.0):
    """Clamp predicted marks strictly to the valid 0-40 range."""
    return np.clip(marks_array, min_val, max_val)
