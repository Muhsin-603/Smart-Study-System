# Smart Study Recommendation System

## Premium Academic Portal — UI/UX Design System

---

# 1. Design Philosophy

The Smart Study Recommendation System is an academic companion, not an "AI analytics dashboard".

The interface should feel like a **premium university student portal**: calm, structured, trustworthy, human, and focused on helping a student understand where they stand and what they should do next.

The Machine Learning system operates underneath the interface. The UI should not constantly advertise the presence of AI.

### Core principle

> **Show the student where they are, what needs attention, and what to do next.**

The design should prioritize:

1. Academic progress
2. Subject performance
3. Areas needing attention
4. Actionable study recommendations
5. Clear explanations
6. Supporting analytics

Analytics should support the student experience rather than dominate it.

Current education products reinforce this direction. Canvas's 2026 customizable dashboard emphasizes personalized, action-oriented information and makes coursework, grades, feedback, and priorities easier to access. Google Classroom similarly uses a personalized dashboard with modular information tailored to the student's role.

---

# 2. Design Personality

## The product should feel

* Academic
* Calm
* Premium
* Institutional
* Human
* Focused
* Trustworthy
* Modern
* Minimal
* Data-informed

## The product should NOT feel

* Like an AI startup landing page
* Cyberpunk
* Futuristic
* Neon
* Gamified
* Overly corporate
* Glassmorphic
* Crypto/fintech-like
* Filled with glowing gradients
* Filled with decorative AI imagery

Avoid visual clichés such as:

* Robot illustrations
* Neural-network backgrounds
* Brain graphics
* Purple AI gradients
* Glowing data particles
* Excessive glass cards
* "AI-powered" badges everywhere

The student should feel that this is **their academic workspace**, not that a machine is judging them.

---

# 3. Design References

The design language should take structural inspiration from established education products.

## Canvas

Use as inspiration for:

* Persistent navigation
* Course/subject organization
* Student-first dashboard
* Action-oriented information
* To-do / next-action concepts
* Flexible dashboard modules

Canvas's current dashboard supports multiple views and uses dashboard/sidebar content to surface coursework, upcoming work, feedback, and grades.

Canvas's 2026 customizable dashboard also allows students to prioritize and rearrange relevant information.

Do NOT copy Canvas branding.

## Google Classroom

Use as inspiration for:

* Simple navigation
* Personalized student homepage
* Modular dashboard
* Clear information grouping
* Minimal visual hierarchy

Google Classroom describes its homepage as a personalized dashboard that highlights important tasks and allows modules to be organized around what the user needs.

## Khan Academy

Use as inspiration for:

* Progress visualization
* Mastery-oriented presentation
* Clear learner feedback
* Showing what to work on next

Khan Academy uses visual mastery/progress views specifically to help learners understand progress and identify where they should focus next.

Do NOT copy its playful/gamified visual style.

---

# 4. Brand Direction

## Brand concept

The visual identity should communicate:

**"A quiet academic workspace."**

Not:

**"Artificial intelligence has entered the classroom."**

The interface should feel appropriate for:

* University students
* Engineering students
* Academic advisors
* Faculty demonstrations

---

# 5. Color System

Use a restrained academic palette.

## Base colors

```text
Background
#F7F8F6

Surface
#FFFFFF

Primary Text
#17211B

Secondary Text
#68736C

Muted Text
#8A938D

Border
#E2E7E3

Subtle Background
#F0F3F1
```

## Brand

```text
Academic Green
#245C4A

Academic Green Hover
#1D4B3C

Academic Green Soft
#E8F1ED
```

The primary brand color should be used sparingly.

Use it for:

* Primary buttons
* Active navigation
* Important links
* Progress indicators
* Selected states
* Key academic highlights

Do not flood the entire interface with green.

---

# 6. Semantic Colors

Semantic colors communicate academic status.

```text
High Priority
#C94A4A

High Priority Soft
#F8E9E9

Medium Priority
#B98232

Medium Priority Soft
#F7F0E3

Maintain / Healthy
#3E8061

Maintain Soft
#E8F1ED

Informational
#4D6F8F

Informational Soft
#EDF2F6
```

Use semantic colors only where meaning exists.

Do not use red, amber, and green simply as decoration.

---

# 7. Typography

Use **Inter** as the primary font.

Fallback:

```text
Inter, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif
```

## Typography hierarchy

### Page title

```text
28px
Line height: 34px
Weight: 650
```

### Section heading

```text
18px
Line height: 24px
Weight: 600
```

### Subject title

```text
16px
Line height: 22px
Weight: 600
```

### Body

```text
14px
Line height: 21px
Weight: 400
```

### Secondary text

```text
13px
Line height: 19px
Weight: 400
```

### Large metric

```text
28–32px
Weight: 600
```

Avoid excessive uppercase text.

Do not use uppercase labels for every metric.

Prefer:

```text
Predicted final score
```

instead of:

```text
PREDICTED FINAL SCORE
```

---

# 8. Layout

Use a persistent left navigation layout.

```text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│  SIDEBAR       MAIN CONTENT                                  │
│                                                              │
│  Study         Page title                                   │
│                                                              │
│  Overview      Content                                       │
│  Subjects                                                    │
│  Progress                                                    │
│  Study Plan                                                  │
│                                                              │
│  ───────                                                     │
│                                                              │
│  Profile                                                      │
│  Settings                                                     │
│                                                              │
│  Student                                                       │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

The sidebar should remain visually quiet.

Use small icons and labels.

Do not use large colorful icon tiles.

---

# 9. Sidebar Navigation

## Brand

Display:

```text
STUDY
```

or the final project/product name.

Use a small academic mark rather than an AI icon.

## Navigation

```text
Overview
Subjects
Progress
Study Plan
```

Divider.

```text
Profile
Settings
```

Bottom:

```text
Student name
Student ID
Avatar
```

Provide logout access from the profile area.

---

# 10. Dashboard Information Hierarchy

The dashboard should answer four questions immediately:

### 1. Where am I?

Overall academic progress.

### 2. How am I doing?

Current and predicted performance.

### 3. What needs attention?

Weak subjects and academic standing.

### 4. What should I do next?

Study recommendations.

This is more useful than presenting four disconnected KPI cards.

---

# 11. Dashboard Layout

Recommended structure:

```text
Good afternoon, Muhsin

Semester 5 · Computer Science · Artificial Intelligence
─────────────────────────────────────────────────────────

┌──────────────────────────────────┬─────────────────────┐
│                                  │                     │
│ YOUR PROGRESS                    │ THIS WEEK           │
│                                  │                     │
│ 67 / 100                         │ Study target        │
│ ███████████████░░░░░             │ 2.5 hrs / day       │
│                                  │                     │
│ Predicted: 71 / 100              │ Attendance: 84%     │
│                                  │                     │
└──────────────────────────────────┴─────────────────────┘

YOUR SUBJECTS

DAA                         18 / 40
Needs attention             Predicted 22
────────────────────────────────────────

Machine Learning            25 / 40
Improving                   Predicted 28
────────────────────────────────────────

Computer Networks            33 / 40
On track                    Predicted 34

...

WHAT TO FOCUS ON

01  DAA
    Practice problems · 45 min/day

02  Machine Learning
    Revise theory · 30 min/day

03  Attendance
    Current 78% · Target 80%
```

The home page should be useful without requiring the student to open an analytics page.

---

# 12. Welcome Header

The dashboard header should contain:

```text
Good afternoon, [Student Name]

Semester 5 · CSE · [Elective]
```

Do not use excessive motivational copy.

Keep the greeting short.

Example:

```text
Good afternoon, Muhsin

Here is your academic progress for this semester.
```

---

# 13. Overall Progress

The primary performance section should show:

```text
Overall performance

67 / 100
━━━━━━━━━━━━━━━━━━━━░░░░

Predicted final
71 / 100
```

Use a progress bar rather than only a large floating number.

The current score should be visually dominant.

The predicted score should be secondary.

---

# 14. Academic Standing

Academic risk should be displayed as a contextual status.

Instead of a giant:

```text
HIGH RISK
```

use:

```text
Academic standing

Needs attention
```

Then explain why.

Example:

```text
Academic standing

Needs attention

2 subjects currently require focused revision.
```

Risk levels remain:

```text
Low
Medium
High
```

But avoid making the risk label the emotional center of the dashboard.

The purpose is to support action, not create anxiety.

---

# 15. Subject Cards

Subject performance is the core of the application.

Each subject should have a clean horizontal card/list item.

Example:

```text
┌─────────────────────────────────────────────────────────┐
│ DAA                                                     │
│ Design & Analysis of Algorithms                         │
│                                                         │
│ 18 / 40                         Needs attention          │
│ █████████░░░░░░░░░░                                  │
│                                                         │
│ Predicted 22 / 40    Attendance 82%    Study 1.4h      │
└─────────────────────────────────────────────────────────┘
```

Avoid turning every subject into a colorful floating dashboard card.

Use subtle borders and separators.

---

# 16. Subject Status

Use human-readable labels.

Instead of:

```text
HIGH PRIORITY
```

prefer:

```text
Needs attention
```

Instead of:

```text
MEDIUM PRIORITY
```

prefer:

```text
Improving
```

Instead of:

```text
MAINTAIN
```

prefer:

```text
On track
```

Internally the system may still use:

```text
High Priority
Medium Priority
Maintain
```

for its recommendation engine.

The UI should use student-friendly language.

---

# 17. Subject Detail

Clicking/opening a subject should show:

```text
DAA

Current marks
18 / 40

Predicted final
22 / 40

Attendance
82%

Study time
1.4 hrs/day
```

Then:

```text
Your next focus

Practice algorithm problems
45 min/day

Review weak topics
30 min/day
```

Then:

```text
Why this matters

Your current marks are below the
high-priority threshold.

Your study time is also below
2 hours/day.
```

This combines:

* Current performance
* Prediction
* Recommendation
* Explainability

in one place.

---

# 18. Study Plan

The recommendation engine should be presented as a **Study Plan**.

Do not call it:

```text
AI Recommendations
```

or:

```text
AI Intervention Engine
```

Use:

```text
Study Plan
```

The page should answer:

> What should I study next?

---

# 19. Study Plan Layout

```text
Your focus this week

Recommended study time
2.5 hrs / day

──────────────────────────────────────

01
DAA

45 min/day

Practice algorithm problems

──────────────────────────────────────

02
Machine Learning

30 min/day

Revise regression and classification

──────────────────────────────────────

03
Attendance

Target 80%+

Current attendance: 78%
```

Sort by urgency.

---

# 20. Recommendation Categories

Recommendations can include:

```text
Increase study hours
Improve attendance
Practice problems
Revise theory
Focus on weak subjects
Maintain current routine
```

Keep recommendations concise.

Do not generate paragraphs of generic advice.

---

# 21. Recommendation Explainability

Use a section titled:

```text
Why this matters
```

rather than:

```text
Explainability
```

Example:

```text
Why this matters

• Current marks: 18 / 40
• Predicted final: 22 / 40
• Study time: 1.4 hrs/day

Your current marks are below the
high-priority threshold and your
study time is below 2 hours/day.
```

The explanation must come from deterministic rule-based logic.

Never claim that the ML model generated the recommendation.

---

# 22. Progress Page

Create a dedicated:

```text
Progress
```

page.

This is where more detailed analytics belong.

The dashboard should not become a chart museum.

The Progress page can contain:

* Current marks
* Predicted marks
* Subject comparison
* Attendance
* Study hours
* Actual vs predicted performance
* Academic trends

---

# 23. Analytics Layout

```text
Performance overview

┌──────────────────────┬──────────────────────┐
│ Current average      │ Predicted average    │
│ 67 / 40              │ 71 / 40              │
└──────────────────────┴──────────────────────┘

Subject performance

[Bar chart]

Attendance vs marks

[Scatter plot]

Actual vs predicted

[Comparison chart]

Areas needing attention

[Horizontal chart]
```

Charts should support interpretation.

Do not show charts merely because the project uses Matplotlib and Seaborn.

---

# 24. Required Charts

Use:

### Subject-wise marks

Bar chart.

### Attendance vs marks

Scatter plot.

### Actual vs predicted marks

Comparison chart.

### Weak-subject chart

Horizontal bar chart.

Use consistent typography and restrained colors.

---

# 25. Chart Styling

Use:

```python
sns.set_theme(
    style="white",
    font="sans-serif"
)
```

Charts should have:

* Minimal grid lines
* No unnecessary borders
* Clear labels
* Appropriate whitespace
* Consistent type
* Restrained colors

Avoid:

* 3D charts
* Donut charts everywhere
* Heavy gradients
* Decorative icons inside charts
* Excessive annotations

---

# 26. Chart Color System

Use the product palette.

```text
Primary data
#245C4A

Secondary data
#8A938D

High priority
#C94A4A

Medium priority
#B98232

Maintain
#3E8061
```

Do not use arbitrary chart colors.

---

# 27. Model Performance

ML metrics should live in a dedicated area rather than the student dashboard.

Create:

```text
Model Performance
```

inside the Progress or dedicated academic analytics section.

Show:

### Linear Regression

```text
R²
MAE
MSE
RMSE
```

### Decision Tree

```text
Accuracy
Precision
Recall
F1-score
Confusion Matrix
```

These metrics are primarily useful for:

* Academic demonstration
* Project evaluation
* Faculty review
* Technical validation

They should not dominate the student experience.

---

# 28. Student Profile

The Profile page should contain:

```text
Student Profile

Name
Student ID
Elective

Overall attendance
Overall study hours
Previous overall marks
```

Keep it simple.

---

# 29. Academic Data Update

Create a dedicated:

```text
Update academic data
```

section.

Allow the student to update:

* Internal marks
* Attendance
* Study hours
* Elective

Optional:

* Actual final marks

Validate all values.

---

# 30. Login Screen

The login screen should resemble an institutional academic portal.

Example:

```text
                    STUDY

            Your academic progress,
               in one place.

       ┌────────────────────────────┐
       │ Student ID                 │
       └────────────────────────────┘

       ┌────────────────────────────┐
       │ Password                   │
       └────────────────────────────┘

                Sign in

       Academic Performance Portal
```

Keep the background simple.

Use the primary green sparingly.

No:

* AI illustrations
* robots
* neural networks
* glowing effects
* animated particles

---

# 31. Login Brand Area

The login page may contain a small abstract academic mark.

Suitable visual concepts:

* Open book geometry
* Simple upward progress mark
* Minimal monogram
* Academic grid
* Abstract page/learning symbol

Do not use a literal graduation cap unless required.

---

# 32. Buttons

Primary button:

```text
Background: #245C4A
Text: #FFFFFF
Radius: 8px
Height: approximately 40px
```

Secondary button:

```text
Background: transparent
Border: #D9E0DB
Text: #245C4A
Radius: 8px
```

Buttons should not be pill-shaped unless they represent filters/tags.

---

# 33. Inputs

Use:

```text
Background: #FFFFFF
Border: #D9E0DB
Radius: 8px
Height: 42–44px
```

Focus:

```text
Border: #245C4A
```

Labels should appear above fields.

Do not rely only on placeholders.

---

# 34. Status Badges

Badges should be compact.

Example:

```text
Needs attention
```

Use:

```text
Background: #F8E9E9
Text: #9E3D3D
```

Medium:

```text
Background: #F7F0E3
Text: #8B6525
```

On track:

```text
Background: #E8F1ED
Text: #32694F
```

Avoid oversized badges.

---

# 35. Cards

Cards should be used selectively.

```text
Background: #FFFFFF
Border: 1px solid #E2E7E3
Border radius: 12px
Shadow: subtle
```

Do NOT use:

```text
backdrop-filter
glassmorphism
heavy blur
neon glow
large shadows
```

Not every section needs a card.

Use whitespace and dividers to create hierarchy.

---

# 36. Spacing System

Use an 8px spacing scale.

```text
4px
8px
12px
16px
24px
32px
40px
48px
64px
```

Recommended:

```text
Page padding: 32px
Section gap: 32px
Card padding: 20–24px
Element gap: 12–16px
```

The layout should feel spacious but not empty.

---

# 37. Borders

Use subtle borders.

```text
#E2E7E3
```

Avoid dark borders.

Avoid colored borders unless communicating a status.

---

# 38. Shadows

Use shadows sparingly.

Example:

```css
box-shadow:
0 1px 2px rgba(23, 33, 27, 0.04);
```

Cards should look like part of the interface, not floating objects.

---

# 39. Icons

Use a consistent simple icon set.

Preferred style:

* Thin
* Monochrome
* Minimal
* 16–20px

Icons should support recognition.

Do not place icons beside every sentence.

---

# 40. Responsive Design

The application should work on:

* Desktop
* Laptop
* Tablet

On narrow screens:

```text
Sidebar
↓
Collapsed navigation

Two-column sections
↓
Single-column sections
```

Subject cards should remain readable.

Charts should resize naturally.

---

# 41. Accessibility

Maintain:

* High text contrast
* Clear focus states
* Readable font sizes
* Meaningful labels
* Non-color-only status indicators

Do not communicate:

```text
Red = bad
Green = good
```

without also displaying text.

Example:

```text
Needs attention
```

rather than only a red dot.

---

# 42. Empty States

If data is missing, provide meaningful academic context.

Example:

```text
No academic data yet

Add your subject marks, attendance,
and study hours to see your progress.

[Update academic data]
```

Do not show empty charts.

---

# 43. Loading States

Use simple loading indicators.

Avoid elaborate animated loaders.

Example:

```text
Preparing your academic overview...
```

Keep loading experiences short and quiet.

---

# 44. Error States

Errors should be human-readable.

Bad:

```text
MongoServerSelectionTimeoutError
```

Good:

```text
We couldn't connect to the academic database.

Please check the database connection and try again.
```

Technical details can be logged separately.

---

# 45. Academic Risk Presentation

Risk is important but should not dominate the interface.

Use:

```text
Academic standing

Medium

1 subject needs focused attention.
```

Avoid:

```text
⚠️ HIGH RISK STUDENT
```

This system should support students, not label them.

---

# 46. Overall Student Journey

The experience should follow:

```text
LOGIN
  ↓
OVERVIEW
  ↓
UNDERSTAND PERFORMANCE
  ↓
IDENTIFY WEAK SUBJECTS
  ↓
UNDERSTAND WHY
  ↓
FOLLOW STUDY PLAN
  ↓
UPDATE ACADEMIC DATA
  ↓
SEE UPDATED PROGRESS
```

The interface should always make the next useful action obvious.

---

# 47. Information Architecture

```text
Study
│
├── Overview
│
├── Subjects
│   ├── Computer Networks
│   ├── Machine Learning
│   ├── DAA
│   ├── MC
│   └── Elective
│
├── Progress
│   ├── Performance
│   ├── Attendance
│   ├── Study Time
│   └── Model Analytics
│
├── Study Plan
│   ├── Priorities
│   ├── Recommendations
│   └── Explanations
│
├── Profile
│
└── Settings
```

---

# 48. Dashboard Content Priority

Priority order:

```text
1. Current academic state
2. Predicted outcome
3. Subjects needing attention
4. Recommended next actions
5. Supporting metrics
6. Detailed analytics
7. ML model information
```

Never reverse this order.

The student should not have to understand machine learning before understanding their academic situation.

---

# 49. Terminology

Use student-friendly terminology.

| Technical             | UI wording          |
| --------------------- | ------------------- |
| ML Prediction         | Performance outlook |
| Recommendation Engine | Study Plan          |
| Risk Classification   | Academic Standing   |
| Explainability        | Why this matters    |
| High Priority         | Needs attention     |
| Medium Priority       | Improving           |
| Maintain              | On track            |
| Feature               | Academic factor     |
| Model Metrics         | Model performance   |
| Inference             | Prediction          |

Internal Python code may retain technical terminology.

---

# 50. Recommendation Language

Recommendations must be direct.

Good:

```text
Increase DAA practice to 45 minutes/day.
```

Good:

```text
Your attendance is currently 78%.
Aim for at least 80%.
```

Good:

```text
Review regression and classification concepts.
```

Avoid:

```text
AI suggests that you should consider potentially
increasing your engagement with DAA.
```

Do not make simple advice sound like a government report.

---

# 51. Progress Language

Use:

```text
Current
Predicted
Target
Progress
Needs attention
Improving
On track
```

Avoid:

```text
Score Optimization Engine
Predictive Intelligence
Academic Neural Insights
AI Risk Intelligence
```

---

# 52. Dashboard Example

The finished dashboard should visually resemble:

```text
┌──────────────────────────────────────────────────────────────┐
│ STUDY                                                        │
│                                                              │
│ Overview     Good afternoon, Muhsin                         │
│ Subjects     Semester 5 · CSE · Artificial Intelligence     │
│ Progress                                                     │
│ Study Plan   ──────────────────────────────────────────────  │
│                                                              │
│ Profile      YOUR PROGRESS              THIS WEEK            │
│ Settings                                                     │
│              67 / 100                   Study target         │
│              ███████████████░░          2.5 hrs / day        │
│                                          Attendance 84%       │
│              Predicted 71 / 100                              │
│                                                              │
│              YOUR SUBJECTS                                   │
│                                                              │
│              DAA                         18 / 40             │
│              Needs attention             Predicted 22        │
│              ───────────────────────────────────────────     │
│                                                              │
│              Machine Learning            25 / 40             │
│              Improving                   Predicted 28        │
│              ───────────────────────────────────────────     │
│                                                              │
│              Computer Networks           33 / 40             │
│              On track                    Predicted 34        │
│                                                              │
│              WHAT TO FOCUS ON                                │
│                                                              │
│              01  DAA                                          │
│                  Practice algorithm problems · 45 min         │
│                                                              │
│              02  Machine Learning                            │
│                  Revise theory · 30 min                     │
└──────────────────────────────────────────────────────────────┘
```

---

# 53. Dark Mode

Dark mode is optional.

If implemented, it must preserve the same academic character.

Use:

```text
Background
#151A17

Surface
#1D2420

Primary Text
#F0F3F0

Secondary Text
#AAB4AD

Border
#303932

Primary Green
#72A88F
```

Do not convert dark mode into a neon cyberpunk theme.

---

# 54. Streamlit Implementation Guidelines

The design must work within Streamlit.

Use:

* `st.sidebar`
* `st.columns`
* `st.container`
* `st.metric` only when appropriate
* `st.progress`
* `st.dataframe`
* `st.tabs` only where useful
* Custom CSS for visual refinement

Do not rely on excessive nested tabs.

Prefer clear page navigation.

---

# 55. Streamlit CSS

Create a centralized CSS/theme layer.

Do not scatter CSS across every page.

Define reusable styles for:

```text
.page-header
.section-title
.subject-row
.subject-card
.status-badge
.progress-bar
.study-plan-item
.explain-card
.metric
.sidebar
```

Keep styling centralized and consistent.

---

# 56. Metric Cards

Do not use four large KPI cards as the default dashboard structure.

Use metrics inside meaningful sections.

For example:

```text
Your progress

Current average     67 / 100
Predicted final     71 / 100
```

This is preferable to:

```text
[67%] [71%] [PASS] [MEDIUM]
```

floating independently.

---

# 57. Tables

Tables should be used for detailed academic comparison.

Recommended columns:

```text
Subject
Current
Predicted
Attendance
Study time
Status
```

Use compact rows.

Do not make tables visually overwhelming.

---

# 58. Student Data Privacy

The interface must ensure that a student sees only their own academic records.

Never expose:

* Other students' marks
* Other students' predictions
* Other students' recommendations
* Password hashes
* Database identifiers

Admin functionality must be separate.

---

# 59. Admin / Technical Dashboard

If an admin dashboard is implemented, it may use a more analytical layout.

Admin can view:

* Student records
* Dataset size
* Model metrics
* Feature importance
* Confusion matrix
* Retraining controls

However, the admin dashboard must still follow the same visual system.

Do not expose admin controls to students.

---

# 60. ML Feature Visualization

For technical demonstration, the admin/model page may show:

```text
Feature importance

Previous marks
Internal marks
Attendance
Study hours
```

Use a horizontal bar chart.

This is useful for explaining how the Decision Tree behaves.

---

# 61. Recommendation Rules

Maintain the existing rule-based recommendation architecture.

Marks are out of 40.

```text
0–24
Needs attention

25–30
Improving

31–40
On track
```

Attendance:

```text
< 80%
Improve attendance
```

Study time:

```text
< 2 hours/day
Increase study time
```

Recommendations:

```text
Increase study hours
Improve attendance
Practice problems
Revise theory
Focus on weak subjects
Maintain current routine
```

---

# 62. Recommended Study Time

Use:

```text
2.0 hrs/day
All subjects on track

2.5 hrs/day
At least one improving subject

3.0 hrs/day
One subject needs attention

3.5 hrs/day
Two or more subjects need attention
```

This remains a project heuristic and must not be presented as medically or scientifically validated guidance.

---

# 63. Academic Risk

Keep the existing technical classification:

### HIGH

* 2+ high-priority subjects
* OR projected average < 16/40
* OR any predicted failure

### MEDIUM

* Exactly 1 high-priority subject
* OR 2+ medium-priority subjects

### LOW

* Majority of subjects on track
* No predicted failures

But present this in the UI as:

```text
Academic standing
```

rather than a threatening risk dashboard.

---

# 64. Explainability Architecture

Every recommendation must be traceable to actual values.

Example:

```text
DAA · Needs attention

Current marks
18 / 40

Predicted
22 / 40

Attendance
82%

Study time
1.4 hrs/day

Why this matters

• Current marks are below 25/40.
• Study time is below 2 hours/day.

Suggested action

Practice DAA problems for 45 minutes/day.
```

Never invent explanations.

---

# 65. Empty Dashboard

If the student has no academic records:

```text
Welcome to Study

Your academic dashboard is ready.

Add your subject performance to see:
• Your current progress
• Performance outlook
• Subjects needing attention
• Your personalized study plan

[Add academic data]
```

---

# 66. First-Time User Experience

After registration:

```text
Welcome to Study

Let's add your current academic information.
```

Then collect:

1. Profile
2. Elective
3. Subject marks
4. Attendance
5. Study hours

After submission:

```text
Your academic overview is ready.
```

Redirect to Overview.

---

# 67. Design Anti-Patterns

The implementation must NOT introduce:

```text
❌ Neon gradients
❌ Purple AI branding
❌ Glassmorphism
❌ Excessive cards
❌ Huge KPI walls
❌ Animated background
❌ Robot illustrations
❌ Brain/AI imagery
❌ Fake confidence percentages
❌ Unexplained predictions
❌ Excessive badges
❌ Excessive rounded pills
❌ Giant decorative charts
❌ Generic motivational quotes
❌ Fake AI-generated advice
```

---

# 68. Quality Bar

The final UI should look closer to:

```text
Modern university portal
+
Premium productivity application
+
Academic progress tracker
```

and not:

```text
Generic AI dashboard
+
Crypto dashboard
+
Hackathon project template
```

---

# 69. Final Design Principle

The entire interface should follow this hierarchy:

```text
ACADEMIC LIFE
      ↓
PROGRESS
      ↓
SUBJECTS
      ↓
AREAS NEEDING ATTENTION
      ↓
WHAT TO DO NEXT
      ↓
WHY
      ↓
DETAILED ANALYTICS
      ↓
ML TECHNICAL DETAILS
```

The machine learning is an implementation detail that makes the experience useful.

It is not the visual identity of the product.

---

# 70. Final Design Statement

**Smart Study Recommendation System should feel like a calm academic workspace that happens to contain machine learning.**

The student should open the application and immediately understand:

> **Where am I?**

> **What needs attention?**

> **What should I do next?**

> **Why does the system recommend this?**

Everything else is secondary.
