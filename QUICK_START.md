# 🚀 Quick Start Guide - Health Risk Classification

## Summary of What Was Done ✅

### 1. Data Analysis
- ✅ Loaded dataset with 1,000 health records
- ✅ Analyzed skewness for all 4 numeric features
- ✅ Identified right-skewed "smoker" feature

### 2. Data Preprocessing
- ✅ Applied **PowerTransformer** to skewed features (smoker)
- ✅ Applied **StandardScaler** to normal features (age, bmi, exercise_days)
- ✅ Split data: 80% training (800 samples), 20% testing (200 samples)

### 3. Model Training & Comparison
Trained 7 classifiers using a unified loop:

| Rank | Model | Accuracy | Status |
|------|-------|----------|--------|
| 🥇 1 | **KNN Classifier** | **97.50%** | ⭐ BEST |
| 🥈 2 | KNeighbors Classifier | 96.50% | ✅ |
| 🥉 3 | SVC | 95.00% | ✅ |
| 4 | Logistic Regression | 93.50% | ✅ |
| 5 | Gaussian NB | 92.00% | ✅ |
| 6 | SGD Classifier | 90.50% | ✅ |
| - | Multinomial NB | ❌ | Error (requires non-negative features) |

### 4. Best Model Details
- **Model:** KNN Classifier (k-Nearest Neighbors)
- **Accuracy:** 97.50%
- **Precision (High Risk):** 92%
- **Recall (High Risk):** 88%
- **True Negatives:** 173/175 (98.8%)
- **True Positives:** 22/25 (88%)

### 5. Output Files Generated
```
✅ skewness_distribution.png      - Feature distribution analysis
✅ model_comparison_results.csv    - Accuracy comparison table
✅ best_model.pkl                 - Trained KNN model
✅ preprocessing_info.pkl         - Preprocessing config
✅ feature_names.pkl              - Feature names
✅ SUMMARY_REPORT.txt             - Pipeline summary
✅ health_risk_ml_pipeline.py     - ML pipeline script
✅ app.py                         - Interactive web app
✅ requirements.txt               - Python dependencies
✅ README.md                      - Full documentation
```

---

## 🎮 How to Use the Web Application

### Step 1: Activate Virtual Environment
```powershell
cd c:\Users\khali\health_risk_classification
.\venv\Scripts\Activate.ps1
```

### Step 2: Run the Interactive App
```powershell
streamlit run app.py
```

### Step 3: Open in Browser
Your browser will automatically open to:
```
http://localhost:8501
```

### Step 4: Make Predictions
1. **Adjust sliders** for your health metrics:
   - Age: 18-69 years
   - BMI: 12.5-40.2
   - Smoking: Yes/No
   - Exercise: 0-7 days/week

2. **Click "Predict Health Risk"** button

3. **View Results:**
   - Health Risk Status (High/Low)
   - Confidence Score
   - Personalized recommendations

---

## 🔧 Command Reference

### Run ML Pipeline (One-Time Setup)
```powershell
python health_risk_ml_pipeline.py
```

### Start Web Application
```powershell
streamlit run app.py
```

### Stop Web App
Press `Ctrl + C` in terminal

### Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 💡 Example Predictions

### Low Risk Example
- Age: 30
- BMI: 23.5
- Smoker: No
- Exercise: 5 days/week
- **Prediction:** ✅ LOW RISK (Confidence: 99%)

### High Risk Example
- Age: 65
- BMI: 32.0
- Smoker: Yes
- Exercise: 1 day/week
- **Prediction:** ⚠️ HIGH RISK (Confidence: 92%)

---

## 📊 Skewness Analysis Results

```
Feature                    Skewness    Type           Preprocessing
─────────────────────────────────────────────────────────────────
age                        -0.0423     Normal         StandardScaler
bmi                        +0.0122     Normal         StandardScaler
smoker                     +1.1441     Right Skewed   PowerTransformer + StandardScaler
exercise_days_per_week     +0.0116     Normal         StandardScaler
```

---

## 🎯 Key Features of the Application

✨ **Interactive Interface**
- Real-time slider controls
- Instant predictions
- Visual confidence scores

📊 **Model Information**
- Display best model name
- Show accuracy metrics
- Feature skewness details
- Preprocessing methods

📈 **Comprehensive Results**
- Classification metrics
- Confusion matrix
- Precision/Recall/F1-Score

💬 **Health Recommendations**
- Personalized risk interpretation
- Actionable health suggestions
- Risk level explanation

---

## ⚙️ Technical Details

### Data Preprocessing Pipeline
```python
Raw Data
    ↓
Identify Features: age, bmi, smoker, exercise_days_per_week
    ↓
Calculate Skewness
    ↓
Apply PowerTransformer (skewed features only)
    ↓
Apply StandardScaler (all numeric features)
    ↓
Train-Test Split (80-20)
    ↓
Ready for Model Training
```

### Model Training Loop
```python
for each classifier in [LogReg, KNN, SGD, KNeighbors, SVC, GaussianNB, MultinomialNB]:
    fit model on training data
    predict on test data
    calculate accuracy
    generate classification report
    store results
```

---

## 🔐 Model Files & Persistence

All trained models are saved in binary format using Python's `pickle` module:

1. **best_model.pkl** - The trained KNN classifier
   - Ready to make predictions
   - Contains all learned parameters

2. **preprocessing_info.pkl** - Preprocessing configuration
   - StandardScaler parameters
   - PowerTransformer parameters
   - Skewness dictionary

3. **feature_names.pkl** - Feature column names
   - Ensures input consistency
   - Prevents feature mismatch errors

---

## 📝 File Locations

All files are in:
```
c:\Users\khali\health_risk_classification\
```

Key files:
- Pipeline: `health_risk_ml_pipeline.py`
- Web App: `app.py`
- Data: `11_health_risk_classification_1000.csv`
- Models: `best_model.pkl`, `preprocessing_info.pkl`, `feature_names.pkl`
- Results: `model_comparison_results.csv`, `skewness_distribution.png`

---

## ⚡ Performance Metrics

**KNN Classifier Performance:**
```
Accuracy:   97.50% (195 out of 200 correct)
Precision:  92% (high-risk predictions are accurate)
Recall:     88% (detects 88% of actual high-risk cases)
F1-Score:   0.90 (balanced precision-recall)
```

**Confusion Matrix Interpretation:**
```
Actual vs Predicted:
                Predicted Negative    Predicted Positive
Actual Negative      173 (TN)             2 (FP)
Actual Positive        3 (FN)            22 (TP)

- True Negatives (TN):   173 ✓ (correctly identified low risk)
- False Positives (FP):    2 (incorrectly flagged as high risk)
- False Negatives (FN):    3 (missed actual high risk)
- True Positives (TP):    22 ✓ (correctly identified high risk)
```

---

## 🎓 What You Learned

This project demonstrates:

✅ **Exploratory Data Analysis (EDA)**
- Data loading and inspection
- Statistical analysis
- Skewness calculation and visualization

✅ **Feature Engineering**
- Skewness-based preprocessing decisions
- PowerTransformer for non-normal distributions
- StandardScaler for normalization

✅ **Model Comparison**
- Training multiple classifiers
- Performance metrics calculation
- Model selection criteria

✅ **Web Application Development**
- Streamlit framework usage
- User input handling
- Real-time predictions
- Result visualization

✅ **Model Persistence**
- Pickle serialization
- Model loading and inference
- Preprocessing pipeline saving

---

## 🆘 Troubleshooting

**Q: App won't start**
A: Make sure virtual environment is activated and streamlit is installed
```powershell
pip install streamlit
```

**Q: "Model files not found" error**
A: Run the pipeline first to generate the files
```powershell
python health_risk_ml_pipeline.py
```

**Q: Port 8501 already in use**
A: Use a different port
```powershell
streamlit run app.py --server.port 8502
```

**Q: Predictions seem off**
A: Ensure input values are within training data range:
- Age: 18-69
- BMI: 12.5-40.2
- Exercise: 0-7 days

---

## 📚 Resources

- [Streamlit Documentation](https://docs.streamlit.io/)
- [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)
- [Seaborn Gallery](https://seaborn.pydata.org/examples.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

**Status:** ✅ Complete and Ready to Use!
**Date:** June 4, 2026
