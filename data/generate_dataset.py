"""
Synthetic Dataset Generator for Smart Study Recommendation System
Generates realistic academic records for college students across core and elective subjects.
NOTE: This dataset is synthetically generated for educational demonstration and does not represent real student data.
"""

import os
import numpy as np
import pandas as pd

CORE_SUBJECTS = [
    "Computer Networks",
    "Machine Learning",
    "Design and Analysis of Algorithms (DAA)",
    "Microcontrollers (MC)"
]

ELECTIVE_SUBJECTS = [
    "Software Project Management",
    "Artificial Intelligence"
]

ALL_SUBJECTS = CORE_SUBJECTS + ELECTIVE_SUBJECTS
PASSING_THRESHOLD = 16  # Passing marks out of 40 (40%)


def generate_synthetic_data(num_students=300, random_state=42):
    """
    Generate synthetic student records with realistic relationships:
    - Internal marks strongly correlate with final marks
    - Previous marks have moderate positive correlation
    - Attendance and study hours positively affect marks
    - Controlled noise is added to avoid artificial perfection
    """
    np.random.seed(random_state)
    records = []

    for i in range(1, num_students + 1):
        student_id = f"STU{1000 + i}"
        
        # Student overall aptitude profile (base capability factor between 0.35 and 0.95)
        aptitude = np.random.beta(a=5, b=3)  # natural bell-like distribution skewed towards passing
        
        # Pick one elective
        elective = np.random.choice(ELECTIVE_SUBJECTS)
        student_subjects = CORE_SUBJECTS + [elective]

        for subject in student_subjects:
            # Subject specific variance (some subjects might be slightly harder for the student)
            subject_affinity = np.clip(np.random.normal(0, 0.08), -0.2, 0.2)
            student_eff_apt = np.clip(aptitude + subject_affinity, 0.15, 0.98)

            # Attendance: correlated with student engagement (55% to 100%)
            attendance = float(np.clip(np.random.normal(student_eff_apt * 85 + 10, 8), 50.0, 100.0))

            # Study hours per day: 0.5 to 5.0 hours
            study_hours = float(np.clip(np.random.normal(student_eff_apt * 3.2 + 0.8, 0.6), 0.5, 5.0))

            # Previous Marks (out of 40)
            prev_marks = float(np.clip(np.random.normal(student_eff_apt * 38, 4.0), 4.0, 40.0))

            # Internal Marks (out of 40): influenced by attendance, study hours, and base marks
            internal_factor = (
                0.50 * (prev_marks / 40.0) +
                0.25 * (attendance / 100.0) +
                0.25 * (study_hours / 4.0)
            )
            internal_marks = float(np.clip(
                np.random.normal(internal_factor * 38.0, 2.5),
                2.0, 40.0
            ))

            # Final Marks (out of 40): strong reliance on internal marks and study habits + realistic noise
            final_factor = (
                0.45 * (internal_marks / 40.0) +
                0.25 * (prev_marks / 40.0) +
                0.15 * (attendance / 100.0) +
                0.15 * (study_hours / 4.0)
            )
            noise = np.random.normal(0, 2.0)
            final_marks = float(np.clip(final_factor * 40.0 + noise, 0.0, 40.0))

            # Pass/Fail label based on passing threshold of 16/40
            pass_fail = 1 if final_marks >= PASSING_THRESHOLD else 0

            records.append({
                "student_id": student_id,
                "subject": subject,
                "previous_marks": round(prev_marks, 1),
                "internal_marks": round(internal_marks, 1),
                "attendance": round(attendance, 1),
                "study_hours": round(study_hours, 1),
                "final_marks": round(final_marks, 1),
                "pass_fail": pass_fail
            })

    df = pd.DataFrame(records)
    return df


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, "student_dataset.csv")

    df = generate_synthetic_data(num_students=300, random_state=42)
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} synthetic student-subject records.")
    print(f"Saved dataset to: {output_path}")
    print(f"Pass rate: {(df['pass_fail'].mean() * 100):.1f}%")
    print(f"Average final marks: {df['final_marks'].mean():.2f} / 40")
