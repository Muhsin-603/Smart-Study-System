"""
Rule-Based Recommendation Engine for Smart Study Recommendation System
Provides transparent, explainable recommendations, subject prioritization,
study schedule recommendations, and academic risk classification.
"""

from typing import List, Dict, Any


def get_subject_priority(current_marks: float) -> str:
    """
    Determine priority category based on marks (out of 40):
    0-24   -> High Priority
    25-30  -> Medium Priority
    31-40  -> Maintain
    """
    if current_marks < 25.0:
        return "High Priority"
    elif current_marks <= 30.0:
        return "Medium Priority"
    else:
        return "Maintain"


def generate_subject_recommendations(subject_rec: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate tailored, rule-based recommendations for a single subject
    with full explainability details.
    """
    subject_name = subject_rec.get("subject", "Unknown Subject")
    current_marks = float(subject_rec.get("internal_marks", 0.0))
    prev_marks = float(subject_rec.get("previous_marks", 0.0))
    attendance = float(subject_rec.get("attendance", 0.0))
    study_hours = float(subject_rec.get("study_hours", 0.0))
    predicted_marks = float(subject_rec.get("predicted_marks", current_marks))
    predicted_pf = subject_rec.get("predicted_pass_fail", "PASS")

    priority = get_subject_priority(current_marks)
    recommendations = []
    reasons = []

    # Priority rule
    if priority == "High Priority":
        recommendations.append(f"High Priority: Immediate focus needed on {subject_name}")
        reasons.append(f"Current internal marks ({current_marks:.1f}/40) are in the critical range (< 25/40).")
    elif priority == "Medium Priority":
        recommendations.append(f"Medium Priority: Consistent review needed on {subject_name}")
        reasons.append(f"Current internal marks ({current_marks:.1f}/40) are in the moderate range (25-30/40).")
    else:
        recommendations.append(f"Maintain current routine for {subject_name}")
        reasons.append(f"Current internal marks ({current_marks:.1f}/40) are solid (31-40/40).")

    # Attendance check
    if attendance < 80.0:
        recommendations.append("Improve attendance to at least 80% to avoid missing crucial lectures")
        reasons.append(f"Attendance is {attendance:.1f}%, which is below the mandatory 80% threshold.")

    # Study hours check
    if study_hours < 2.0:
        recommendations.append("Increase daily study time for this subject")
        reasons.append(f"Current study time ({study_hours:.1f}h/day) is below the minimum recommended 2.0 hours/day.")

    # Problem-solving vs Theory guidance
    analytical_subjects = ["Machine Learning", "Design and Analysis of Algorithms (DAA)", "Microcontrollers (MC)"]
    if current_marks < 28.0:
        if any(analytic in subject_name for analytic in analytical_subjects):
            recommendations.append(f"Practice more problems, diagrams, and numerical algorithms for {subject_name}")
            reasons.append("Analytical and algorithmic subjects require hands-on problem-solving practice.")
        else:
            recommendations.append(f"Revise core concepts and theoretical frameworks for {subject_name}")
            reasons.append("Conceptual mastery and regular revision will lift baseline performance.")

    # Failure warning
    if predicted_pf == "FAIL" or predicted_marks < 16.0:
        recommendations.append("Seek faculty or peer mentoring immediately to prevent failing final exams")
        reasons.append(f"Predicted final score is {predicted_marks:.1f}/40 (Passing threshold: 16/40).")

    return {
        "subject": subject_name,
        "priority": priority,
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
    Transparent rule-based daily study time heuristic:
    - No weak subjects: 2.0 hours/day
    - One medium-priority subject (no high): 2.5 hours/day
    - One high-priority subject: 3.0 hours/day
    - Multiple high-priority subjects: 3.5 hours/day
    """
    high_count = sum(1 for s in subject_analysis_list if s["priority"] == "High Priority")
    med_count = sum(1 for s in subject_analysis_list if s["priority"] == "Medium Priority")

    if high_count > 1:
        return 3.5
    elif high_count == 1:
        return 3.0
    elif med_count >= 1:
        return 2.5
    else:
        return 2.0


def sort_subject_priority(subject_analysis_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort subjects strictly by academic priority:
    High Priority -> Medium Priority -> Maintain
    Within same category, lower marks first.
    """
    priority_order_map = {
        "High Priority": 0,
        "Medium Priority": 1,
        "Maintain": 2
    }

    return sorted(
        subject_analysis_list,
        key=lambda s: (priority_order_map.get(s["priority"], 3), s["current_marks"])
    )


def determine_academic_risk(subject_analysis_list: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Determine overall academic risk (HIGH, MEDIUM, LOW) using transparent criteria:
    HIGH:
      - Multiple High Priority subjects, OR
      - Predicted overall score is < 16/40 (40%), OR
      - Any predicted result is FAIL
    MEDIUM:
      - One High Priority subject, OR
      - Multiple Medium Priority subjects
    LOW:
      - Most subjects in Maintain category, no FAIL predicted, overall score is solid
    """
    high_count = sum(1 for s in subject_analysis_list if s["priority"] == "High Priority")
    med_count = sum(1 for s in subject_analysis_list if s["priority"] == "Medium Priority")
    fail_count = sum(1 for s in subject_analysis_list if s.get("predicted_pass_fail") == "FAIL")

    avg_predicted = sum(s.get("predicted_marks", 0.0) for s in subject_analysis_list) / max(len(subject_analysis_list), 1)

    if high_count >= 2 or avg_predicted < 16.0 or fail_count >= 1:
        risk_level = "HIGH"
        risk_description = "High academic risk detected due to multiple weak subjects, low projected score, or risk of failing one or more courses."
        badge_color = "red"
    elif high_count == 1 or med_count >= 2:
        risk_level = "MEDIUM"
        risk_description = "Moderate risk detected. Targeted effort on weak areas will restore comfortable academic standing."
        badge_color = "orange"
    else:
        risk_level = "LOW"
        risk_description = "Low academic risk. Overall performance is consistent and on track for successful completion."
        badge_color = "green"

    return {
        "risk_level": risk_level,
        "risk_description": risk_description,
        "badge_color": badge_color,
        "high_priority_count": high_count,
        "medium_priority_count": med_count,
        "fail_count": fail_count,
        "avg_predicted": round(avg_predicted, 1)
    }


def analyze_student_academic_state(subject_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Perform full end-to-end recommendation analysis for a student.
    Returns:
    - subject_analysis: detailed list of subjects with priority, recommendations, and reasons
    - sorted_subjects: prioritized subject list
    - recommended_study_hours: daily recommended hours
    - risk_assessment: risk level and summary
    """
    analyzed_subjects = [generate_subject_recommendations(rec) for rec in subject_records]
    sorted_subjects = sort_subject_priority(analyzed_subjects)
    rec_study_time = calculate_recommended_study_time(analyzed_subjects)
    risk_info = determine_academic_risk(analyzed_subjects)

    return {
        "subject_analysis": analyzed_subjects,
        "sorted_subjects": sorted_subjects,
        "recommended_study_hours": rec_study_time,
        "risk_assessment": risk_info
    }
