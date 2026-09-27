"""
Utility Helpers for Smart Study Recommendation System
Includes input validators and academic visualizations styled per Design.md:
Palette: Academic Green (#245C4A), Needs Attention (#C94A4A), Improving (#B98232), On Track (#3E8061).
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
# Chart Helpers (Design.md Sections 24, 25, 26)
# -----------------------------

COLOR_PRIMARY = "#245C4A"
COLOR_SECONDARY = "#8A938D"
COLOR_ATTENTION = "#C94A4A"
COLOR_IMPROVING = "#B98232"
COLOR_ON_TRACK = "#3E8061"
COLOR_BORDER = "#E2E7E3"


def configure_chart_axes(ax):
    """Apply consistent quiet academic styling per Design.md."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_BORDER)
    ax.spines["bottom"].set_color(COLOR_BORDER)
    ax.yaxis.grid(True, linestyle=":", color=COLOR_BORDER, alpha=0.8)
    ax.xaxis.grid(False)


def plot_subject_marks_bar(subject_data: List[Dict[str, Any]]) -> plt.Figure:
    """
    Chart 1: Subject-wise Marks Bar Chart
    Shows current marks for each subject with color-coded status.
    """
    sns.set_theme(style="white", font="sans-serif")
    df = pd.DataFrame(subject_data)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    palette = []
    for m in df["internal_marks"]:
        if m < 25.0:
            palette.append(COLOR_ATTENTION)
        elif m <= 30.0:
            palette.append(COLOR_IMPROVING)
        else:
            palette.append(COLOR_ON_TRACK)

    bars = ax.bar(
        [s.split("(")[0].strip() for s in df["subject"]],
        df["internal_marks"],
        color=palette,
        width=0.48
    )

    ax.axhline(16, color="#C94A4A", linestyle="--", linewidth=1.0, alpha=0.7, label="Pass Benchmark (16)")
    ax.set_ylim(0, 44)
    ax.set_ylabel("Marks (out of 40)", color="#68736C", fontsize=9.5)
    ax.set_title("Current Subject Performance", color="#17211B", fontsize=11, fontweight="bold", pad=12)

    configure_chart_axes(ax)

    for bar in bars:
        h = bar.get_height()
        ax.annotate(f"{h:.1f}",
                    xy=(bar.get_x() + bar.get_width() / 2, h),
                    xytext=(0, 4), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8.5, color="#17211B", fontweight="bold")

    ax.legend(loc="upper right", frameon=False, fontsize=8)
    fig.tight_layout()
    return fig


def plot_attendance_vs_marks_scatter(subject_data: List[Dict[str, Any]], background_df: Optional[pd.DataFrame] = None) -> plt.Figure:
    """
    Chart 2: Attendance vs Marks Scatter Plot
    Shows student's subject standing against general cohort distribution.
    """
    sns.set_theme(style="white", font="sans-serif")
    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    if background_df is not None and not background_df.empty:
        sample_bg = background_df.sample(min(120, len(background_df)), random_state=42)
        ax.scatter(sample_bg["attendance"], sample_bg["internal_marks"],
                   color=COLOR_SECONDARY, alpha=0.25, s=20, label="Cohort Reference")

    df = pd.DataFrame(subject_data)
    ax.scatter(df["attendance"], df["internal_marks"],
               color=COLOR_PRIMARY, s=90, edgecolors="#17211B", linewidth=1.2, zorder=5, label="Your Subjects")

    for _, row in df.iterrows():
        ax.annotate(row["subject"].split("(")[0].strip()[:9],
                    xy=(row["attendance"], row["internal_marks"]),
                    xytext=(5, 4), textcoords="offset points",
                    fontsize=8, color="#17211B")

    ax.axvline(80, color=COLOR_ATTENTION, linestyle="--", linewidth=1.0, alpha=0.6, label="Min Attendance (80%)")
    ax.set_xlabel("Attendance (%)", color="#68736C", fontsize=9.5)
    ax.set_ylabel("Marks (out of 40)", color="#68736C", fontsize=9.5)
    ax.set_title("Attendance vs. Marks", color="#17211B", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlim(45, 105)
    ax.set_ylim(0, 44)

    configure_chart_axes(ax)
    ax.xaxis.grid(True, linestyle=":", color=COLOR_BORDER, alpha=0.8)

    ax.legend(loc="lower right", frameon=False, fontsize=8)
    fig.tight_layout()
    return fig


def plot_actual_vs_predicted_marks(subject_data: List[Dict[str, Any]]) -> plt.Figure:
    """
    Chart 3: Actual vs Predicted Performance Comparison
    """
    sns.set_theme(style="white", font="sans-serif")
    df = pd.DataFrame(subject_data)
    fig, ax = plt.subplots(figsize=(6.5, 3.8))

    x = np.arange(len(df))
    width = 0.32

    bars1 = ax.bar(x - width/2, df["internal_marks"], width, label="Current Marks", color=COLOR_PRIMARY)
    bars2 = ax.bar(x + width/2, df["predicted_marks"], width, label="Predicted Final", color=COLOR_SECONDARY)

    ax.set_ylabel("Marks (out of 40)", color="#68736C", fontsize=9.5)
    ax.set_title("Current vs. Predicted Outcome", color="#17211B", fontsize=11, fontweight="bold", pad=12)
    ax.set_xticks(x)
    ax.set_xticklabels([s.split("(")[0].strip() for s in df["subject"]], rotation=15, ha="right", fontsize=9)
    ax.set_ylim(0, 44)

    configure_chart_axes(ax)

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f"{h:.1f}",
                        xy=(bar.get_x() + bar.get_width() / 2, h),
                        xytext=(0, 3), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, color="#17211B")

    ax.legend(loc="upper right", frameon=False, fontsize=8)
    fig.tight_layout()
    return fig


def plot_weak_subjects_priority(sorted_subjects: List[Dict[str, Any]]) -> plt.Figure:
    """
    Chart 4: Areas Needing Attention (Horizontal Bar Chart)
    """
    sns.set_theme(style="white", font="sans-serif")
    df = pd.DataFrame(sorted_subjects)
    fig, ax = plt.subplots(figsize=(6.5, 3.5))

    color_map = {
        "Needs attention": COLOR_ATTENTION,
        "Improving": COLOR_IMPROVING,
        "On track": COLOR_ON_TRACK
    }
    colors = [color_map.get(p, COLOR_SECONDARY) for p in df["display_status"]]

    y_pos = np.arange(len(df))
    bars = ax.barh(y_pos, df["current_marks"], color=colors, height=0.48)

    ax.set_yticks(y_pos)
    ax.set_yticklabels([s.split("(")[0].strip() for s in df["subject"]], fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Current Marks (out of 40)", color="#68736C", fontsize=9.5)
    ax.set_title("Subject Urgency Hierarchy", color="#17211B", fontsize=11, fontweight="bold", pad=12)
    ax.set_xlim(0, 44)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(COLOR_BORDER)
    ax.spines["bottom"].set_color(COLOR_BORDER)
    ax.xaxis.grid(True, linestyle=":", color=COLOR_BORDER, alpha=0.8)
    ax.yaxis.grid(False)

    for bar, status in zip(bars, df["display_status"]):
        w = bar.get_width()
        ax.annotate(f" {w:.1f} ({status})",
                    xy=(w, bar.get_y() + bar.get_height() / 2),
                    xytext=(3, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=8, color="#17211B", fontweight="medium")

    fig.tight_layout()
    return fig
