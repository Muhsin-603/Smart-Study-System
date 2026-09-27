"""
Rule-Based Recommendation Engine for Smart Study Recommendation System
Follows the Design.md specifications:
- Terminology: "Needs attention" (<25), "Improving" (25-30), "On track" (31-40)
- Academic Standing: "Needs attention", "Moderate", "On track"
- Daily Study Target heuristics
- Transparent "Why this matters" explainability
"""

from typing import List, Dict, Any

# Internal priority keys to student-friendly display labels
PRIORITY_DISPLAY = {
    "High Priority": "Needs attention",
    "Medium Priority": "Improving",
    "Maintain": "On track"
}


def get_subject_priority(current_marks: float) -> str:
    """
    Determine priority category based on marks (out of 40):
    0-24   -> High Priority ("Needs attention")
    25-30  -> Medium Priority ("Improving")
    31-40  -> Maintain ("On track")
    """
    if current_marks < 25.0:
        return "High Priority"
    elif current_marks <= 30.0:
        return "Medium Priority"
    else:
        return "Maintain"


def generate_subject_recommendations(subject_rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate tailored, concise rule-based recommendations for a subject
    with human-readable reasons following Section 21 & 50 of Design.md.
    """
    subject_name = subject_rec.get("subject", "Unknown Subject")
    current_marks = float(subject_rec.get("internal_marks", 0.0))
    prev_marks = float(subject_rec.get("previous_marks", 0.0))
    attendance = float(subject_rec.get("attendance", 0.0))
    study_hours = float(subject_rec.get("study_hours", 0.0))
    predicted_marks = float(subject_rec.get("predicted_marks", current_marks))
    predicted_pf = subject_rec.get("predicted_pass_fail", "PASS")

    priority_internal = get_subject_priority(current_marks)
    display_status = PRIORITY_DISPLAY[priority_internal]

    recommendations = []
    reasons = []

    # Priority-based core action
    if priority_internal == "High Priority":
        recommendations.append(f"Dedicate 45 min/day to focused revision on {subject_name}")
        reasons.append(f"Current internal marks ({current_marks:.1f}/40) are below the 25-mark benchmark.")
    elif priority_internal == "Medium Priority":
        recommendations.append(f"Review core concepts for 30 min/day to consolidate progress in {subject_name}")
        reasons.append(f"Current internal marks ({current_marks:.1f}/40) show steady progress but need reinforcement.")
    else:
        recommendations.append(f"Maintain regular study routine (20 min/day) for {subject_name}")
        reasons.append(f"Current internal marks ({current_marks:.1f}/40) are solid and on track.")

    # Attendance check
    if attendance < 80.0:
        recommendations.append(f"Improve attendance from {attendance:.1f}% to at least 80% to avoid missing key lectures")
        reasons.append(f"Attendance is currently {attendance:.1f}%, below the required 80% threshold.")

    # Study hours check
    if study_hours < 2.0:
        recommendations.append(f"Increase daily study time for this subject toward 2.0 hours/day")
        reasons.append(f"Current study time ({study_hours:.1f} hrs/day) is below the recommended 2.0 hrs/day baseline.")

    # Analytical vs Theory guidance
    analytical_subjects = ["Machine Learning", "Design and Analysis of Algorithms (DAA)", "Microcontrollers (MC)"]
    if current_marks < 28.0:
        if any(analytic in subject_name for analytic in analytical_subjects):
            recommendations.append(f"Practice algorithmic problem sets and circuit diagrams regularly")
            reasons.append("Applied problem-solving is critical for algorithmic and hardware courses.")
        else:
            recommendations.append(f"Summarize key definitions and conceptual frameworks weekly")
            reasons.append("Structured concept summaries strengthen retention in theoretical subjects.")

    # Pass/Fail alert
    if predicted_pf == "FAIL" or predicted_marks < 16.0:
        recommendations.append("Connect with faculty or a study group for targeted tutoring before semester finals")
        reasons.append(f"Performance outlook indicates potential risk of falling below the 16/40 pass mark.")

    return {
        "subject": subject_name,
        "priority_internal": priority_internal,
        "display_status": display_status,
        "current_marks": current_marks,
        "predicted_marks": predicted_marks,
        "predicted_pass_fail": predicted_pf,
        "attendance": attendance,
        "study_hours": study_hours,
        "recommendations": recommendations,
        "reasons": reasons
    }


def calculate_recommended_study_time(subject_analysis_list: List[Dict[str, Any]]) -> float:
    """
    Recommended daily study time heuristic (Design.md Section 62):
    2.0 hrs/day -> All subjects on track
    2.5 hrs/day -> At least one improving subject
    3.0 hrs/day -> One subject needs attention
    3.5 hrs/day -> Two or more subjects need attention
    """
    needs_att_count = sum(1 for s in subject_analysis_list if s["priority_internal"] == "High Priority")
    improving_count = sum(1 for s in subject_analysis_list if s["priority_internal"] == "Medium Priority")

    if needs_att_count >= 2:
        return 3.5
    elif needs_att_count == 1:
        return 3.0
    elif improving_count >= 1:
        return 2.5
    else:
        return 2.0


def sort_subject_priority(subject_analysis_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort subjects by urgency:
    Needs attention (High) -> Improving (Medium) -> On track (Maintain)
    Within same category, lower marks first.
    """
    priority_order_map = {
        "High Priority": 0,
        "Medium Priority": 1,
        "Maintain": 2
    }
    return sorted(
        subject_analysis_list,
        key=lambda s: (priority_order_map.get(s["priority_internal"], 3), s["current_marks"])
    )


def determine_academic_risk(subject_analysis_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Determine Academic Standing (Design.md Section 14, 63):
    Needs attention (High): 2+ subjects needing attention, or projected average < 16, or any predicted fail
    Moderate (Medium): 1 subject needing attention, or 2+ improving subjects
    On track (Low): Majority on track, no predicted failures
    """
    needs_att_count = sum(1 for s in subject_analysis_list if s["priority_internal"] == "High Priority")
    improving_count = sum(1 for s in subject_analysis_list if s["priority_internal"] == "Medium Priority")
    fail_count = sum(1 for s in subject_analysis_list if s.get("predicted_pass_fail") == "FAIL")

    avg_predicted = sum(s.get("predicted_marks", 0.0) for s in subject_analysis_list) / max(len(subject_analysis_list), 1)

    if needs_att_count >= 2 or avg_predicted < 16.0 or fail_count >= 1:
        standing_label = "Needs attention"
        standing_level = "High"
        if needs_att_count >= 2:
            standing_description = f"{needs_att_count} subjects currently require focused revision."
        elif fail_count >= 1:
            standing_description = "1 or more subjects require immediate support to ensure passing."
        else:
            standing_description = "Projected semester average requires targeted academic focus."
    elif needs_att_count == 1 or improving_count >= 2:
        standing_label = "Moderate"
        standing_level = "Medium"
        if needs_att_count == 1:
            standing_description = "1 subject requires focused attention to get back on track."
        else:
            standing_description = f"{improving_count} subjects are showing steady progress and need consistency."
    else:
        standing_label = "On track"
        standing_level = "Low"
        standing_description = "All subjects are performing well and on track for semester goals."

    return {
        "standing_label": standing_label,
        "standing_level": standing_level,
        "standing_description": standing_description,
        "needs_attention_count": needs_att_count,
        "improving_count": improving_count,
        "fail_count": fail_count,
        "avg_predicted": round(avg_predicted, 1)
    }


def analyze_student_academic_state(subject_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    End-to-end academic analysis for a student.
    """
    analyzed = [generate_subject_recommendations(rec) for rec in subject_records]
    sorted_subjects = sort_subject_priority(analyzed)
    rec_hours = calculate_recommended_study_time(analyzed)
    standing = determine_academic_risk(analyzed)

    return {
        "subject_analysis": analyzed,
        "sorted_subjects": sorted_subjects,
        "recommended_study_hours": rec_hours,
        "academic_standing": standing
    }
