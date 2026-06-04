"""
Health Risk Classification - Batch Prediction Demo
Demonstrates input → output with multiple examples
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import PowerTransformer, StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# LOAD MODEL AND CONFIGURATION
# ============================================================================
print("\n" + "="*80)
print("🏥 HEALTH RISK CLASSIFICATION - BATCH PREDICTION DEMO")
print("="*80)

try:
    with open('best_model.pkl', 'rb') as f:
        model = pickle.load(f)
    
    with open('preprocessing_info.pkl', 'rb') as f:
        preprocessing_info = pickle.load(f)
    
    with open('feature_names.pkl', 'rb') as f:
        feature_names = pickle.load(f)
    
    print("✅ Model loaded successfully")
except FileNotFoundError:
    print("❌ Error: Model files not found!")
    print("   Please run: python health_risk_ml_pipeline.py")
    exit()

# Extract configuration
skewness_dict = preprocessing_info['skewness_dict']
numeric_features = preprocessing_info['numeric_features']
scaler = preprocessing_info['scaler']
best_model_name = preprocessing_info['best_model_name']
best_accuracy = preprocessing_info['best_accuracy']

print(f"✅ Model: {best_model_name} (Accuracy: {best_accuracy:.2%})")

# ============================================================================
# PREDICTION FUNCTION
# ============================================================================
def predict_health_risk(age, bmi, smoker, exercise):
    """Make prediction with given inputs"""
    try:
        input_data = pd.DataFrame({
            'age': [age],
            'bmi': [bmi],
            'smoker': [smoker],
            'exercise_days_per_week': [exercise]
        })
        
        input_processed = input_data.copy()
        
        for col in numeric_features:
            if col in input_processed.columns:
                if abs(skewness_dict[col]) > 0.5:
                    pt = PowerTransformer(method='yeo-johnson')
                    input_processed[col] = pt.fit_transform(input_processed[[col]])
        
        input_processed[numeric_features] = scaler.transform(input_processed[numeric_features])
        
        for col in feature_names:
            if col not in input_processed.columns:
                input_processed[col] = 0
        
        input_processed = input_processed[feature_names]
        
        prediction = model.predict(input_processed)[0]
        
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_processed)[0]
            confidence = max(probabilities)
        else:
            confidence = None
        
        return prediction, confidence
    except Exception as e:
        return None, None

# ============================================================================
# TEST CASES
# ============================================================================
test_cases = [
    {"age": 30, "bmi": 23.5, "smoker": 0, "exercise": 5, "description": "Young & Healthy"},
    {"age": 45, "bmi": 27.5, "smoker": 0, "exercise": 3, "description": "Middle-aged, Average Health"},
    {"age": 65, "bmi": 32.0, "smoker": 1, "exercise": 1, "description": "Senior, Smoker, Low Activity"},
    {"age": 50, "bmi": 25.0, "smoker": 0, "exercise": 6, "description": "Active & Fit"},
    {"age": 55, "bmi": 30.5, "smoker": 1, "exercise": 0, "description": "Smoker, Overweight, Sedentary"},
]

print("\n" + "="*80)
print("BATCH PREDICTION EXAMPLES - INPUT → OUTPUT")
print("="*80)

results = []

for i, test_case in enumerate(test_cases, 1):
    age = test_case["age"]
    bmi = test_case["bmi"]
    smoker = test_case["smoker"]
    exercise = test_case["exercise"]
    description = test_case["description"]
    
    prediction, confidence = predict_health_risk(age, bmi, smoker, exercise)
    
    print(f"\n{'─'*80}")
    print(f"TEST CASE {i}: {description}")
    print(f"{'─'*80}")
    
    # Input
    print(f"\n📥 INPUT:")
    print(f"   Age: {age} years")
    print(f"   BMI: {bmi}")
    print(f"   Smoker: {'Yes' if smoker == 1 else 'No'}")
    print(f"   Exercise Days/Week: {exercise}")
    
    # Output
    print(f"\n📤 OUTPUT:")
    if prediction is not None:
        risk_status = "⚠️  HIGH RISK" if prediction == 1 else "✅ LOW RISK"
        print(f"   Health Risk Status: {risk_status}")
        print(f"   Prediction Code: {prediction}")
        if confidence:
            print(f"   Confidence: {confidence:.2%}")
        
        results.append({
            'Case': description,
            'Age': age,
            'BMI': bmi,
            'Smoker': 'Yes' if smoker == 1 else 'No',
            'Exercise': exercise,
            'Prediction': risk_status,
            'Confidence': f"{confidence:.2%}" if confidence else "N/A"
        })
    else:
        print("   ❌ Error in prediction")

# ============================================================================
# SUMMARY TABLE
# ============================================================================
print(f"\n{'='*80}")
print("📊 SUMMARY - ALL PREDICTIONS")
print(f"{'='*80}\n")

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))

# ============================================================================
# STATISTICS
# ============================================================================
print(f"\n{'='*80}")
print("📈 STATISTICS")
print(f"{'='*80}")

high_risk_count = len([r for r in results if '⚠️' in r['Prediction']])
low_risk_count = len([r for r in results if '✅' in r['Prediction']])

print(f"\nTotal Predictions: {len(results)}")
print(f"High Risk Cases: {high_risk_count}")
print(f"Low Risk Cases: {low_risk_count}")
print(f"\nHigh Risk Percentage: {high_risk_count/len(results)*100:.1f}%")
print(f"Low Risk Percentage: {low_risk_count/len(results)*100:.1f}%")

# ============================================================================
# HOW TO USE FOR CUSTOM PREDICTIONS
# ============================================================================
print(f"\n{'='*80}")
print("🎯 HOW TO USE WITH YOUR OWN DATA")
print(f"{'='*80}")

print("""
Option 1: INTERACTIVE COMMAND LINE
   cd c:\\Users\\khali\\health_risk_classification
   .\\venv\\Scripts\\python.exe predict.py
   
   Then enter your health metrics when prompted.

Option 2: STREAMLIT WEB APP
   .\\venv\\Scripts\\streamlit.exe run app.py
   
   Open browser to: http://localhost:8501
   Use interactive sliders to make predictions.

Option 3: PYTHON SCRIPT (PROGRAMMATIC)
   from predict import predict_health_risk
   
   result = predict_health_risk(age=50, bmi=28, smoker=0, exercise=4)
   prediction, confidence = result
""")

print(f"\n{'='*80}\n")
