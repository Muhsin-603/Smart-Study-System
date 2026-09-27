"""
Machine Learning Prediction Module
Serves inference for Final Marks (Linear Regression) and Pass/Fail (Decision Tree).
"""

import numpy as np
import pandas as pd
from ml.preprocessing import FEATURE_COLUMNS, clamp_marks


def predict_final_marks(model, previous_marks: float, internal_marks: float, attendance: float, study_hours: float) -> float:
    """
    Predict final marks using trained Linear Regression model.
    Output is clamped strictly between 0 and 40.
    """
    df_input = pd.DataFrame([{
        "previous_marks": float(previous_marks),
        "internal_marks": float(internal_marks),
        "attendance": float(attendance),
        "study_hours": float(study_hours)
    }])[FEATURE_COLUMNS]

    raw_pred = model.predict(df_input)[0]
    clamped_pred = float(clamp_marks(np.array([raw_pred]))[0])
    return round(clamped_pred, 1)


def predict_pass_fail(model, previous_marks: float, internal_marks: float, attendance: float, study_hours: float) -> str:
    """
    Predict Pass/Fail using trained Decision Tree classifier.
    Returns 'PASS' or 'FAIL'.
    """
    df_input = pd.DataFrame([{
        "previous_marks": float(previous_marks),
        "internal_marks": float(internal_marks),
        "attendance": float(attendance),
        "study_hours": float(study_hours)
    }])[FEATURE_COLUMNS]

    pred_code = int(model.predict(df_input)[0])
    return "PASS" if pred_code == 1 else "FAIL"


def batch_predict_subject_records(reg_model, clf_model, subject_records: list) -> list:
    """
    Enrich an array of subject dictionaries with predictions.
    Each item in subject_records is expected to have:
    - subject: str
    - previous_marks: float
    - internal_marks: float
    - attendance: float
    - study_hours: float
    """
    enriched = []
    for rec in subject_records:
        rec_copy = dict(rec)
        p_marks = rec.get("previous_marks", 0.0)
        i_marks = rec.get("internal_marks", 0.0)
        att = rec.get("attendance", 0.0)
        hours = rec.get("study_hours", 0.0)

        pred_final = predict_final_marks(reg_model, p_marks, i_marks, att, hours)
        pred_pf = predict_pass_fail(clf_model, p_marks, i_marks, att, hours)

        rec_copy["predicted_marks"] = pred_final
        rec_copy["predicted_pass_fail"] = pred_pf
        enriched.append(rec_copy)

    return enriched
