"""
Smart Study Recommendation System — Premium Academic Portal
Implemented strictly according to Design.md:
- Calm, structured university aesthetic (Academic Green #245C4A, clear typography, no AI clichés)
- Persistent sidebar navigation: Overview, Subjects, Progress, Study Plan, Update Data, Admin Portal
- Student-friendly terminology: "Needs attention", "Improving", "On track", "Why this matters", "Performance outlook"
- Deterministic explainability and continual learning feedback loop
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
    page_title="Study — Academic Performance Portal",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Design.md Stylesheet (Academic Green, Calm Surfaces, Non-Aggressive Hierarchy)
st.markdown("""
<style>
    /* Google Inter font fallback styling */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    /* Academic Header styling */
    .portal-brand {
        font-size: 1.25rem;
        font-weight: 750;
        letter-spacing: 0.08em;
        color: #52B788 !important;
        margin-bottom: 2px;
    }
    .portal-sub {
        font-size: 0.82rem;
        color: #AAB4AD !important;
        margin-bottom: 18px;
    }

    /* Calm Academic Card */
    .academic-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 16px;
    }

    /* Progress and Metric styling */
    .section-eyebrow {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #72A88F !important;
        margin-bottom: 6px;
    }
    .metric-hero {
        font-size: 2.1rem;
        font-weight: 700;
        line-height: 1.2;
        color: inherit;
        margin: 2px 0 6px 0;
    }
    .metric-sub {
        font-size: 0.88rem;
        color: #72948A !important;
    }

    /* Human Academic Badges */
    .badge-attention {
        background-color: rgba(201, 74, 74, 0.22);
        color: #FFA3A3 !important;
        border: 1px solid rgba(201, 74, 74, 0.45);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-improving {
        background-color: rgba(185, 130, 50, 0.22);
        color: #FAD38D !important;
        border: 1px solid rgba(185, 130, 50, 0.45);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }
    .badge-ontrack {
        background-color: rgba(62, 128, 97, 0.22);
        color: #8DE0B8 !important;
        border: 1px solid rgba(62, 128, 97, 0.45);
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        font-weight: 600;
    }

    /* Subject Row Card */
    .subject-row-card {
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 10px;
        background: rgba(255, 255, 255, 0.03);
    }

    /* Explainability Card ("Why this matters") */
    .why-card {
        background: rgba(82, 183, 136, 0.10);
        border: 1px solid rgba(82, 183, 136, 0.28);
        border-left: 4px solid #52B788;
        border-radius: 0 8px 8px 0;
        padding: 12px 16px;
        margin-top: 8px;
        font-size: 0.88rem;
        color: inherit;
    }

    /* Focus Number Block */
    .focus-number {
        font-size: 1.1rem;
        font-weight: 700;
        color: #52B788 !important;
        background: rgba(82, 183, 136, 0.16);
        border: 1px solid rgba(82, 183, 136, 0.3);
        width: 32px;
        height: 32px;
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* ================================================================
       DARK MODE — explicit overrides for Streamlit dark theme
    ================================================================ */
    [data-theme="dark"] .metric-hero  { color: #F0F3F0 !important; }
    [data-theme="dark"] .why-card     { color: #E2E8E4 !important; background: rgba(82, 183, 136, 0.08); }
    [data-theme="dark"] .academic-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.13);
    }
    [data-theme="dark"] .subject-row-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.11);
    }
    [data-theme="dark"] .badge-attention { color: #FFA3A3 !important; }
    [data-theme="dark"] .badge-improving { color: #FAD38D !important; }
    [data-theme="dark"] .badge-ontrack   { color: #8DE0B8 !important; }

    /* ================================================================
       LIGHT MODE — explicit overrides for Streamlit light theme
    ================================================================ */
    [data-theme="light"] .metric-hero { color: #1A2E23 !important; }
    [data-theme="light"] .metric-sub  { color: #4E6B5E !important; }
    [data-theme="light"] .why-card    { color: #1A2E23 !important; background: rgba(82, 183, 136, 0.10); }
    [data-theme="light"] .portal-sub  { color: #556B5E !important; }
    [data-theme="light"] .academic-card {
        background: rgba(36, 92, 74, 0.05);
        border: 1px solid rgba(36, 92, 74, 0.16);
    }
    [data-theme="light"] .subject-row-card {
        background: rgba(36, 92, 74, 0.04);
        border: 1px solid rgba(36, 92, 74, 0.14);
    }
    [data-theme="light"] .badge-attention { background-color: rgba(201, 74, 74, 0.12); color: #8B1A1A !important; border-color: rgba(201, 74, 74, 0.30); }
    [data-theme="light"] .badge-improving { background-color: rgba(185, 130, 50, 0.14); color: #6E470A !important; border-color: rgba(185, 130, 50, 0.30); }
    [data-theme="light"] .badge-ontrack   { background-color: rgba(62, 128, 97, 0.12);  color: #245C4A !important; border-color: rgba(62, 128, 97, 0.30); }

    /* prefers-color-scheme fallback (when data-theme isn't set yet) */
    @media (prefers-color-scheme: light) {
        .metric-hero  { color: #1A2E23 !important; }
        .metric-sub   { color: #4E6B5E !important; }
        .why-card     { color: #1A2E23 !important; }
        .portal-sub   { color: #556B5E !important; }
        .academic-card    { background: rgba(36,92,74,0.05); border: 1px solid rgba(36,92,74,0.16); }
        .subject-row-card { background: rgba(36,92,74,0.04); border: 1px solid rgba(36,92,74,0.14); }
        .badge-attention  { color: #8B1A1A !important; background-color: rgba(201,74,74,0.12); }
        .badge-improving  { color: #6E470A !important; background-color: rgba(185,130,50,0.14); }
        .badge-ontrack    { color: #245C4A !important; background-color: rgba(62,128,97,0.12); }
    }

    /* ================================================================
       SEMANTIC TEXT UTILITY CLASSES
       Use these in inline HTML instead of hardcoded dark-only hex.
    ================================================================ */

    /* Primary text — high contrast body copy */
    .t-primary { color: #1A2E23; }
    .t-secondary { color: #3A5447; }
    .t-muted { color: #556B5E; }
    .t-brand { color: #52B788 !important; }

    /* Dark mode overrides */
    [data-theme="dark"] .t-primary   { color: #F0F3F0; }
    [data-theme="dark"] .t-secondary { color: #CBD5E1; }
    [data-theme="dark"] .t-muted     { color: #94A3B8; }

    @media (prefers-color-scheme: dark) {
        .t-primary   { color: #F0F3F0; }
        .t-secondary { color: #CBD5E1; }
        .t-muted     { color: #94A3B8; }
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_ml_models():
    """Load serialized ML models and metrics report."""
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
    """Load reference dataset for visualization comparison."""
    data_path = os.path.join(BASE_DIR, "data", "student_dataset.csv")
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    return pd.DataFrame()


# Session state initialization
if "logged_in_student" not in st.session_state:
    st.session_state.logged_in_student = None
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


# Sidebar Navigation Setup (Design.md Section 8 & 9)
st.sidebar.markdown("""
<div style="padding-top:4px;">
    <div class="portal-brand">STUDY</div>
    <div class="portal-sub">Academic Progress Portal</div>
</div>
""", unsafe_allow_html=True)

db_ok, db_msg = check_connection()
if db_ok:
    st.sidebar.caption("🟢 Connected to Academic DB")
    seed_demo_students_if_empty()
else:
    st.sidebar.error("🔴 Database Offline")
    st.sidebar.caption(db_msg)

reg_model, clf_model, model_metrics = load_ml_models()
ref_df = load_reference_dataset()

# Navigation options
if st.session_state.logged_in_student:
    nav_selection = st.sidebar.radio(
        "Navigation",
        ["Overview", "Subjects", "Progress", "Study Plan", "Update Academic Data", "Admin Portal"],
        index=0
    )
else:
    nav_selection = st.sidebar.radio(
        "Navigation",
        ["Student Access", "Admin Portal"],
        index=0
    )

# Student profile card at sidebar bottom if logged in
if st.session_state.logged_in_student:
    curr_student = st.session_state.logged_in_student
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div class="t-primary" style="font-size:0.88rem; font-weight:600;">{curr_student.get('name', 'Student')}</div>
    <div class="t-muted" style="font-size:0.78rem;">ID: {curr_student.get('student_id')} · Semester 5</div>
    """, unsafe_allow_html=True)
    if st.sidebar.button("Sign out", key="sidebar_logout_btn"):
        st.session_state.logged_in_student = None
        st.rerun()


# ==============================================================================
# AUTHENTICATION SCREEN (Design.md Section 30 & 31)
# ==============================================================================
if not st.session_state.logged_in_student and nav_selection == "Student Access":
    if not db_ok:
        st.error("We couldn't connect to the academic database. Please check your `.env` connection settings.")
        st.stop()

    auth_col1, auth_col2, auth_col3 = st.columns([1, 1.8, 1])
    with auth_col2:
        st.markdown("""
        <div style="text-align:center; padding: 30px 0 16px 0;">
            <div style="font-size: 1.8rem; font-weight: 700; color: #52B788; letter-spacing: 0.05em;">STUDY</div>
            <div class="t-muted" style="font-size: 0.95rem; margin-top: 4px;">Your academic progress, in one place.</div>
        </div>
        """, unsafe_allow_html=True)

        tab_signin, tab_register = st.tabs(["Sign In", "Create Account"])

        with tab_signin:
            with st.form("signin_form"):
                stu_id = st.text_input("Student ID", placeholder="e.g. STU101").strip().upper()
                stu_pw = st.text_input("Password", type="password")
                submit_login = st.form_submit_button("Sign in to Study", use_container_width=True)

            if submit_login:
                if not stu_id or not stu_pw:
                    st.error("Please enter both Student ID and Password.")
                else:
                    ok, student_doc, msg = authenticate_student(stu_id, stu_pw)
                    if ok:
                        st.session_state.logged_in_student = student_doc
                        st.rerun()
                    else:
                        st.error(msg)

            st.caption("Demo Accounts: `STU101` or `STU102` | Password: `password123`")

        with tab_register:
            with st.form("register_form"):
                reg_id = st.text_input("Choose Student ID (e.g. STU105)").strip().upper()
                reg_name = st.text_input("Full Name")
                reg_elective = st.selectbox("Select Elective Subject", ELECTIVE_SUBJECTS)
                reg_pw = st.text_input("Choose Password", type="password")
                submit_reg = st.form_submit_button("Create Student Account", use_container_width=True)

            if submit_reg:
                if not reg_id or not reg_name or not reg_pw:
                    st.error("All registration fields are required.")
                else:
                    ok, msg = register_student(reg_id, reg_name, reg_pw, reg_elective)
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)


# ==============================================================================
# LOGGED IN STUDENT PORTAL (Design.md Sections 10 - 21)
# ==============================================================================
elif st.session_state.logged_in_student and nav_selection != "Admin Portal":
    student = st.session_state.logged_in_student
    student_id = student["student_id"]

    # Retrieve fresh records from MongoDB
    profile = get_student_profile(student_id) or student
    records = get_student_academic_records(student_id)

    # Empty State check (Design.md Section 65)
    if not records:
        st.markdown(f"## Welcome to Study, {profile.get('name', 'Student')}")
        st.markdown("""
        Your academic dashboard is ready. Add your subject performance to see:
        - Your current progress
        - Performance outlook
        - Subjects needing attention
        - Your personalized study plan
        """)
        if st.button("Add academic data now"):
            nav_selection = "Update Academic Data"
            st.rerun()
        st.stop()

    # Inference & Rule Evaluation
    enriched_records = batch_predict_subject_records(reg_model, clf_model, records) if (reg_model and clf_model) else records
    analysis = analyze_student_academic_state(enriched_records)
    standing = analysis["academic_standing"]
    sorted_subjects = analysis["sorted_subjects"]

    # Compute overall statistics (Marks are out of 40)
    avg_internal = sum(r.get("internal_marks", 0.0) for r in enriched_records) / max(len(enriched_records), 1)
    avg_predicted = standing["avg_predicted"]
    avg_attendance = sum(r.get("attendance", 0.0) for r in enriched_records) / max(len(enriched_records), 1)

    # Normalize to 100-point scale for overall progress bar (Design.md Section 11 & 13)
    score_100 = (avg_internal / 40.0) * 100.0
    pred_100 = (avg_predicted / 40.0) * 100.0

    # --------------------------------------------------------------------------
    # 1. OVERVIEW PAGE (Design.md Section 11 - 16)
    # --------------------------------------------------------------------------
    if nav_selection == "Overview":
        # Welcome Header (Section 12)
        st.markdown(f"### Good afternoon, {profile.get('name', 'Student')}")
        st.caption(f"Semester 5 · Computer Science & Engineering · {profile.get('elective', 'N/A')}")
        st.write("")

        # Two-column top section: YOUR PROGRESS & THIS WEEK (Section 11)
        col_prog, col_week = st.columns([1.1, 1])

        with col_prog:
            st.markdown("""
            <div class="academic-card">
                <div class="section-eyebrow">Your Academic Progress</div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div class='metric-hero'>{avg_internal:.1f} <span class='t-muted' style='font-size:1rem;'>/ 40</span></div>", unsafe_allow_html=True)
            st.progress(min(max(avg_internal / 40.0, 0.0), 1.0))
            st.markdown(f"<div class='metric-sub' style='margin-top:6px;'>Performance outlook: <b>{avg_predicted:.1f} / 40</b> predicted final average</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col_week:
            st.markdown("""
            <div class="academic-card">
                <div class="section-eyebrow">This Week's Focus</div>
            """, unsafe_allow_html=True)
            st.markdown(f"<div class='t-primary' style='font-size:1.15rem; font-weight:600;'>Study target: <b>{analysis['recommended_study_hours']} hrs / day</b></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='t-muted' style='font-size:0.92rem; margin: 4px 0 10px 0;'>Attendance average: <b>{avg_attendance:.1f}%</b></div>", unsafe_allow_html=True)

            # Academic standing presentation (Section 14 & 45)
            badge_class = "badge-attention" if standing["standing_level"] == "High" else ("badge-improving" if standing["standing_level"] == "Medium" else "badge-ontrack")
            st.markdown(f"""
            <div class="t-primary" style="font-size:0.88rem; margin-top:6px;">
                Academic standing: <span class="{badge_class}">{standing['standing_label']}</span>
            </div>
            <div class="t-muted" style="font-size:0.82rem; margin-top:4px;">{standing['standing_description']}</div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        st.write("")
        st.markdown("#### Your Subjects")

        # Subject List View (Section 15 & 16)
        for subj_item in sorted_subjects:
            subj_name = subj_item["subject"]
            cur_m = subj_item["current_marks"]
            pred_m = subj_item["predicted_marks"]
            att_v = subj_item["attendance"]
            hrs_v = subj_item["study_hours"]
            status_text = subj_item["display_status"]

            badge_html = f"<span class='badge-attention'>Needs attention</span>" if status_text == "Needs attention" else (
                f"<span class='badge-improving'>Improving</span>" if status_text == "Improving" else f"<span class='badge-ontrack'>On track</span>"
            )

            st.markdown(f"""
            <div class="subject-row-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <span class="t-primary" style="font-weight:650; font-size:1.02rem;">{subj_name}</span>
                    </div>
                    <div>
                        {badge_html}
                    </div>
                </div>
                <div style="margin: 8px 0 6px 0;">
                    <div class="t-secondary" style="display:flex; justify-content:space-between; font-size:0.85rem; margin-bottom:2px;">
                        <span>Current: <b class="t-primary">{cur_m:.1f} / 40</b></span>
                        <span>Predicted: <b style="color:#52B788;">{pred_m:.1f} / 40</b></span>
                    </div>
                </div>
                <div class="t-muted" style="font-size:0.82rem;">
                    Attendance: {att_v:.1f}% · Study time: {hrs_v:.1f} hrs/day
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### What to Focus On Next")

        # Top 3 Focus Actions (Section 11)
        top_focus = sorted_subjects[:3]
        for idx, item in enumerate(top_focus, 1):
            top_rec = item["recommendations"][0] if item["recommendations"] else "Maintain consistent study routine"
            st.markdown(f"""
            <div class="subject-row-card" style="display:flex; align-items:flex-start; margin-bottom:12px;">
                <div class="focus-number" style="margin-right:14px; flex-shrink:0;">0{idx}</div>
                <div>
                    <div class="t-primary" style="font-weight:600; font-size:0.95rem;">{item['subject']}</div>
                    <div class="t-secondary" style="font-size:0.86rem; margin-top:2px;">{top_rec}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 2. SUBJECTS PAGE (Design.md Section 15 & 17)
    # --------------------------------------------------------------------------
    elif nav_selection == "Subjects":
        st.markdown("### Course Subjects & Academic Performance")
        st.caption("Detailed view of all 5 enrolled semester courses.")

        for item in sorted_subjects:
            status_text = item["display_status"]
            badge_html = f"<span class='badge-attention'>Needs attention</span>" if status_text == "Needs attention" else (
                f"<span class='badge-improving'>Improving</span>" if status_text == "Improving" else f"<span class='badge-ontrack'>On track</span>"
            )

            with st.expander(f"{item['subject']} — {item['current_marks']:.1f}/40 ({status_text})", expanded=(status_text == "Needs attention")):
                c_data1, c_data2 = st.columns([1.2, 1])

                with c_data1:
                    st.markdown(f"**Current Status:** {badge_html}", unsafe_allow_html=True)
                    st.markdown(f"""
                    - **Current Marks:** `{item['current_marks']:.1f} / 40`
                    - **Predicted Final Marks:** `{item['predicted_marks']:.1f} / 40`
                    - **Attendance Rate:** `{item['attendance']:.1f}%`
                    - **Daily Study Time:** `{item['study_hours']:.1f} hrs/day`
                    """)

                    st.markdown("**Your Next Focus:**")
                    for r in item["recommendations"]:
                        st.markdown(f"- {r}")

                with c_data2:
                    st.markdown("**Why this matters:**")
                    reasons_html = "<br/>".join([f"• {r}" for r in item["reasons"]])
                    st.markdown(f"""
                    <div class="why-card">
                        <b>Academic Factors:</b><br/>
                        {reasons_html}
                    </div>
                    """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 3. PROGRESS PAGE (Design.md Section 22 - 27)
    # --------------------------------------------------------------------------
    elif nav_selection == "Progress":
        st.markdown("### Academic Analytics & Progress")
        st.caption("Supporting visualizations and performance comparisons.")

        # Performance Overview Cards
        p_c1, p_c2 = st.columns(2)
        with p_c1:
            st.markdown(f"""
            <div class="academic-card">
                <div class="section-eyebrow">Current Average</div>
                <div class="metric-hero">{avg_internal:.1f} <span class="t-muted" style="font-size:1rem;">/ 40</span></div>
            </div>
            """, unsafe_allow_html=True)
        with p_c2:
            st.markdown(f"""
            <div class="academic-card">
                <div class="section-eyebrow">Predicted Average Outcome</div>
                <div class="metric-hero" style="color:#52B788 !important;">{avg_predicted:.1f} <span class="t-muted" style="font-size:1rem;">/ 40</span></div>
            </div>
            """, unsafe_allow_html=True)

        st.write("")
        st.markdown("#### Subject Comparison Charts")

        ch1, ch2 = st.columns(2)
        with ch1:
            st.pyplot(plot_subject_marks_bar(enriched_records))
        with ch2:
            st.pyplot(plot_attendance_vs_marks_scatter(enriched_records, ref_df))

        ch3, ch4 = st.columns(2)
        with ch3:
            st.pyplot(plot_actual_vs_predicted_marks(enriched_records))
        with ch4:
            st.pyplot(plot_weak_subjects_priority(sorted_subjects))

        st.markdown("---")
        with st.expander("Technical Model Performance Details"):
            st.caption("Verification metrics evaluated from actual test splits.")
            if model_metrics:
                m1, m2 = st.columns(2)
                with m1:
                    reg_m = model_metrics.get("linear_regression", {}).get("metrics", {})
                    st.markdown(f"""
                    **Linear Regression (Final Marks)**
                    - R²: `{reg_m.get('r2')}`
                    - MAE: `{reg_m.get('mae')} marks`
                    - RMSE: `{reg_m.get('rmse')} marks`
                    """)
                with m2:
                    clf_m = model_metrics.get("decision_tree", {}).get("metrics", {})
                    st.markdown(f"""
                    **Decision Tree (Pass/Fail)**
                    - Accuracy: `{clf_m.get('accuracy')}`
                    - Precision: `{clf_m.get('precision')}`
                    - Recall: `{clf_m.get('recall')}`
                    - F1-Score: `{clf_m.get('f1_score')}`
                    """)

    # --------------------------------------------------------------------------
    # 4. STUDY PLAN (Design.md Section 18 - 21)
    # --------------------------------------------------------------------------
    elif nav_selection == "Study Plan":
        st.markdown("### Your Study Plan")
        st.caption("Prioritized academic schedule and transparent guidance.")

        st.markdown(f"""
        <div style="background:rgba(82, 183, 136, 0.14); border:1px solid rgba(82, 183, 136, 0.35); border-radius:8px; padding:16px 20px; margin-bottom:20px;">
            <div class="t-brand" style="font-size:0.85rem; font-weight:600; text-transform:uppercase;">Recommended Daily Study Target</div>
            <div class="t-primary" style="font-size:1.7rem; font-weight:700; margin:4px 0;">{analysis['recommended_study_hours']} hours / day</div>
            <div class="t-secondary" style="font-size:0.88rem;">Allocated based on your areas currently needing attention.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### Priority Action Sequence")
        for idx, item in enumerate(sorted_subjects, 1):
            status_text = item["display_status"]
            badge_html = f"<span class='badge-attention'>Needs attention</span>" if status_text == "Needs attention" else (
                f"<span class='badge-improving'>Improving</span>" if status_text == "Improving" else f"<span class='badge-ontrack'>On track</span>"
            )

            recs_html = "".join([f'<div class="t-secondary" style="font-size:0.88rem; margin-bottom:4px;">• {r}</div>' for r in item['recommendations']])
            reasons_html = "<br/>".join([f"• {r}" for r in item['reasons']])

            st.markdown(f"""
            <div class="subject-row-card" style="padding:16px 20px; margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center;">
                        <span class="focus-number" style="margin-right:12px;">0{idx}</span>
                        <span class="t-primary" style="font-size:1.05rem; font-weight:650;">{item['subject']}</span>
                    </div>
                    <div>{badge_html}</div>
                </div>
                <div style="margin:12px 0 8px 44px;">
                    <div class="t-primary" style="font-weight:600; font-size:0.9rem; margin-bottom:4px;">Actionable Plan:</div>
                    {recs_html}
                </div>
                <div style="margin-left:44px;">
                    <div class="why-card">
                        <b>Why this matters:</b><br/>
                        {reasons_html}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # 5. UPDATE ACADEMIC DATA (Design.md Section 28 & 29)
    # --------------------------------------------------------------------------
    elif nav_selection == "Update Academic Data":
        st.markdown("### Update Academic Data")
        st.caption("Keep your attendance, internal marks, and study hours up to date. Adding semester final marks helps improve system accuracy.")

        with st.form("update_academic_form"):
            st.markdown("##### Profile Details")
            u_col1, u_col2 = st.columns(2)
            with u_col1:
                new_name = st.text_input("Full Name", value=profile.get("name", ""))
                new_elec = st.selectbox(
                    "Elective Course",
                    ELECTIVE_SUBJECTS,
                    index=ELECTIVE_SUBJECTS.index(profile.get("elective", ELECTIVE_SUBJECTS[0])) if profile.get("elective") in ELECTIVE_SUBJECTS else 0
                )
            with u_col2:
                new_overall_att = st.number_input("Overall Attendance %", min_value=0.0, max_value=100.0, value=float(profile.get("overall_attendance", 85.0)), step=1.0)
                new_overall_hrs = st.number_input("Average Daily Study Hours", min_value=0.0, max_value=24.0, value=float(profile.get("overall_study_hours", 2.5)), step=0.5)

            st.markdown("---")
            st.markdown("##### Subject Marks & Hours (Marks out of 40)")

            active_course_list = CORE_SUBJECTS + [new_elec]
            new_records_payload = []

            for subj in active_course_list:
                rec_match = next((r for r in records if r.get("subject") == subj), {})
                st.markdown(f"**{subj}**")
                s_c1, s_c2, s_c3, s_c4, s_c5 = st.columns(5)
                with s_c1:
                    p_val = st.number_input("Previous Marks", min_value=0.0, max_value=40.0, value=float(rec_match.get("previous_marks", 25.0)), step=0.5, key=f"f_prev_{subj}")
                with s_c2:
                    i_val = st.number_input("Internal Marks", min_value=0.0, max_value=40.0, value=float(rec_match.get("internal_marks", 25.0)), step=0.5, key=f"f_int_{subj}")
                with s_c3:
                    a_val = st.number_input("Attendance %", min_value=0.0, max_value=100.0, value=float(rec_match.get("attendance", 80.0)), step=1.0, key=f"f_att_{subj}")
                with s_c4:
                    h_val = st.number_input("Study Hours/Day", min_value=0.0, max_value=24.0, value=float(rec_match.get("study_hours", 2.0)), step=0.5, key=f"f_hrs_{subj}")
                with s_c5:
                    act_raw = rec_match.get("actual_final_marks")
                    act_init = str(act_raw) if act_raw is not None else ""
                    act_val_input = st.text_input("Actual Final Marks (Optional)", value=act_init, key=f"f_act_{subj}", help="Enter once semester results are published to refine prediction accuracy.")

                act_final_val = None
                if act_val_input.strip():
                    v_ok, v_res, _ = validate_marks(act_val_input)
                    if v_ok:
                        act_final_val = v_res

                new_records_payload.append({
                    "subject": subj,
                    "previous_marks": p_val,
                    "internal_marks": i_val,
                    "attendance": a_val,
                    "study_hours": h_val,
                    "actual_final_marks": act_final_val
                })

            submit_update = st.form_submit_button("Save Academic Updates", use_container_width=True)

        if submit_update:
            p_saved = update_student_profile(student_id, new_name, new_elec, new_overall_att, new_overall_hrs, 28.0)
            r_saved = save_student_academic_records(student_id, new_records_payload)

            if p_saved and r_saved:
                st.success("Your academic records have been saved successfully.")
                # Continual learning check
                if any(r["actual_final_marks"] is not None for r in new_records_payload):
                    try:
                        from models.train_models import train_and_evaluate_models
                        train_and_evaluate_models()
                        st.cache_resource.clear()
                        st.info("System models refined with verified semester outcome.")
                    except Exception as e:
                        pass
                st.rerun()
            else:
                st.error("Failed to save changes. Please verify database connection.")


# ==============================================================================
# ADMIN PORTAL (Design.md Section 59 & 60)
# ==============================================================================
if nav_selection == "Admin Portal":
    st.markdown("### Administrator & Institutional Analytics")
    st.caption("Faculty supervision and technical machine learning metrics.")

    admin_pw_target = os.getenv("ADMIN_PASSWORD", "admin123")
    if not st.session_state.admin_authenticated:
        with st.form("admin_portal_login"):
            admin_input = st.text_input("Admin Password", type="password")
            admin_btn = st.form_submit_button("Sign In as Administrator", use_container_width=True)
            if admin_btn:
                if admin_input == admin_pw_target:
                    st.session_state.admin_authenticated = True
                    st.rerun()
                else:
                    st.error("Invalid administrator password.")
        st.stop()

    if st.button("Log out of Admin Portal"):
        st.session_state.admin_authenticated = False
        st.rerun()

    adm_tab1, adm_tab2, adm_tab3 = st.tabs(["Cohort Directory", "Model Validation", "Retraining Pipeline"])

    with adm_tab1:
        st.markdown("##### Registered Students Directory")
        all_students = get_all_students_summary()
        if not all_students:
            st.info("No registered students found.")
        else:
            tbl_data = []
            for s in all_students:
                s_subjs = s.get("subjects", [])
                avg_m = (sum(r.get("internal_marks", 0) for r in s_subjs) / len(s_subjs)) if s_subjs else 0.0
                v_count = sum(1 for r in s_subjs if r.get("actual_final_marks") is not None)
                tbl_data.append({
                    "Student ID": s.get("student_id"),
                    "Name": s.get("name"),
                    "Elective": s.get("elective"),
                    "Internal Average": f"{avg_m:.1f} / 40",
                    "Verified Outcomes Logged": v_count
                })
            st.dataframe(pd.DataFrame(tbl_data), use_container_width=True, hide_index=True)

    with adm_tab2:
        st.markdown("##### Machine Learning Evaluation")
        if model_metrics:
            ds = model_metrics.get("dataset_summary", {})
            st.markdown(f"**Records in Master Dataset:** {ds.get('total_records', 0)} ({ds.get('train_records', 0)} training / {ds.get('test_records', 0)} testing)")

            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown("**Linear Regression (Final Marks)**")
                r_m = model_metrics.get("linear_regression", {}).get("metrics", {})
                st.markdown(f"""
                - R² Score: `{r_m.get('r2')}`
                - MAE: `{r_m.get('mae')}` marks
                - MSE: `{r_m.get('mse')}`
                - RMSE: `{r_m.get('rmse')}` marks
                """)
                st.markdown("**Learned Coefficients:**")
                st.json(model_metrics.get("linear_regression", {}).get("coefficients", {}))

            with col_m2:
                st.markdown("**Decision Tree (Pass / Fail)**")
                c_m = model_metrics.get("decision_tree", {}).get("metrics", {})
                st.markdown(f"""
                - Accuracy: `{c_m.get('accuracy')}`
                - Precision: `{c_m.get('precision')}`
                - Recall: `{c_m.get('recall')}`
                - F1-Score: `{c_m.get('f1_score')}`
                """)
                st.markdown("**Confusion Matrix:**")
                cm = c_m.get("confusion_matrix", [[0, 0], [0, 0]])
                st.dataframe(pd.DataFrame(cm, columns=["Pred Fail", "Pred Pass"], index=["Actual Fail", "Actual Pass"]))

    with adm_tab3:
        st.markdown("##### Continual Learning Supervision")
        from database.mongodb import get_verified_records_for_retraining
        verified_count = len(get_verified_records_for_retraining())
        st.metric("Total Verified Student Outcome Records in Database", verified_count)

        if st.button("Trigger Full Pipeline Retraining", use_container_width=True):
            with st.spinner("Retraining Linear Regression and Decision Tree models..."):
                try:
                    from models.train_models import train_and_evaluate_models
                    train_and_evaluate_models()
                    st.cache_resource.clear()
                    st.success("Models retrained and benchmark report updated.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Retraining error: {e}")
