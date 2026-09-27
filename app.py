"""
Smart Study Recommendation System
Main Streamlit Application featuring Student Dashboard & Admin Dashboard.
"""

import os
import sys
import json
import joblib
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Ensure root directory is on sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.mongodb import (
    check_connection,
    authenticate_student,
    register_student,
    get_student_profile,
    update_student_profile,
    get_student_academic_records,
    save_student_academic_records,
    get_all_students_summary,
    seed_demo_students_if_empty
)
from ml.prediction import batch_predict_subject_records
from recommendations.recommendation_engine import analyze_student_academic_state
from utils.helpers import (
    validate_marks,
    validate_attendance,
    validate_study_hours,
    plot_subject_marks_bar,
    plot_attendance_vs_marks_scatter,
    plot_actual_vs_predicted_marks,
    plot_weak_subjects_priority
)
from data.generate_dataset import CORE_SUBJECTS, ELECTIVE_SUBJECTS

# Page configuration
st.set_page_config(
    page_title="Smart Study Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished academic appearance
st.markdown("""
<style>
    /* Metric card styles */
    .metric-card {
        background: rgba(255, 255, 255, 0.04);
        border-radius: 10px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.12);
        border: 1px solid rgba(148, 163, 184, 0.25);
        margin-bottom: 12px;
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .badge-high {
        background-color: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.4);
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-medium {
        background-color: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
        border: 1px solid rgba(245, 158, 11, 0.4);
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .badge-low, .badge-maintain {
        background-color: rgba(16, 185, 129, 0.2);
        color: #10B981;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .explain-card {
        background-color: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.25);
        border-left: 4px solid #3B82F6;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin-bottom: 14px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_ml_models():
    """Load serialized ML models and metrics."""
    reg_path = os.path.join(BASE_DIR, "models", "linear_regression.pkl")
    clf_path = os.path.join(BASE_DIR, "models", "decision_tree.pkl")
    metrics_path = os.path.join(BASE_DIR, "models", "model_metrics.json")

    reg_model = joblib.load(reg_path) if os.path.exists(reg_path) else None
    clf_model = joblib.load(clf_path) if os.path.exists(clf_path) else None

    metrics = {}
    if os.path.exists(metrics_path):
        with open(metrics_path, "r") as f:
            metrics = json.load(f)

    return reg_model, clf_model, metrics


@st.cache_data
def load_reference_dataset():
    """Load reference dataset for visualization benchmarks."""
    data_path = os.path.join(BASE_DIR, "data", "student_dataset.csv")
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return pd.DataFrame()


# Session state initialization
if "logged_in_student" not in st.session_state:
    st.session_state.logged_in_student = None
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


# Sidebar Navigation
st.sidebar.title("🎓 Smart Study System")
st.sidebar.markdown("**Machine Learning Recommendation Platform**")

db_ok, db_msg = check_connection()
if db_ok:
    st.sidebar.success("🟢 MongoDB Connected")
    seed_demo_students_if_empty()
else:
    st.sidebar.error("🔴 MongoDB Offline")
    st.sidebar.caption(db_msg)

role_option = st.sidebar.radio(
    "Choose Portal:",
    ["Student Dashboard", "Admin Dashboard"],
    index=0
)

reg_model, clf_model, model_metrics = load_ml_models()
ref_df = load_reference_dataset()

if reg_model is None or clf_model is None:
    st.sidebar.warning("⚠️ ML models not loaded. Retrain in Admin.")


# ==============================================================================
# 1. STUDENT DASHBOARD
# ==============================================================================
if role_option == "Student Dashboard":

    if not db_ok:
        st.error("🚨 Database Connection Required")
        st.markdown(f"""
        The system could not connect to MongoDB Atlas:
        `{db_msg}`
        
        Please check your `.env` configuration file and verify your credentials and network IP access.
        """)
        st.stop()

    if not st.session_state.logged_in_student:
        # Authentication Screen (Login / Sign Up)
        st.markdown("## 🔐 Student Access Portal")
        st.markdown("Log in or create a student account to view personalized study analytics and recommendations.")

        auth_tab1, auth_tab2 = st.tabs(["Student Login", "New Student Registration"])

        with auth_tab1:
            st.markdown("#### Enter Your Credentials")
            with st.form("login_form"):
                login_id = st.text_input("Student ID (e.g., STU101)", placeholder="STU101").strip().upper()
                login_pw = st.text_input("Password", type="password")
                login_submit = st.form_submit_button("Log In", use_container_width=True)

            if login_submit:
                if not login_id or not login_pw:
                    st.error("Please enter both Student ID and Password.")
                else:
                    success, student, msg = authenticate_student(login_id, login_pw)
                    if success:
                        st.session_state.logged_in_student = student
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

            st.markdown("---")
            st.info("💡 **Quick Demo Accounts:** Use `STU101` or `STU102` with password `password123`")

        with auth_tab2:
            st.markdown("#### Register New Account")
            with st.form("signup_form"):
                new_id = st.text_input("Choose Student ID (e.g., STU105)").strip().upper()
                new_name = st.text_input("Full Name")
                new_elective = st.selectbox("Select Elective Subject", ELECTIVE_SUBJECTS)
                new_pw = st.text_input("Choose Password", type="password")
                signup_submit = st.form_submit_button("Register Account", use_container_width=True)

            if signup_submit:
                if not new_id or not new_name or not new_pw:
                    st.error("All fields are mandatory.")
                else:
                    success, msg = register_student(new_id, new_name, new_pw, new_elective)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)

    else:
        # Logged-in Student Experience
        student = st.session_state.logged_in_student
        student_id = student["student_id"]
        
        # Refresh student profile and records
        profile = get_student_profile(student_id) or student
        records = get_student_academic_records(student_id)

        # Header bar
        top_col1, top_col2 = st.columns([3, 1])
        with top_col1:
            st.title(f"Welcome, {profile.get('name', 'Student')}!")
            st.caption(f"Student ID: **{student_id}** | Elective: **{profile.get('elective', 'N/A')}**")
        with top_col2:
            st.write("")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in_student = None
                st.rerun()

        # Run predictions & recommendations
        enriched_records = batch_predict_subject_records(reg_model, clf_model, records) if (reg_model and clf_model) else records
        analysis_result = analyze_student_academic_state(enriched_records)
        risk = analysis_result["risk_assessment"]

        # Student Tabs
        dash_tab, subject_tab, rec_tab, profile_tab = st.tabs([
            "📊 Dashboard Overview",
            "📚 Subject Performance & Charts",
            "💡 Personalized Recommendations",
            "✏️ Update Academic Marks"
        ])

        # -----------------------------
        # Tab 1: Dashboard Overview
        # -----------------------------
        with dash_tab:
            st.markdown("### Academic Summary")

            avg_internal = sum(r.get("internal_marks", 0.0) for r in enriched_records) / max(len(enriched_records), 1)
            avg_predicted = risk["avg_predicted"]
            avg_attendance = sum(r.get("attendance", 0.0) for r in enriched_records) / max(len(enriched_records), 1)
            overall_pass = "FAIL" if risk["fail_count"] > 0 or avg_predicted < 16.0 else "PASS"

            # 4 KPI Cards
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Current Average Score</div>
                    <div class="metric-value">{avg_internal:.1f} <span style="font-size:1rem;color:#64748B;">/ 40</span></div>
                    <small style="color:#64748B;">Internal marks average</small>
                </div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Predicted Final Score</div>
                    <div class="metric-value" style="color:#3B82F6;">{avg_predicted:.1f} <span style="font-size:1rem;color:#64748B;">/ 40</span></div>
                    <small style="color:#64748B;">Linear Regression forecast</small>
                </div>
                """, unsafe_allow_html=True)
            with c3:
                pf_color = "#16A34A" if overall_pass == "PASS" else "#DC2626"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Predicted Status</div>
                    <div class="metric-value" style="color:{pf_color};">{overall_pass}</div>
                    <small style="color:#64748B;">Passing benchmark: 16/40</small>
                </div>
                """, unsafe_allow_html=True)
            with c4:
                badge_class = f"badge-{risk['risk_level'].lower()}"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Academic Risk Level</div>
                    <div class="metric-value"><span class="{badge_class}">{risk['risk_level']}</span></div>
                    <small style="color:#64748B;">{risk['high_priority_count']} High Priority areas</small>
                </div>
                """, unsafe_allow_html=True)

            st.info(f"📌 **Risk Assessment:** {risk['risk_description']}")

            # Study hours recommendation highlight
            st.markdown(f"""
            <div style="background:rgba(59, 130, 246, 0.12); border:1px solid rgba(59, 130, 246, 0.35); border-radius:8px; padding:14px 18px; margin-top:8px;">
                <h4 style="margin:0; color:#60A5FA;">⏱️ Recommended Daily Study Target: <b>{analysis_result['recommended_study_hours']} hours/day</b></h4>
                <p style="margin:4px 0 0 0; color:#93C5FD; font-size:0.9rem;">
                    Calculated based on your {risk['high_priority_count']} High Priority and {risk['medium_priority_count']} Medium Priority subjects.
                </p>
            </div>
            """, unsafe_allow_html=True)

        # -----------------------------
        # Tab 2: Subject Performance & Charts
        # -----------------------------
        with subject_tab:
            st.markdown("### Subject Performance Table")

            table_rows = []
            for item in analysis_result["sorted_subjects"]:
                p = item["priority"]
                badge_str = f"🔴 {p}" if p == "High Priority" else (f"🟡 {p}" if p == "Medium Priority" else f"🟢 {p}")
                table_rows.append({
                    "Subject": item["subject"],
                    "Current Marks": f"{item['current_marks']:.1f} / 40",
                    "Predicted Marks": f"{item['predicted_marks']:.1f} / 40",
                    "Predicted Result": item["predicted_pass_fail"],
                    "Attendance": f"{item['attendance']:.1f}%",
                    "Study Hours": f"{item['study_hours']:.1f} h/day",
                    "Priority": badge_str
                })
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)

            st.markdown("---")
            st.markdown("### Academic Analytics Visualizations")

            ch_col1, ch_col2 = st.columns(2)
            with ch_col1:
                st.pyplot(plot_subject_marks_bar(enriched_records))
            with ch_col2:
                st.pyplot(plot_attendance_vs_marks_scatter(enriched_records, ref_df))

            ch_col3, ch_col4 = st.columns(2)
            with ch_col3:
                st.pyplot(plot_actual_vs_predicted_marks(enriched_records))
            with ch_col4:
                st.pyplot(plot_weak_subjects_priority(analysis_result["sorted_subjects"]))

        # -----------------------------
        # Tab 3: Recommendations & Explainability
        # -----------------------------
        with rec_tab:
            st.markdown("### 🎯 Prioritized Action Plan & Transparent Explanations")
            st.caption("Subjects are sorted in descending order of urgency (High Priority first, followed by lower marks).")

            priority_order_names = " ➔ ".join([f"**{s['subject']}**" for s in analysis_result["sorted_subjects"]])
            st.markdown(f"**Focus Sequence:** {priority_order_names}")
            st.write("")

            for item in analysis_result["sorted_subjects"]:
                p = item["priority"]
                color_code = "#DC2626" if p == "High Priority" else ("#D97706" if p == "Medium Priority" else "#16A34A")

                with st.expander(f"{item['subject']} — Priority: {p} (Marks: {item['current_marks']:.1f}/40, Pred: {item['predicted_marks']:.1f}/40)", expanded=(p == "High Priority")):
                    c_rec, c_why = st.columns([1.2, 1])

                    with c_rec:
                        st.markdown(f"<h5 style='color:{color_code};'>Recommendations:</h5>", unsafe_allow_html=True)
                        for r in item["recommendations"]:
                            st.markdown(f"- {r}")

                    with c_why:
                        st.markdown("##### 🔍 Why this was generated (Explainability):")
                        st.markdown(f"""
                        <div class="explain-card">
                            <b>Current Marks:</b> {item['current_marks']:.1f} / 40<br>
                            <b>Attendance:</b> {item['attendance']:.1f}%<br>
                            <b>Study Hours:</b> {item['study_hours']:.1f} h/day<br>
                            <b>Predicted Final Marks:</b> {item['predicted_marks']:.1f} / 40<br>
                            <hr style="margin:8px 0;">
                            <b>System Rationale:</b><br>
                            {'<br>'.join(['• ' + r for r in item['reasons']])}
                        </div>
                        """, unsafe_allow_html=True)

        # -----------------------------
        # Tab 4: Update Academic Profile
        # -----------------------------
        with profile_tab:
            st.markdown("### ✏️ Update Academic Data & Provide Actual Results")
            st.caption("Modify your internal marks, attendance, study hours, or enter semester final marks to feed the continuous learning pipeline.")

            with st.form("update_profile_form"):
                st.subheader("1. General Profile")
                p_c1, p_c2 = st.columns(2)
                with p_c1:
                    u_name = st.text_input("Full Name", value=profile.get("name", ""))
                    u_elective = st.selectbox(
                        "Elective Subject",
                        ELECTIVE_SUBJECTS,
                        index=ELECTIVE_SUBJECTS.index(profile.get("elective", ELECTIVE_SUBJECTS[0])) if profile.get("elective") in ELECTIVE_SUBJECTS else 0
                    )
                with p_c2:
                    u_overall_att = st.number_input("Overall Attendance %", min_value=0.0, max_value=100.0, value=float(profile.get("overall_attendance", 85.0)), step=1.0)
                    u_overall_hrs = st.number_input("Overall Daily Study Hours", min_value=0.0, max_value=24.0, value=float(profile.get("overall_study_hours", 2.5)), step=0.5)

                st.subheader("2. Subject Marks & Habits (Marks out of 40)")

                active_subjects = CORE_SUBJECTS + [u_elective]
                updated_subject_records = []

                for subj in active_subjects:
                    rec_match = next((r for r in records if r.get("subject") == subj), {})
                    st.markdown(f"**📘 {subj}**")
                    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
                    with col_m1:
                        p_mark = st.number_input(f"Previous Marks", min_value=0.0, max_value=40.0, value=float(rec_match.get("previous_marks", 25.0)), step=0.5, key=f"prev_{subj}")
                    with col_m2:
                        i_mark = st.number_input(f"Internal Marks", min_value=0.0, max_value=40.0, value=float(rec_match.get("internal_marks", 25.0)), step=0.5, key=f"int_{subj}")
                    with col_m3:
                        att_val = st.number_input(f"Attendance %", min_value=0.0, max_value=100.0, value=float(rec_match.get("attendance", 80.0)), step=1.0, key=f"att_{subj}")
                    with col_m4:
                        hrs_val = st.number_input(f"Study Hours/Day", min_value=0.0, max_value=24.0, value=float(rec_match.get("study_hours", 2.0)), step=0.5, key=f"hrs_{subj}")
                    with col_m5:
                        actual_final = rec_match.get("actual_final_marks")
                        actual_str = str(actual_final) if actual_final is not None else ""
                        actual_input = st.text_input(f"Actual Final Mark (Optional)", value=actual_str, key=f"act_{subj}", help="Fill once final semester exam results are announced to help train the AI.")

                    # Validation
                    v_p, v_p_val, _ = validate_marks(p_mark)
                    v_i, v_i_val, _ = validate_marks(i_mark)
                    v_a, v_a_val, _ = validate_attendance(att_val)
                    v_h, v_h_val, _ = validate_study_hours(hrs_val)

                    act_val = None
                    if actual_input.strip():
                        v_act, v_act_res, _ = validate_marks(actual_input)
                        if v_act:
                            act_val = v_act_res

                    updated_subject_records.append({
                        "subject": subj,
                        "previous_marks": v_p_val,
                        "internal_marks": v_i_val,
                        "attendance": v_a_val,
                        "study_hours": v_h_val,
                        "actual_final_marks": act_val
                    })

                save_profile_btn = st.form_submit_button("💾 Save Profile & Academic Data", use_container_width=True)

            if save_profile_btn:
                # Update profile
                profile_ok = update_student_profile(student_id, u_name, u_elective, u_overall_att, u_overall_hrs, 28.0)
                records_ok = save_student_academic_records(student_id, updated_subject_records)

                if profile_ok and records_ok:
                    st.success("✅ Academic profile and marks saved successfully! Calculations updated.")
                    # Automatically trigger continual retraining if any actual marks were entered
                    has_verified = any(r["actual_final_marks"] is not None for r in updated_subject_records)
                    if has_verified:
                        try:
                            from models.train_models import train_and_evaluate_models
                            train_and_evaluate_models()
                            st.cache_resource.clear()
                            st.info("🤖 AI Models automatically retrained with your verified exam outcome!")
                        except Exception as e:
                            st.warning(f"Note: Model retraining note: {e}")
                    st.rerun()
                else:
                    st.error("Failed to update records. Please check database connectivity.")


# ==============================================================================
# 2. ADMIN DASHBOARD
# ==============================================================================
elif role_option == "Admin Dashboard":
    st.title("🛠️ Administrator & ML Operations Dashboard")
    st.markdown("Monitor student cohorts, analyze ML evaluation metrics, and supervise the continual learning loop.")

    # Admin Login verification
    admin_pw_target = os.getenv("ADMIN_PASSWORD", "admin123")
    if not st.session_state.admin_authenticated:
        with st.form("admin_auth_form"):
            entered_pw = st.text_input("Enter Admin Password", type="password")
            admin_submit = st.form_submit_button("Access Admin Panel", use_container_width=True)
            if admin_submit:
                if entered_pw == admin_pw_target:
                    st.session_state.admin_authenticated = True
                    st.success("Admin authenticated.")
                    st.rerun()
                else:
                    st.error("Invalid Admin password.")
        st.stop()

    # Authenticated Admin Panel
    if st.button("🚪 Logout Admin"):
        st.session_state.admin_authenticated = False
        st.rerun()

    admin_tab1, admin_tab2, admin_tab3 = st.tabs([
        "👥 Student Records Overview",
        "📈 ML Model Evaluation & Performance",
        "🔄 Continual Learning & Retraining"
    ])

    with admin_tab1:
        st.markdown("### Registered Students Directory")
        all_students = get_all_students_summary()

        if not all_students:
            st.info("No student accounts currently registered.")
        else:
            summary_data = []
            for s in all_students:
                s_id = s.get("student_id")
                s_name = s.get("name")
                s_elec = s.get("elective", "None")
                subjs = s.get("subjects", [])
                avg_m = (sum(r.get("internal_marks", 0) for r in subjs) / len(subjs)) if subjs else 0.0
                verified_count = sum(1 for r in subjs if r.get("actual_final_marks") is not None)

                summary_data.append({
                    "Student ID": s_id,
                    "Name": s_name,
                    "Elective": s_elec,
                    "Subjects Enrolled": len(subjs),
                    "Average Internal Marks": f"{avg_m:.1f} / 40",
                    "Verified Final Marks Logged": verified_count
                })

            st.dataframe(pd.DataFrame(summary_data), use_container_width=True, hide_index=True)

    with admin_tab2:
        st.markdown("### Machine Learning Model Evaluation")
        st.markdown("Metrics calculated directly from actual test sets (80% train / 20% test split).")

        if model_metrics:
            ds_info = model_metrics.get("dataset_summary", {})
            st.markdown(f"**Training Set Size:** {ds_info.get('train_records', 0)} records | **Test Set Size:** {ds_info.get('test_records', 0)} records | **Passing Threshold:** {ds_info.get('passing_threshold', 16)}/40")

            m_col1, m_col2 = st.columns(2)

            with m_col1:
                st.subheader("Model 1: Linear Regression (Final Marks)")
                reg_m = model_metrics.get("linear_regression", {}).get("metrics", {})
                st.markdown(f"""
                - **Mean Absolute Error (MAE):** `{reg_m.get('mae', 'N/A')}`
                - **Mean Squared Error (MSE):** `{reg_m.get('mse', 'N/A')}`
                - **Root MSE (RMSE):** `{reg_m.get('rmse', 'N/A')}`
                - **R² Score:** `{reg_m.get('r2', 'N/A')}`
                """)
                st.markdown("**Learned Feature Coefficients:**")
                st.json(model_metrics.get("linear_regression", {}).get("coefficients", {}))

            with m_col2:
                st.subheader("Model 2: Decision Tree (Pass / Fail)")
                clf_m = model_metrics.get("decision_tree", {}).get("metrics", {})
                st.markdown(f"""
                - **Accuracy:** `{clf_m.get('accuracy', 'N/A')}`
                - **Precision:** `{clf_m.get('precision', 'N/A')}`
                - **Recall:** `{clf_m.get('recall', 'N/A')}`
                - **F1 Score:** `{clf_m.get('f1_score', 'N/A')}`
                """)
                st.markdown("**Confusion Matrix (Actual vs Predicted):**")
                cm = clf_m.get("confusion_matrix", [[0, 0], [0, 0]])
                cm_df = pd.DataFrame(cm, columns=["Pred FAIL", "Pred PASS"], index=["Actual FAIL", "Actual PASS"])
                st.dataframe(cm_df)

                st.markdown("**Feature Importances:**")
                st.json(model_metrics.get("decision_tree", {}).get("feature_importances", {}))
        else:
            st.warning("No metrics file found. Run model training.")

    with admin_tab3:
        st.markdown("### Continual Learning Pipeline Status")
        st.markdown("""
        When students finish exams and record their **Actual Final Marks**, their verified records are pooled with
        the training dataset to retrain and continuously improve model accuracy over time.
        """)

        from database.mongodb import get_verified_records_for_retraining
        verified_recs = get_verified_records_for_retraining()
        st.metric("Total Verified Student Outcome Records in MongoDB", len(verified_recs))

        if st.button("🚀 Trigger Manual Model Retraining Now", use_container_width=True):
            with st.spinner("Retraining Linear Regression and Decision Tree models..."):
                try:
                    from models.train_models import train_and_evaluate_models
                    new_metrics = train_and_evaluate_models()
                    st.cache_resource.clear()
                    st.success("✅ Models retrained and re-evaluated successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Retraining failed: {e}")
