# Smart Study Recommendation System 🎓

A complete college-level Machine Learning mini-project built with **Python**, **Streamlit**, **Scikit-learn**, and **MongoDB Atlas**. 

The system analyzes student academic data, identifies weak subjects, predicts final semester marks using **Linear Regression**, forecasts Pass/Fail status using a **Decision Tree Classifier**, determines academic risk levels, and provides personalized, explainable study recommendations. It also incorporates a **continual learning loop** where verified student outcomes are fed back to retrain and refine the ML models.

---

## 📌 Features

1. **Student Authentication & Isolation**:
   - Secure student registration and login with salted PBKDF2-SHA256 password hashing.
   - Strict data privacy ensuring students can only access and modify their own records.
2. **Interactive Student Dashboard**:
   - Academic KPI cards (Average Score, Predicted Final Score, Pass/Fail Result, Academic Risk Badge).
   - Recommended daily study target (hours/day) tailored to the student's weak subjects.
3. **Subject Analytics & Rich Visualizations**:
   - Subject performance breakdown across 4 Core subjects (*Computer Networks*, *Machine Learning*, *DAA*, *Microcontrollers*) and 1 chosen Elective (*Software Project Management* or *Artificial Intelligence*).
   - 4 Matplotlib & Seaborn visualizations:
     1. Subject-wise Marks Bar Chart with priority reference lines.
     2. Attendance vs. Marks Scatter Plot with cohort reference.
     3. Current vs. Predicted Final Performance grouped bar chart.
     4. Weak Subject Priority Matrix.
4. **Explainable Rule-Based Recommendation Engine**:
   - Transparent rules for subject priorities (High, Medium, Maintain).
   - Explicit rationales explaining *why* each recommendation was generated based on the student's exact marks, attendance, and study hours.
5. **Real-Time Data Updating**:
   - Students can update their marks, attendance, study hours, or elective in real time.
6. **Continual Learning Pipeline**:
   - Students can log their verified semester final marks, automatically updating the dataset and triggering retraining to improve model accuracy over time.
7. **Admin & ML Operations Dashboard**:
   - Cohort-wide student performance directory.
   - Actual test set ML metrics (MAE, MSE, RMSE, R², Accuracy, Precision, Recall, F1-Score, Confusion Matrix).
   - Live continual learning status and manual retraining controls.

---

## 🛠️ Technology Stack

* **Programming Language**: Python 3.11+
* **Web Application & UI**: Streamlit
* **Data Processing**: Pandas, NumPy
* **Machine Learning**: Scikit-learn (Linear Regression, Decision Tree Classifier)
* **Visualizations**: Matplotlib, Seaborn
* **Database**: MongoDB Atlas (PyMongo)
* **Model Serialization**: Joblib
* **Configuration**: Python-Dotenv

---

## 📁 Project Structure

```text
Smart Study system/
│
├── app.py                             # Main Streamlit web application
├── requirements.txt                   # Project dependencies
├── README.md                          # Project documentation
├── .env                               # Environment variables (MongoDB credentials)
├── .env.example                       # Environment configuration template
├── .gitignore                         # Git exclusion rules
│
├── data/
│   ├── generate_dataset.py            # Synthetic dataset generator script
│   └── student_dataset.csv            # Generated synthetic dataset (1,500 records)
│
├── models/
│   ├── train_models.py                # Model training and evaluation script
│   ├── linear_regression.pkl          # Trained Linear Regression model
│   ├── decision_tree.pkl              # Trained Decision Tree classifier
│   └── model_metrics.json             # Calculated test metrics report
│
├── database/
│   └── mongodb.py                     # MongoDB Atlas connection & CRUD operations
│
├── ml/
│   ├── preprocessing.py               # Feature extraction and train/test splitting
│   ├── prediction.py                  # Model inference and clamping
│   └── evaluation.py                  # Regression & classification metric calculations
│
├── recommendations/
│   └── recommendation_engine.py       # Rule-based heuristics, risk, and explainability
│
└── utils/
    └── helpers.py                     # Input validators and Matplotlib/Seaborn plots
```

---

## 📊 Dataset Notice

> **Important**: The base dataset is synthetically generated for academic demonstration and does not represent real-world student populations. It introduces realistic statistical correlations and noise across marks, attendance, study hours, and academic outcomes.

---

## 🚀 Setup & Installation

### 1. Clone or Open Project Directory
```bash
cd "Smart Study system"
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure MongoDB Atlas (`.env`)
Create a `.env` file in the project root:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.a8wl8vu.mongodb.net/smart_study_db?retryWrites=true&w=majority&appName=Cluster0
DB_NAME=smart_study_db
ADMIN_PASSWORD=admin123
PASSING_MARKS=16
```

### 4. Generate Synthetic Dataset
```bash
python data/generate_dataset.py
```

### 5. Train & Evaluate ML Models
```bash
python models/train_models.py
```

### 6. Launch the Application
```bash
streamlit run app.py
```

---

## 🤖 Machine Learning Pipeline & Metrics

### Model 1: Linear Regression (Final Marks Prediction)
* **Target**: Continuous final marks (0.0 to 40.0). Clamped to valid boundaries.
* **Features**: Previous Marks, Internal Marks, Attendance %, Study Hours/day.
* **Test Metrics (80/20 Split)**:
  * **MAE**: `1.57`
  * **MSE**: `3.97`
  * **R² Score**: `0.91`

### Model 2: Decision Tree Classifier (Pass / Fail Prediction)
* **Target**: Binary classification (0: Fail, 1: Pass) using a 16/40 passing mark threshold.
* **Test Metrics (80/20 Split)**:
  * **Accuracy**: `93.7%`
  * **Precision**: `96.3%`
  * **Recall**: `96.7%`
  * **F1-Score**: `0.965`

---

## 💡 Recommendation Logic & Heuristics

* **Priority Thresholds (Marks out of 40)**:
  * `0 - 24`: **High Priority** (Immediate intervention required)
  * `25 - 30`: **Medium Priority** (Consistent review needed)
  * `31 - 40`: **Maintain** (Solid performance)
* **Attendance Benchmark**:
  * Attendance < 80% triggers attendance improvement advice.
* **Study Hours Benchmark**:
  * Study hours < 2.0 hours/day triggers study time increase advice.
* **Recommended Daily Study Target**:
  * No weak subjects: `2.0 hours/day`
  * One medium-priority subject: `2.5 hours/day`
  * One high-priority subject: `3.0 hours/day`
  * Multiple high-priority subjects: `3.5 hours/day`
* **Academic Risk Levels**:
  * **HIGH**: Multiple high-priority subjects, OR predicted average < 16/40, OR any predicted FAIL.
  * **MEDIUM**: One high-priority subject, OR multiple medium-priority subjects.
  * **LOW**: Most subjects in Maintain category, no FAIL predicted.

---

## ⚠️ Academic Limitations
* The dataset is synthetic and tailored for educational demonstration.
* Recommendations are heuristic rule-based aids and should not be used as clinical or institutional evaluations.
