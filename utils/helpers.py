"""
Utility Helpers for Smart Study Recommendation System
Includes input validators and clean academic visualizations using Matplotlib and Seaborn.
"""

from typing import Tuple, List, Dict, Any, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


# -----------------------------
# Input Validation Functions
# -----------------------------

def validate_marks(val: Any) -> Tuple[bool, Optional[float], str]:
    """Validate that marks are between 0 and 40."""
    try:
        f_val = float(val)
        if 0.0 <= f_val <= 40.0:
            return True, round(f_val, 1), ""
        return False, None, "Marks must be between 0.0 and 40.0."
    except (ValueError, TypeError):
        return False, None, "Invalid numerical value for marks."


def validate_attendance(val: Any) -> Tuple[bool, Optional[float], str]:
    """Validate that attendance percentage is between 0 and 100."""
    try:
        f_val = float(val)
        if 0.0 <= f_val <= 100.0:
            return True, round(f_val, 1), ""
        return False, None, "Attendance must be between 0.0% and 100.0%."
    except (ValueError, TypeError):
        return False, None, "Invalid numerical value for attendance."


def validate_study_hours(val: Any) -> Tuple[bool, Optional[float], str]:
    """Validate that daily study hours are >= 0."""
    try:
        f_val = float(val)
        if 0.0 <= f_val <= 24.0:
            return True, round(f_val, 1), ""
        return False, None, "Study hours must be between 0.0 and 24.0 hours/day."
    except (ValueError, TypeError):
        return False, None, "Invalid numerical value for study hours."


# -----------------------------
# Visualization Functions (Matplotlib & Seaborn)
# -----------------------------

# Set modern aesthetic
sns.set_theme(style="whitegrid", font="sans-serif")
plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "figure.titlesize": 13,
})


def plot_subject_marks_bar(subject_data: List[Dict[str, Any]]) -> plt.Figure:
    """
    Chart 1: Subject-wise Marks Bar Chart
    Shows current marks for each subject with color-coded priority thresholds.
    """
    df = pd.DataFrame(subject_data)
    fig, ax = plt.subplots(figsize=(7, 4))

    # Priority colors: Red for High Priority (<25), Amber for Medium (25-30), Green for Maintain (>30)
    palette = []
    for m in df["internal_marks"]:
        if m < 25.0:
            palette.append("#E63946")  # Red
        elif m <= 30.0:
            palette.append("#F4A261")  # Amber
        else:
            palette.append("#2A9D8F")  # Teal Green

    bars = ax.bar(df["subject"], df["internal_marks"], color=palette, width=0.55, edgecolor="#2B2D42", linewidth=0.8)

    # Reference threshold lines
    ax.axhline(16, color="#D90429", linestyle="--", alpha=0.7, label="Pass Threshold (16/40)")
    ax.axhline(25, color="#F4A261", linestyle=":", alpha=0.7, label="High Priority Threshold (<25)")
    ax.axhline(31, color="#2A9D8F", linestyle=":", alpha=0.7, label="Maintain Threshold (>30)")

    ax.set_ylim(0, 44)
    ax.set_ylabel("Internal Marks (out of 40)")
    ax.set_title("Subject-wise Academic Performance", fontweight="bold", pad=12)
    plt.xticks(rotation=20, ha="right")

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

    ax.legend(loc="upper right", framealpha=0.9, fontsize=8)
    fig.tight_layout()
    return fig


def plot_attendance_vs_marks_scatter(subject_data: List[Dict[str, Any]], background_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """
    Chart 2: Attendance vs Marks Scatter Plot
    Plots the student's subjects with contextual distribution.
    """
    fig, ax = plt.subplots(figsize=(7, 4))

    if background_df is not None and not background_df.empty:
        # Sample background for context
        sample_bg = background_df.sample(min(150, len(background_df)), random_state=42)
        ax.scatter(sample_bg["attendance"], sample_bg["internal_marks"],
                   color="#D1D5DB", alpha=0.35, s=25, label="Cohort Reference")

    df = pd.DataFrame(subject_data)
    scatter = ax.scatter(df["attendance"], df["internal_marks"],
                         c=df["internal_marks"], cmap="coolwarm_r",
                         s=130, edgecolor="#1E293B", linewidth=1.5, zorder=5, label="Your Subjects")

    for _, row in df.iterrows():
        ax.annotate(row["subject"].split("(")[0].strip()[:10],
                    xy=(row["attendance"], row["internal_marks"]),
                    xytext=(6, 4), textcoords="offset points",
                    fontsize=8, fontweight="medium", color="#0F172A")

    # Threshold markers
    ax.axvline(80, color="#E63946", linestyle="--", alpha=0.6, label="Min Attendance (80%)")
    ax.axhline(16, color="#D90429", linestyle=":", alpha=0.6, label="Pass Marks (16/40)")

    ax.set_xlabel("Attendance Percentage (%)")
    ax.set_ylabel("Marks (out of 40)")
    ax.set_title("Attendance vs. Marks Distribution", fontweight="bold", pad=12)
    ax.set_xlim(40, 105)
    ax.set_ylim(0, 44)
    ax.legend(loc="lower right", framealpha=0.9, fontsize=8)
    fig.tight_layout()
    return fig


def plot_actual_vs_predicted_marks(subject_data: List[Dict[str, Any]]) -> plt.Figure:
    """
    Chart 3: Actual vs. Predicted Marks Comparison
    Grouped bar chart showing current marks vs ML predicted final marks.
    """
    df = pd.DataFrame(subject_data)
    fig, ax = plt.subplots(figsize=(7, 4))

    x = np.arange(len(df))
    width = 0.35

    bars1 = ax.bar(x - width/2, df["internal_marks"], width, label="Current Internal Marks", color="#3A86FF", edgecolor="#1D3557", linewidth=0.8)
    bars2 = ax.bar(x + width/2, df["predicted_marks"], width, label="Predicted Final Marks (ML)", color="#8338EC", edgecolor="#1D3557", linewidth=0.8)

    ax.set_ylabel("Marks (out of 40)")
    ax.set_title("Current vs. Predicted Final Performance", fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels([s.split("(")[0].strip() for s in df["subject"]], rotation=20, ha="right")
    ax.set_ylim(0, 44)
    ax.axhline(16, color="#E63946", linestyle="--", alpha=0.7, label="Pass Benchmark (16/40)")

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.1f}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")

    ax.legend(loc="upper right", framealpha=0.9, fontsize=8)
    fig.tight_layout()
    return fig


def plot_weak_subjects_priority(sorted_subjects: List[Dict[str, Any]]) -> plt.Figure:
    """
    Chart 4: Weak Subject Priority Chart
    Visualizes all subjects sorted from highest academic priority to maintain.
    """
    df = pd.DataFrame(sorted_subjects)
    fig, ax = plt.subplots(figsize=(7, 3.8))

    color_map = {
        "High Priority": "#E63946",
        "Medium Priority": "#F4A261",
        "Maintain": "#2A9D8F"
    }
    colors = [color_map.get(p, "#94A3B8") for p in df["priority"]]

    y_pos = np.arange(len(df))
    bars = ax.barh(y_pos, df["current_marks"], color=colors, height=0.55, edgecolor="#1E293B", linewidth=0.8)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["subject"])
    ax.invert_yaxis()  # Highest priority on top
    ax.set_xlabel("Current Marks (out of 40)")
    ax.set_title("Subject Priority Matrix (Weakest & Critical First)", fontweight="bold", pad=12)
    ax.set_xlim(0, 44)

    for bar, priority in zip(bars, df["priority"]):
        w = bar.get_width()
        ax.annotate(f" {w:.1f}  [{priority}]",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0),
                    textcoords="offset points",
                    ha="left", va="center", fontsize=8.5, fontweight="bold")

    fig.tight_layout()
    return fig
