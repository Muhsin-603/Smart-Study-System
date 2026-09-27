# MASTER PROMPT: SMART STUDY RECOMMENDATION SYSTEM

Build a complete **college-level Machine Learning mini-project** called:

**Smart Study Recommendation System**

The application must be a **polished Streamlit website** that uses Machine Learning to analyze student academic data, identify weak subjects, predict academic performance, determine academic risk, and provide personalized study recommendations.

Do not add unnecessary features or technologies that are not specified below.

---

# 1. PROJECT OBJECTIVE

The system should:

1. Allow students to log in.
2. Store multiple students and their academic data.
3. Collect student-level and subject-level information.
4. Analyze academic performance.
5. Identify weak subjects.
6. Predict final marks.
7. Predict Pass/Fail.
8. Determine academic risk level.
9. Generate personalized study recommendations.
10. Explain why each recommendation was generated.
11. Display the results through a polished dashboard.

The system should be suitable for demonstration as a **college ML mini-project**.

---

# 2. TECHNOLOGY STACK

Use only the following primary technologies:

### Programming Language

* Python

### Frontend / Application

* Streamlit

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn

### Visualization

* Matplotlib
* Seaborn

### Database

* MongoDB

Do not introduce React, Next.js, Flask, Django, Firebase, PostgreSQL, MySQL, or other frameworks unless absolutely required by a dependency.

The application must run locally.

---

# 3. PROJECT STRUCTURE

Create a clean but beginner-friendly project structure.

Suggested structure:

```text
smart-study-recommendation/
│
├── app.py
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
│
├── data/
│   └── student_dataset.csv
│
├── models/
│   ├── train_models.py
│   ├── linear_regression.pkl
│   └── decision_tree.pkl
│
├── database/
│   └── mongodb.py
│
├── ml/
│   ├── preprocessing.py
│   ├── prediction.py
│   └── evaluation.py
│
├── recommendations/
│   └── recommendation_engine.py
│
├── utils/
│   └── helpers.py
│
└── pages/
    ├── login.py
    ├── dashboard.py
    ├── student_profile.py
    └── recommendations.py
```

You may simplify this structure if necessary for Streamlit, but do not create unnecessary architecture.

Keep the code modular and readable.

---

# 4. STUDENT SUBJECTS

The default academic subjects are:

### Core subjects

* Computer Networks
* Machine Learning
* Design and Analysis of Algorithms (DAA)
* MC

### Elective

The student chooses ONE elective:

* Software Project Management
* Artificial Intelligence

Therefore, each student has **5 subjects total**.

Make the elective selectable during data entry.

---

# 5. STUDENT DATA

Collect the following general student information:

```text
Student Name
Student ID
Password
Overall Attendance %
Overall Study Hours/day
Previous Overall Marks
```

For each subject collect:

```text
Subject Name
Previous Marks
Current/Internal Marks
Attendance %
Study Hours/day
```

Marks are assumed to be **out of 40**.

Validate all inputs.

Examples:

```text
Marks: 0–40
Attendance: 0–100
Study hours: 0 or greater
```

Do not silently accept invalid values.

---

# 6. SYNTHETIC DATASET

A real dataset is not available.

Create a **synthetic CSV dataset** for training the ML models.

The dataset should contain enough realistic records for a meaningful demonstration, preferably at least several hundred student-subject records.

Do NOT claim that the synthetic dataset represents real-world student populations.

Clearly document in the README that the dataset is synthetic and created for academic demonstration.

Suggested columns:

```text
student_id
subject
previous_marks
internal_marks
attendance
study_hours
final_marks
pass_fail
```

Generate realistic relationships between the variables.

For example:

* Higher attendance should generally correlate with better performance.
* Higher study hours should generally correlate with better performance.
* Previous marks should have some relationship with final marks.
* Add reasonable noise so that the dataset is not perfectly predictable.

Do not make the dataset unrealistically perfect.

---

# 7. MACHINE LEARNING

Implement two ML models.

## Model 1: Linear Regression

Use Linear Regression to predict:

```text
Final Marks
```

Features should include relevant academic variables such as:

```text
Previous Marks
Internal Marks
Attendance
Study Hours
```

The model output should be converted/clamped appropriately to the valid marks range of 0–40.

Display:

```text
Predicted Final Marks
```

---

## Model 2: Decision Tree

Use a Decision Tree classifier to predict:

```text
Pass / Fail
```

Use appropriate features from the student academic data.

Display:

```text
Predicted Result: PASS / FAIL
```

Also use the student's predicted/observed academic performance to determine an:

```text
Academic Risk Level
```

---

# 8. MODEL TRAINING

Split the synthetic dataset into training and testing data.

Use an appropriate train/test split, such as:

```text
80% training
20% testing
```

Use a fixed random state so results are reproducible.

Evaluate the models.

For Linear Regression display:

* MAE
* MSE
* R²

For Decision Tree display:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

Do not fabricate evaluation scores.

Calculate them from the actual test results.

---

# 9. MODEL COMPARISON

The application should include a simple ML Model Performance section showing the actual evaluation metrics.

For example:

```text
Linear Regression
MAE: actual calculated value
MSE: actual calculated value
R²: actual calculated value

Decision Tree
Accuracy: actual calculated value
Precision: actual calculated value
Recall: actual calculated value
F1 Score: actual calculated value
```

Use charts where appropriate.

Do not claim that one model is better unless the relevant metric actually supports that interpretation.

---

# 10. RECOMMENDATION ENGINE

Recommendations must be **rule-based**, not generated by an LLM.

The system should identify weak subjects and generate recommendations using the student's:

* Marks
* Attendance
* Study hours
* Predicted performance

## Marks rules

Marks are out of 40.

Use these exact boundaries:

```text
0–24   → High Priority
25–30  → Medium Priority
31–40  → Maintain
```

## Attendance

```text
Attendance < 80%
→ Recommend improving attendance
```

## Study hours

```text
Study hours < 2 hours/day
→ Recommend increasing study time
```

---

# 11. RECOMMENDATION TYPES

The system may generate these recommendations:

```text
Increase study hours
Improve attendance
Practice problems
Revise theory
Focus on weak subjects
Maintain current routine
```

Recommendations should depend on the student's actual data.

Example:

```text
Subject: DAA
Marks: 18/40
Attendance: 85%
Study Hours: 1.5/day

Recommendations:
- High Priority: Focus on DAA
- Increase study time
- Practice more DAA problems
```

Another example:

```text
Subject: Computer Networks
Marks: 34/40
Attendance: 92%
Study Hours: 2.5/day

Recommendation:
- Maintain current routine
```

Do not give the same recommendation to every student.

---

# 12. RECOMMENDED STUDY TIME

Calculate a recommended daily study time based on the student's weak areas.

Use a simple transparent rule-based system.

Example:

```text
No weak subjects:
2 hours/day

One medium-priority subject:
2.5 hours/day

One or more high-priority subjects:
3 hours/day

Multiple high-priority subjects:
3.5 hours/day
```

The exact calculation must be documented in the code.

Do not pretend this is scientifically validated. It is a project-level heuristic.

---

# 13. PRIORITY ORDER

Generate a subject priority list.

Example:

```text
Priority:
DAA > Machine Learning > Computer Networks > MC > AI
```

Sort subjects based on academic priority:

```text
High Priority
    ↓
Medium Priority
    ↓
Maintain
```

Within the same category, use lower marks first.

---

# 14. ACADEMIC RISK LEVEL

Create three risk levels:

```text
LOW
MEDIUM
HIGH
```

Use transparent rules.

Suggested approach:

### HIGH

If:

* multiple high-priority subjects, OR
* predicted overall performance is low, OR
* predicted result is FAIL

### MEDIUM

If:

* one high-priority subject, OR
* multiple medium-priority subjects

### LOW

If:

* most subjects are in the Maintain category
* predicted result is PASS
* no major academic weaknesses exist

Clearly document the exact implementation.

---

# 15. EXPLAINABILITY

Every recommendation should explain WHY it was generated.

Example:

```text
Why is DAA high priority?

• Current marks: 18/40
• Attendance: 82%
• Study time: 1.5 hours/day
• Predicted final marks: 22/40

Reason:
Your current marks are below the high-priority threshold
and your study time is below 2 hours/day.
```

This is important because the project should not behave like a mysterious oracle.

---

# 16. DASHBOARD

Create a polished Streamlit dashboard.

The dashboard should contain:

## Student Profile

```text
Name
Student ID
Attendance
Study Hours
```

## Overall Performance

Show cards for:

```text
Overall Score
Predicted Score
Pass/Fail
Academic Risk
```

Example:

```text
Overall Score: 67%

Predicted Score: 71%

Result: PASS

Risk: MEDIUM
```

Do not hard-code these values.

Calculate them from the actual student's data.

---

# 17. SUBJECT PERFORMANCE

Show a subject table containing:

```text
Subject
Current Marks
Predicted Marks
Attendance
Study Hours
Priority
```

Example:

```text
DAA             18/40    22/40    82%    1.5h    HIGH
Machine Learning 25/40   28/40    85%    1.8h    MEDIUM
CN              33/40    34/40    91%    2.5h    MAINTAIN
MC              35/40    35/40    94%    2.5h    MAINTAIN
AI              29/40    31/40    87%    2.0h    MEDIUM
```

Use the student's selected elective.

---

# 18. VISUALIZATIONS

Use **Matplotlib and Seaborn**.

Include:

### 1. Subject-wise Marks

Bar chart showing marks for each subject.

### 2. Attendance vs Marks

Scatter plot showing the relationship between attendance and marks.

### 3. Actual vs Predicted Marks

Compare actual/current marks against predicted final marks.

### 4. Weak Subject Chart

Clearly visualize subjects requiring attention.

Do not create unnecessary charts.

Charts must use actual student data.

---

# 19. LOGIN SYSTEM

Implement a simple student login system.

Multiple students must be supported.

Store authentication information in MongoDB.

Do NOT store plain-text passwords.

Use password hashing with an appropriate Python library.

The login system should provide:

```text
Student ID
Password
Login
```

After login, show only that student's information.

A student must not be able to access another student's academic data.

---

# 20. MONGODB

Use MongoDB for persistent storage.

Create appropriate collections, for example:

```text
students
academic_records
```

Store:

```text
Student profile
Hashed password
Subjects
Marks
Attendance
Study hours
Elective
```

Use environment variables for the MongoDB connection string.

Example:

```text
MONGODB_URI
```

Provide a `.env.example`.

Never hard-code credentials.

Handle database connection errors gracefully.

---

# 21. STREAMLIT PAGES

Use a clear navigation structure.

Suggested pages:

```text
Login
Dashboard
Student Profile
Performance Analysis
Recommendations
```

The exact implementation may use Streamlit's current navigation approach.

Keep navigation simple.

---

# 22. UI DESIGN

The interface should look like a polished modern academic dashboard.

Use:

* Clean layout
* Consistent spacing
* Cards
* Clear typography
* Tables
* Charts
* Appropriate visual hierarchy
* Responsive Streamlit layout

Avoid:

* Excessive animations
* Unnecessary gradients
* Clutter
* Huge decorative elements
* Fake AI branding

The UI should feel like a real academic analytics application.

---

# 23. DATA VALIDATION

Validate all user input.

Examples:

```text
Marks:
0 <= marks <= 40

Attendance:
0 <= attendance <= 100

Study hours:
study_hours >= 0
```

Prevent empty required fields.

Show useful Streamlit error messages.

Do not crash because a student entered an invalid value.

---

# 24. ERROR HANDLING

Handle:

* MongoDB unavailable
* Missing dataset
* Missing trained model
* Invalid input
* Empty records
* Login failure
* Model prediction errors

Display understandable messages.

Do not expose sensitive stack traces to normal users.

---

# 25. MODEL FILES

Train the models using a separate training script.

Save trained models using an appropriate serialization method such as `joblib`.

The application should load the saved models rather than retraining them every time the Streamlit application starts.

Provide a clear command in the README for:

```text
1. Generate dataset
2. Train models
3. Start Streamlit application
```

---

# 26. SYNTHETIC DATA GENERATION

Create a Python script that generates the CSV dataset.

The generator should:

* Create realistic academic records.
* Use random but reproducible values.
* Create relationships between attendance, study hours, previous marks, internal marks and final marks.
* Add reasonable noise.
* Produce pass/fail labels based on final marks.
* Avoid impossible values.

Use a fixed random seed.

---

# 27. README

Create a complete beginner-friendly README containing:

## Project Overview

## Features

## Technology Stack

## Project Structure

## Dataset

Clearly state:

> The dataset is synthetically generated for educational demonstration and does not represent real student data.

## Installation

Example:

```bash
pip install -r requirements.txt
```

## MongoDB Setup

Explain how to create the database and configure:

```text
MONGODB_URI
```

## Generate Dataset

## Train Models

## Run Application

Example:

```bash
streamlit run app.py
```

## ML Algorithms

Explain:

* Linear Regression
* Decision Tree

## Evaluation Metrics

Explain:

* MAE
* MSE
* R²
* Accuracy
* Precision
* Recall
* F1-score

## Recommendation Logic

Explain the thresholds and rules.

## Limitations

Mention that:

* The dataset is synthetic.
* Recommendations are heuristic.
* Predictions are for educational demonstration.
* The system should not be treated as a real academic assessment system.

---

# 28. REQUIREMENTS.TXT

Create a requirements.txt containing the actual dependencies used.

At minimum, use the necessary packages for:

```text
streamlit
pandas
numpy
scikit-learn
matplotlib
seaborn
pymongo
python-dotenv
joblib
```

Do not add packages that are not actually required.

---

# 29. IMPORTANT DEVELOPMENT RULES

Follow these rules strictly:

1. Do not invent missing requirements.
2. Do not add unnecessary features.
3. Do not hard-code student results.
4. Do not fabricate ML evaluation metrics.
5. Do not claim synthetic data is real-world data.
6. Do not use an LLM API for recommendations.
7. Recommendations must be explainable rule-based logic.
8. Use actual model predictions.
9. Use actual MongoDB data.
10. Keep the code beginner-friendly.
11. Use meaningful variable and function names.
12. Add comments where the ML logic may be difficult for a beginner.
13. Avoid over-engineering.
14. Keep configuration in environment variables.
15. Do not expose credentials.
16. Validate all user inputs.
17. Make the application runnable locally.
18. Ensure all imports and files are consistent.
19. Do not leave placeholder functions such as `TODO` for core functionality.
20. Do not claim something works unless it has been implemented.

---

# 30. FINAL EXPECTED USER EXPERIENCE

A student should be able to:

```text
Open Website
      ↓
Login
      ↓
View Dashboard
      ↓
View Student Profile
      ↓
View Current Performance
      ↓
View Predicted Performance
      ↓
View Pass/Fail Prediction
      ↓
View Academic Risk
      ↓
See Weak Subjects
      ↓
See Subject Priority
      ↓
See Personalized Recommendations
      ↓
See Why Each Recommendation Was Given
```

The final application should demonstrate the complete ML pipeline:

```text
Data Collection
      ↓
Synthetic Dataset
      ↓
Data Preprocessing
      ↓
Train/Test Split
      ↓
Linear Regression
      ↓
Final Marks Prediction
      ↓
Decision Tree
      ↓
Pass/Fail Prediction
      ↓
Risk Analysis
      ↓
Rule-Based Recommendation Engine
      ↓
Streamlit Dashboard
      ↓
MongoDB Storage
```

---

# 31. BEFORE FINISHING

Before declaring the project complete, verify:

* The application starts successfully.
* Login works.
* MongoDB connection works.
* Multiple students can be stored.
* Student data is isolated between accounts.
* Synthetic dataset can be generated.
* Models can be trained.
* Models can be loaded.
* Predictions work.
* Recommendations change according to student data.
* Charts use actual data.
* Invalid input is handled.
* No credentials are hard-coded.
* README instructions work.
* requirements.txt contains all required packages.
* There are no missing imports.
* There are no obvious runtime errors.

If you encounter an implementation issue, fix the root cause rather than hiding the error.

Build the project as a **complete runnable mini-project**, not merely a UI mockup or collection of code snippets.
